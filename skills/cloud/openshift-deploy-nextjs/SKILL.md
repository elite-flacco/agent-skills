---
name: openshift-deploy-nextjs
description: Deploy a Next.js application to OpenShift from scratch. Use this skill when the user wants to deploy a new Next.js app to OpenShift, mentions "deploy to openshift", "ocp deployment", needs help with OpenShift builds, or wants to get their Next.js app running in a Kubernetes/OpenShift cluster. Also trigger for troubleshooting OpenShift deployment issues like BuildPodEvicted, route problems, or proxy configuration.
---

# Deploy Next.js to OpenShift

Guide the user through deploying a Next.js application to OpenShift, handling the complete workflow from preparation to verification.

## Overview

This skill walks through:
1. Prerequisites verification
2. App preparation (next.config.ts, Dockerfile)
3. Optional OpenShift configuration generation
4. Building the image in OpenShift
5. Tagging and deploying
6. Configuring environment variables and proxy
7. Exposing with TLS
8. Verification and troubleshooting

## Important Context

**OpenShift Environment Specifics:**
- Corporate proxy may be required (check your organization's proxy settings)
- Namespace = Project (terms are interchangeable)
- TLS edge termination required for external routes
- Next.js builds need 4Gi memory (TypeScript checking is intensive)
- Dummy env vars needed at build time for Next.js pre-rendering

## Step 1: Prerequisites Check

Before starting, verify:

```bash
# Check OpenShift CLI is installed and logged in
oc whoami

# Check current project/namespace
oc project

# List available projects if needed
oc get projects

# Verify current directory
pwd
ls -la
```

**Ask the user:**
- Are you logged into OpenShift? (show `oc whoami` output)
- Which namespace/project do you want to use? (show available projects)
- Are you in the root directory of your Next.js app? (should see package.json, app/, etc.)

If any prerequisite is missing, guide them to fix it before proceeding.

## Step 2: Prepare the App

### Check next.config.ts

Read the current `next.config.ts` and check if it has `output: 'standalone'`:

```typescript
const nextConfig: NextConfig = {
  output: 'standalone',
};
```

**If missing:** Explain why it's needed (Docker optimization) and offer to add it.

### Check/Create Dockerfile

Look for a Dockerfile in the app directory.

**If exists:** Read it and verify it has:
- Multi-stage build (deps → builder → runtime)
- `ENV ADO_PAT=dummy_build_value` in builder stage (or similar dummy values for required env vars)
- Proper `npm run build` command
- Standalone output copied correctly

**If missing or incomplete:** Offer to create/fix it. Use the template from our deployment guide, adapted to their app's needs.

**Why dummy env vars?** Explain: Next.js pre-renders pages during build. If pages need environment variables (like ADO_PAT), the build hangs without them. We provide dummy values at build time; real values are injected at runtime.

## Step 3: OpenShift Configuration (Optional)

Ask: "Do you want to generate Helm charts and pipeline files using ocp-onboard?"

**If yes:**
1. Explain: "ocp-onboard will generate deployment manifests, but it's interactive. I'll tell you the exact command to run."
2. Provide the command:
   ```bash
   ocp-onboard --add-service apps/your-app-name
   ```
3. Tell them what to expect:
   - Continue? → `y`
   - Language → `4` (Nodejs)
   - Namespace → their-namespace (the one they're using)
4. Wait for them to confirm it's done
5. Note: "The automated pipeline needs Quay registry permissions. We'll do manual deployment for now, which is simpler."

**If no:** Skip to next step.

## Step 4: Build Image in OpenShift

### Switch to project
```bash
oc project <their-namespace>
```

### Navigate to app directory
Confirm they're in the directory containing the Dockerfile:
```bash
pwd
ls Dockerfile
```

### Create build configuration with memory limits

**CRITICAL:** Next.js builds need 4Gi memory. Always set this upfront.

```bash
# Create build config with Docker strategy
oc new-build --binary --name=<app-name> --strategy=docker

# Immediately increase memory limits
oc patch bc/<app-name> --type=json -p='[
  {
    "op":"add",
    "path":"/spec/resources",
    "value":{
      "limits":{"memory":"4Gi","cpu":"2"},
      "requests":{"memory":"2Gi","cpu":"1"}
    }
  }
]'
```

**Explain why:** "Next.js builds with TypeScript are memory-intensive. 4Gi prevents BuildPodEvicted errors we'd otherwise hit."

### Start the build

```bash
oc start-build <app-name> --from-dir=. --follow
```

**Tell the user:** "This will take 5-10 minutes (npm install is slow). I'll watch the logs."

Monitor for:
- ✅ `Successfully pushed` → build succeeded
- ❌ `BuildPodEvicted` → increase memory (though we already set 4Gi, so this is rare)
- ❌ `Collecting page data` hangs → missing dummy env vars in Dockerfile
- ❌ Registry whitelist errors → should be prevented by `--strategy=docker`

**If build fails:** Check logs with `oc logs build/<app-name>-N` and troubleshoot based on error (see Common Issues section).

## Step 5: Tag the Image Stream

After successful build, tag it:

```bash
# Get the image digest from the build
BUILD_NUM=$(oc get builds --sort-by=.metadata.creationTimestamp | grep <app-name> | tail -1 | awk '{print $1}' | cut -d'-' -f3)
IMAGE_DIGEST=$(oc get build/<app-name>-${BUILD_NUM} -o jsonpath='{.status.output.to.imageDigest}')

# Get the registry URL from the build
REGISTRY_URL=$(oc get build/<app-name>-${BUILD_NUM} -o jsonpath='{.status.outputDockerImageReference}' | cut -d'/' -f1)

# Tag it
oc tag ${REGISTRY_URL}/<namespace>/<app-name>@${IMAGE_DIGEST} <app-name>:latest
```

**Explain:** "This creates a stable 'latest' tag pointing to the newly built image."

Verify:
```bash
oc get imagestream <app-name>
```

Should show the image with a tag.

## Step 6: Deploy the Application

```bash
oc new-app <app-name>:latest
```

**This creates:**
- Deployment (manages pods)
- Service (internal networking)

Wait a moment, then check:
```bash
oc get pods -l deployment=<app-name>
```

**If pod is stuck in ContainerCreating/Pending:** Wait a bit longer. If it stays stuck, check events:
```bash
oc describe pod -l deployment=<app-name>
```

## Step 7: Configure Environment Variables

### Set application secrets

Ask: "What's your Azure DevOps Personal Access Token (ADO_PAT)?"

**Security note:** The PAT will be visible in command history. For production, they should use Kubernetes secrets, but for now this is simplest.

```bash
oc set env deployment/<app-name> \
  ADO_PAT=<their-pat>
```

### Set corporate proxy (CRITICAL for external API access)

```bash
oc set env deployment/<app-name> \
  HTTPS_PROXY=http://your-corporate-proxy:80 \
  HTTP_PROXY=http://your-corporate-proxy:80 \
  NO_PROXY=.cluster.local,.svc
```

**Explain:** "Apps inside OpenShift can't reach external APIs (like Azure DevOps) without proxy configuration."

**What happens:** The pod automatically restarts with new environment variables. Monitor:
```bash
oc get pods -l deployment=<app-name> -w
```

Wait until new pod shows `1/1 Running`.

## Step 8: Expose with TLS

```bash
oc create route edge <app-name> --service=<app-name> --port=8080
```

**Explain:** "Edge TLS termination means: external traffic uses HTTPS, OpenShift router handles TLS, and forwards HTTP to your app on port 8080."

Get the URL:
```bash
oc get route <app-name> -o jsonpath='https://{.spec.host}'
```

Show the user: "Your app will be available at: <URL>"

## Step 9: Verify Deployment

### Check pod status
```bash
oc get pods -l deployment=<app-name>
```
Should show: `1/1 Running`

### Check logs
```bash
oc logs deployment/<app-name> --tail=50
```
Should show: "Next.js ready" message

### Test from inside pod
```bash
oc exec deployment/<app-name> -- curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/
```
Should return: `200`

### Test the public route

Ask the user to open the URL in their browser.

**Common issues:**
- "Application not available" → Route might not have TLS configured (we just did this, but verify: `oc describe route <app-name>` should show `TLS Termination: edge`)
- App loads but no data → Proxy not configured (we just did this too, but verify env vars are set)
- 503 error → Pod might not be ready yet, or app crashed (check logs)

## Common Issues & Solutions

### BuildPodEvicted
**Symptom:** Build fails with eviction message
**Solution:** We already set 4Gi, but if it still happens:
```bash
oc patch bc/<app-name> --type=json -p='[{"op":"replace","path":"/spec/resources","value":{"limits":{"memory":"6Gi","cpu":"2"},"requests":{"memory":"3Gi","cpu":"1"}}}]'
```

### Build hangs at "Collecting page data"
**Symptom:** Build runs forever during Next.js build phase
**Solution:** Dockerfile missing dummy env vars. Check builder stage has:
```dockerfile
ENV ADO_PAT=dummy_build_value
```

### "Application not available"
**Symptom:** Route shows "Application is currently not serving requests"
**Solution 1:** Check route has TLS:
```bash
oc describe route <app-name> | grep -i tls
```
If missing, recreate:
```bash
oc delete route <app-name>
oc create route edge <app-name> --service=<app-name> --port=8080
```

**Solution 2:** Check pod is running:
```bash
oc get pods -l deployment=<app-name>
oc logs deployment/<app-name> --tail=50
```

### App loads but no data from external APIs
**Symptom:** UI displays but shows loading indicators
**Solution:** Proxy not configured. Check:
```bash
oc get deployment/<app-name> -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="HTTPS_PROXY")].value}'
```
If empty, set it:
```bash
oc set env deployment/<app-name> \
  HTTPS_PROXY=http://your-corporate-proxy:80 \
  HTTP_PROXY=http://your-corporate-proxy:80
```

### Registry whitelist error
**Symptom:** `registry "docker.io:443" not allowed by whitelist`
**Solution:** Use `--strategy=docker` (we already do this)

## Success!

Once verified, tell the user:
1. ✅ App is deployed and accessible at <URL>
2. ✅ Pod is running with <X> memory/cpu
3. ✅ Environment variables configured (ADO_PAT, proxy)
4. ✅ TLS route exposed

Remind them: "For future updates, use the `openshift-update-app` skill which handles rebuilds quickly."

## Reference Commands

Save these for the user:

```bash
# View all resources
oc get all -l app=<app-name>

# Stream logs
oc logs -f deployment/<app-name>

# Get shell in pod
oc exec -it deployment/<app-name> -- /bin/sh

# Restart deployment (without rebuilding)
oc rollout restart deployment/<app-name>

# Check resource usage
oc adm top pod -l deployment=<app-name>
```
