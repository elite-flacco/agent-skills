---
name: openshift-deploy-nextjs
description: Use when the user wants to deploy a new Next.js app to OpenShift / OCP from scratch — e.g. "deploy to openshift", "ocp deployment", "get my Next.js app running on OpenShift", or needs help with OpenShift builds. Also use when troubleshooting fresh deployment issues like BuildPodEvicted, route problems, or proxy configuration.
---

# Deploy Next.js to OpenShift

Guide the user through deploying a Next.js app to OpenShift from preparation to verification.

## When to Read What

- **Always follow** — the workflow below.
- **Copy directly** — `templates/Dockerfile` (multi-stage Next.js standalone build with dummy env vars).
- **Read on errors** — `references/troubleshooting.md` (BuildPodEvicted, build hangs, route/proxy issues, image tagging commands).

## Important Context

- Namespace = Project (interchangeable terms).
- Corporate proxy is usually required for external API access.
- TLS edge termination is required for external routes.
- Next.js builds need **4Gi memory** (TypeScript checking is intensive) — set this upfront or builds get evicted.
- **Dummy env vars** are needed at build time so Next.js pre-rendering doesn't hang; real values are injected at runtime.

## Step 1 — Prerequisites

```bash
oc whoami        # logged in?
oc project       # current project
oc get projects  # available projects
```
Confirm: logged in, target namespace chosen, and you're in the Next.js app root (see `package.json`, `app/`). Ask the user for anything missing.

## Step 2 — Prepare the App

- **`next.config.ts`** must have `output: 'standalone'`. Add it if missing (needed for the optimized Docker image).
- **Dockerfile** must be a multi-stage build (deps → builder → runtime) with dummy env vars in the builder stage and standalone output copied to runtime. Use `templates/Dockerfile` if none exists or the existing one is incomplete.

## Step 3 — OpenShift Config (optional)

Ask if they want `ocp-onboard` to generate Helm charts / pipeline. If yes:
```bash
ocp-onboard --add-service apps/<app-name>
```
Prompts: Continue → `y`, Language → `4` (Nodejs), Namespace → theirs. Note: the automated pipeline needs Quay permissions; manual deploy below is simpler.

## Step 4 — Build the Image

```bash
oc project <namespace>
oc new-build --binary --name=<app-name> --strategy=docker

# CRITICAL: Next.js builds need 4Gi — set this before building
oc patch bc/<app-name> --type=json -p='[
  {"op":"add","path":"/spec/resources","value":{"limits":{"memory":"4Gi","cpu":"2"},"requests":{"memory":"2Gi","cpu":"1"}}}
]'

oc start-build <app-name> --from-dir=. --follow
```
Takes 5–10 min. Watch for `Successfully pushed`. On failure, read `references/troubleshooting.md`.

## Step 5 — Tag the Image Stream

```bash
oc get imagestream <app-name>   # confirm image present
```
The tagging commands (extract latest build digest → tag as `:latest`) are in `references/troubleshooting.md` under "Reference Commands".

## Step 6 — Deploy

```bash
oc new-app <app-name>:latest    # creates Deployment + Service
oc get pods -l deployment=<app-name>
```
If pods stick in Pending/ContainerCreating, check `oc describe pod -l deployment=<app-name>`.

## Step 7 — Environment Variables

```bash
# App secret (ask user for their ADO_PAT — note: visible in history; use K8s secrets for prod)
oc set env deployment/<app-name> ADO_PAT=<pat>

# Corporate proxy (CRITICAL for external API access)
oc set env deployment/<app-name> \
  HTTPS_PROXY=http://your-corporate-proxy:80 \
  HTTP_PROXY=http://your-corporate-proxy:80 \
  NO_PROXY=.cluster.local,.svc
```
Pod restarts automatically; wait for `1/1 Running`.

## Step 8 — Expose with TLS

```bash
oc create route edge <app-name> --service=<app-name> --port=8080
oc get route <app-name> -o jsonpath='https://{.spec.host}'$'\n'
```
Edge TLS = HTTPS externally, router handles TLS, forwards HTTP to the app on 8080.

## Step 9 — Verify

```bash
oc get pods -l deployment=<app-name>                 # 1/1 Running
oc logs deployment/<app-name> --tail=50              # "Next.js ready"
oc exec deployment/<app-name> -- curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/  # 200
```
Then ask the user to open the URL in a browser. For any issue, see `references/troubleshooting.md`.

## Done

Confirm to the user: app URL, pod running, env vars configured, TLS route exposed. For future rebuilds, point them to the `openshift-update-app` skill.
