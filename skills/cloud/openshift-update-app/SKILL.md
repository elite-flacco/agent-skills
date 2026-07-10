---
name: openshift-update-app
description: Use when the user wants to deploy code changes to an app already running on OpenShift, or rebuild/redeploy an existing deployment — e.g. "redeploy", "update my app", "rebuild", "deploy changes to openshift". Also use when troubleshooting issues with an existing OpenShift deployment.
---

# Update OpenShift Next.js App

Quickly rebuild and redeploy an existing Next.js application on OpenShift when code changes.

## Overview

This skill handles:
1. Prerequisites verification (logged in, correct directory)
2. Rebuilding the image in OpenShift
3. Tagging the new image
4. Waiting for automatic rollout
5. Verifying the update
6. Quick troubleshooting if needed

## Step 1: Prerequisites Check

Verify basics before starting:

```bash
# Check OpenShift login
oc whoami

# Check current project
oc project

# Verify in app directory
pwd
ls -la package.json Dockerfile
```

**Ask the user:**
- Which app are you updating? (get the app name)
- Are you in the app's root directory? (should see package.json, Dockerfile)
- Which project/namespace is it deployed in? (if not already in correct project)

If they need to switch projects:
```bash
oc project <namespace>
```

## Step 2: Verify Existing Deployment

Check the app exists:
```bash
# Check deployment exists
oc get deployment <app-name>

# Check current pod status
oc get pods -l deployment=<app-name>

# Check current build configs
oc get bc | grep <app-name>
```

If deployment doesn't exist, tell them: "This app hasn't been deployed yet. Use the `openshift-deploy-nextjs` skill for new deployments."

If build config doesn't exist, tell them: "No build configuration found. You'll need to do a full deployment using `openshift-deploy-nextjs`."

## Step 3: Rebuild the Image

Start a new build from the current directory:

```bash
oc start-build <app-name> --from-dir=. --follow
```

**Tell the user:** "Building... This takes 5-10 minutes for Next.js apps (npm install is slow)."

Monitor the build logs. Watch for:
- ✅ `Successfully pushed` → build succeeded
- ❌ `BuildPodEvicted` → memory issue, may need to increase limits
- ❌ Build hangs at "Collecting page data" → Dockerfile missing dummy env vars
- ❌ `npm ERR!` → dependency or code issue in the app

**If build fails:**
1. Check the error in the logs
2. Common fixes:
   - BuildPodEvicted: `oc patch bc/<app-name> --type=json -p='[{"op":"replace","path":"/spec/resources","value":{"limits":{"memory":"6Gi","cpu":"2"},"requests":{"memory":"3Gi","cpu":"1"}}}]'`
   - Missing dummy env vars: Check Dockerfile builder stage has `ENV ADO_PAT=dummy_build_value`
   - Code errors: Fix the code and rebuild

## Step 4: Tag the New Image

After successful build:

```bash
# Get the latest build number and image digest
BUILD_NUM=$(oc get builds --sort-by=.metadata.creationTimestamp | grep <app-name> | tail -1 | awk '{print $1}' | cut -d'-' -f3)
NEW_DIGEST=$(oc get build/<app-name>-${BUILD_NUM} -o jsonpath='{.status.output.to.imageDigest}')
REGISTRY_URL=$(oc get build/<app-name>-${BUILD_NUM} -o jsonpath='{.status.outputDockerImageReference}' | cut -d'/' -f1)

# Tag it as latest
oc tag ${REGISTRY_URL}/<namespace>/<app-name>@${NEW_DIGEST} <app-name>:latest
```

**Explain:** "This updates the 'latest' tag to point to your new build. The deployment will automatically roll out."

## Step 5: Watch the Rollout

The deployment automatically picks up the new image and rolls out:

```bash
oc get pods -l deployment=<app-name> -w
```

**Tell the user:** "Watching pods update... Press Ctrl+C when you see the new pod Running."

What to expect:
1. Old pod keeps running
2. New pod starts (ContainerCreating → Running)
3. Once new pod is ready, old pod terminates
4. Should see: `<app-name>-<new-hash>  1/1  Running`

**If new pod fails:**
- Check why: `oc logs deployment/<app-name> --tail=50`
- Common issues:
  - App crashes on startup → code issue, check logs
  - Environment variables missing → unlikely if this was working before
  - Memory/CPU limits too low → increase if needed

## Step 6: Verify the Update

### Quick checks:
```bash
# Verify new pod is running
oc get pods -l deployment=<app-name>

# Check recent logs
oc logs deployment/<app-name> --tail=20
```

Should see Next.js startup message.

### Test the app:
```bash
# Get the route URL
oc get route <app-name> -o jsonpath='https://{.spec.host}'
```

Ask the user: "Can you open <URL> in your browser and verify the changes are there?"

**Common issues:**

**Old code still showing:**
- Hard refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- Check pod started recently: `oc get pods -l deployment=<app-name>` (AGE should be < few minutes)
- If pod is old, rollout might not have happened:
  ```bash
  oc rollout status deployment/<app-name>
  oc rollout restart deployment/<app-name>  # Force restart if needed
  ```

**App not loading:**
- Check pod is Running: `oc get pods -l deployment=<app-name>`
- Check logs for errors: `oc logs deployment/<app-name>`
- Check route: `oc describe route <app-name>` (should show TLS: edge, Endpoints: <pod-ip>)

**Data not loading (API calls failing):**
- Usually means proxy not configured or PAT expired
- Check env vars: `oc get deployment/<app-name> -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="HTTPS_PROXY")]}'`
- Verify PAT: `oc get deployment/<app-name> -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="ADO_PAT")].value}'`

## Success!

Tell the user:
- ✅ Build completed: build #<N>
- ✅ Image tagged as latest
- ✅ Rollout complete
- ✅ New pod running: <pod-name>
- ✅ App accessible at: <URL>

## Troubleshooting

For rollback, force restart, deployment history, scaling, and diagnosing app-not-loading / proxy / TLS issues, see the shared reference in the `openshift-deploy-nextjs` skill: `references/troubleshooting.md`. Those commands (e.g. `oc rollout undo`, `oc rollout restart`, `oc get all -l app=...`) apply identically here.

Two update-specific config changes that don't require a full redeploy:

**Environment variables changed:**
```bash
oc set env deployment/<app-name> NEW_VAR=value
# Pod automatically restarts
```

**Memory/CPU limits changed:**
```bash
oc set resources deployment/<app-name> --limits=cpu=2,memory=1Gi --requests=cpu=500m,memory=512Mi
```

**Major changes (Dockerfile, build strategy, etc.):**
- Use the `openshift-deploy-nextjs` skill to redo the full deployment, or
- Manually delete and recreate: `oc delete all -l app=<app-name>` then redeploy
