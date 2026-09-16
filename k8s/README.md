# AspireOS — Kubernetes Deployment Guide

This turns the existing `docker-compose.yml` (local dev) into a production
Kubernetes deployment, with CI/CD in `.github/workflows/ci-cd.yml`.

## What changed vs. local Docker Compose

- `backend/Dockerfile` now runs as a non-root user.
- `frontend/Dockerfile` now accepts `VITE_API_URL` as a build arg (default
  `/api/v1`, a relative path) so the built JS calls the API on the same host
  the frontend is served from — no CORS/hardcoded-domain issues.
- Postgres and Redis, which docker-compose ran as sidecar containers, become
  a `StatefulSet` (Postgres, for its persistent volume) and a `Deployment`
  (Redis) in `k8s/`.
- One `Ingress` fronts both services: `/api/*` → backend, everything else →
  frontend.

## One-time setup

1. **Container registry** — push images somewhere the cluster can pull from
   (Utho Container Registry, GHCR, Docker Hub, etc). Update the image names
   in `k8s/backend.yaml`, `k8s/frontend.yaml`, `k8s/kustomization.yaml`, and
   `REGISTRY`/`IMAGE_NAMESPACE` in `.github/workflows/ci-cd.yml`.

2. **Domain** — replace `aspireos.example.com` in `k8s/ingress.yaml` with
   your real domain, and update `CORS_ORIGINS` in `k8s/configmap.yaml` to
   match (`https://yourdomain.com`).

3. **Ingress controller + TLS** — the cluster needs an ingress controller
   (e.g. `ingress-nginx`) and, if you want automatic TLS, `cert-manager`
   with a `ClusterIssuer` named `letsencrypt-prod`. If you don't use
   cert-manager, delete that annotation and the `tls:` block and terminate
   TLS elsewhere (e.g. a Utho Load Balancer).

4. **Secrets** — never commit real secrets. Create them directly in the
   cluster:

   ```bash
   kubectl create namespace aspireos
   kubectl create secret generic aspireos-secrets -n aspireos \
     --from-literal=SECRET_KEY="$(openssl rand -hex 32)" \
     --from-literal=POSTGRES_PASSWORD="<strong-random-password>" \
     --from-literal=DATABASE_URL="postgresql+psycopg://aspireos:<same-password>@postgres:5432/aspireos"
   ```

   (`k8s/secret.example.yaml` is a template/reference only — it's excluded
   from `kustomization.yaml` on purpose.)

5. **Registry pull secret** (if your registry is private):

   ```bash
   kubectl create secret docker-registry regcred -n aspireos \
     --docker-server=<registry-url> \
     --docker-username=<user> \
     --docker-password=<token>
   ```

   Then add `imagePullSecrets: [{name: regcred}]` under `spec.template.spec`
   in `k8s/backend.yaml` and `k8s/frontend.yaml`.

## Deploy manually (first time / debugging)

```bash
# build & push
docker build -t <registry>/<ns>/aspireos-backend:v1 ./backend
docker build -t <registry>/<ns>/aspireos-frontend:v1 --build-arg VITE_API_URL=/api/v1 ./frontend
docker push <registry>/<ns>/aspireos-backend:v1
docker push <registry>/<ns>/aspireos-frontend:v1

# point manifests at that tag and apply
cd k8s
kustomize edit set image \
  <registry>/<ns>/aspireos-backend=<registry>/<ns>/aspireos-backend:v1 \
  <registry>/<ns>/aspireos-frontend=<registry>/<ns>/aspireos-frontend:v1
kubectl apply -k .

kubectl -n aspireos get pods -w
```

## CI/CD (automatic, on push to `main`)

`.github/workflows/ci-cd.yml` runs backend tests, builds & pushes both
images tagged with the commit SHA, then applies the manifests and waits for
rollout. It needs these GitHub Actions secrets:

| Secret               | Value                                                        |
| --------------------- | ------------------------------------------------------------ |
| `REGISTRY_USERNAME`   | Registry login username / robot account                      |
| `REGISTRY_PASSWORD`   | Registry login password / token                               |
| `KUBE_CONFIG_B64`     | `cat ~/.kube/config \| base64 -w0` for a cluster-scoped or namespace-scoped service account with access to `aspireos` |

## Local dev is unaffected

`docker compose up --build` still works exactly as before — none of this
touches `docker-compose.yml`.
