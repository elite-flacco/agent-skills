---
name: openshift-update-app
description: Use when the user wants to deploy code changes to an app already running on OpenShift, or rebuild/redeploy an existing deployment — e.g. "redeploy", "update my app", "rebuild", "deploy changes to openshift". Also use when troubleshooting issues with an existing OpenShift deployment.
---

# Update OpenShift Next.js App

Quickly rebuild and redeploy an existing Next.js application on OpenShift when code changes.

## When to Read What

- **Always follow** — the workflow below.
- **Read on errors** — `references/troubleshooting.md` (BuildPodEvicted, build hangs, route/proxy/pod issues, image-tagging commands). Those commands apply identically to updates.

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

Takes 5–10 minutes for Next.js apps (npm install is slow). Watch for `Successfully pushed` (success) or failure signals like `BuildPodEvicted`, build hangs at "Collecting page data", or `npm ERR!`. On failure, see `references/troubleshooting.md` for fixes (memory limits, dummy env vars, code errors).

## Step 4: Tag the New Image

After a successful build, tag the latest build's image digest as `:latest` so the deployment picks it up. The full tagging commands (extract build number → digest → `oc tag`) are in `references/troubleshooting.md` under "Reference Commands".

The deployment automatically rolls out once `:latest` moves.

## Step 5: Watch the Rollout

```bash
oc get pods -l deployment=<app-name> -w
```

Press Ctrl+C when the new pod is `1/1 Running`. Expected sequence: old pod keeps running → new pod starts (ContainerCreating → Running) → old pod terminates.

If the new pod fails to start, check `oc logs deployment/<app-name> --tail=50` and see `references/troubleshooting.md` for diagnosis (app crashes, missing env vars, resource limits).

## Step 6: Verify the Update

```bash
# Verify new pod is running
oc get pods -l deployment=<app-name>

# Check recent logs
oc logs deployment/<app-name> --tail=20
```

Get the route URL and ask the user to open it and confirm the changes are there:

```bash
oc get route <app-name> -o jsonpath='https://{.spec.host}\n'
```

If old code still shows (hard refresh / `oc rollout restart`), the app won't load (pod/route/TLS), or API calls fail (proxy/PAT), see `references/troubleshooting.md`.

## Success!

Tell the user:
- ✅ Build completed: build #<N>
- ✅ Image tagged as latest
- ✅ Rollout complete
- ✅ New pod running: <pod-name>
- ✅ App accessible at: <URL>

## Update-Specific Config Changes

Two config changes that don't require a full redeploy:

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
