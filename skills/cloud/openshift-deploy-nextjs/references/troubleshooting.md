<!-- Mirrored between openshift-deploy-nextjs and openshift-update-app (references/troubleshooting.md) — edit both copies. -->

# OpenShift Deployment — Troubleshooting & Reference

## Common Issues

### BuildPodEvicted
**Symptom:** Build fails with eviction message.
**Solution:** Memory too low. Bump it with a merge patch (works whether or not `/spec/resources` is already set):
```bash
oc patch bc/<app-name> --type=merge -p '{"spec":{"resources":{"limits":{"memory":"6Gi","cpu":"2"},"requests":{"memory":"3Gi","cpu":"1"}}}}'
```

### Build hangs at "Collecting page data"
**Symptom:** Build runs forever during the Next.js build phase.
**Solution:** Dockerfile missing dummy env vars in the builder stage. Ensure it has:
```dockerfile
ENV ADO_PAT=dummy_build_value
```

### "Application not available"
**Symptom:** Route shows "Application is currently not serving requests".
**Fix 1 — TLS missing on route:**
```bash
oc describe route <app-name> | grep -i tls
# if missing:
oc delete route <app-name>
oc create route edge <app-name> --service=<app-name> --port=8080
```
**Fix 2 — Pod not ready / crashed:**
```bash
oc get pods -l deployment=<app-name>
oc logs deployment/<app-name> --tail=50
```

### App loads but no data from external APIs
**Symptom:** UI renders but shows loading indicators / empty data.
**Solution:** Corporate proxy not configured.
```bash
oc get deployment/<app-name> -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="HTTPS_PROXY")].value}'
# if empty:
oc set env deployment/<app-name> \
  HTTPS_PROXY=http://your-corporate-proxy:80 \
  HTTP_PROXY=http://your-corporate-proxy:80
```

### Registry whitelist error
**Symptom:** `registry "docker.io:443" not allowed by whitelist`.
**Solution:** Create the build with `--strategy=docker` (the skill does this by default).

## Reference Commands

```bash
# View all resources for the app
oc get all -l app=<app-name>

# Stream logs
oc logs -f deployment/<app-name>

# Shell into the pod
oc exec -it deployment/<app-name> -- /bin/sh

# Restart the deployment without rebuilding
oc rollout restart deployment/<app-name>

# Check resource usage
oc adm top pod -l deployment=<app-name>

# Tag the latest build's image
# Look up the most recent build by its buildconfig label (splitting the build
# name on dashes breaks when the app name itself contains a dash).
BUILD_NAME=$(oc get builds -l buildconfig=<app-name> --sort-by=.metadata.creationTimestamp -o name | tail -1 | cut -d'/' -f2)
IMAGE_DIGEST=$(oc get build/${BUILD_NAME} -o jsonpath='{.status.output.to.imageDigest}')
REGISTRY_URL=$(oc get build/${BUILD_NAME} -o jsonpath='{.status.outputDockerImageReference}' | cut -d'/' -f1)
oc tag ${REGISTRY_URL}/<namespace>/<app-name>@${IMAGE_DIGEST} <app-name>:latest
```
