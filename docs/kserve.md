# KServe Installation (Helm)

KServe provides Kubernetes-native model serving. It requires **cert-manager** and **Knative** (or can run in RawDeployment mode without Knative).

## Prerequisites

- Kubernetes cluster (v1.27+)
- `kubectl` and `helm` installed and configured

## 1. Install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.15.0 \
  --set crds.enabled=true

# Verify
kubectl get pods -n cert-manager
```

## 2. Install Cert Manager
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
```

## 3. Install KServe

KServe v0.17+ restructured Helm charts — there is no longer a Helm repo URL. Charts are published as GitHub release assets and must be installed directly.

# Install KServe CRDs
```
kubectl create namespace kserve

helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
  --version v0.16.0 \
  -n kserve \
  --wait
```

# Install KServe controller
```
helm install kserve oci://ghcr.io/kserve/charts/kserve \
  --version v0.16.0 \
  -n kserve \
  --set kserve.controller.deploymentMode=RawDeployment \
  --wait

```

> For RawDeployment (no Knative), add `--set kserve.controller.deploymentMode=RawDeployment` to the `kserve-resources` install step.

## 4. Verify Installation

```bash
kubectl get pods -n kserve
kubectl get clusterservingruntimes
```

## 6. AWS Credentials Secret

Edit `k8s/aws-secret.yaml` and replace the placeholder values with your real credentials, then apply:

```bash
kubectl apply -f k8s/aws-secret.yaml
```

> **Note:** `k8s/aws-secret.yaml` is git-ignored and must never be committed with real credentials. For production, use Sealed Secrets (see step 6a below) or IRSA.

## 6a. Sealed Secrets (production — safe to commit)

Sealed Secrets encrypts `aws-secret.yaml` using a cluster-side certificate. The encrypted file (`aws-secret-sealed.yaml`) can be safely committed to Git — only the cluster can decrypt it.

### Install the Sealed Secrets controller

```bash
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm repo update

helm install sealed-secrets sealed-secrets/sealed-secrets \
  --namespace kube-system \
  --version 2.16.0
```

### Install the kubeseal CLI

```bash
# macOS
brew install kubeseal

# Linux
curl -Lo kubeseal.tar.gz https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.27.0/kubeseal-0.27.0-linux-amd64.tar.gz
tar -xzf kubeseal.tar.gz kubeseal
sudo install -m 755 kubeseal /usr/local/bin/kubeseal
```

### Seal the secret

Fill in your real credentials in `k8s/aws-secret.yaml`, then seal it:

```bash
kubeseal --format yaml < k8s/aws-secret.yaml > k8s/aws-secret-sealed.yaml
```

`k8s/aws-secret-sealed.yaml` is now safe to commit. Apply it to the cluster:

```bash
kubectl apply -f k8s/aws-secret-sealed.yaml

# Verify the secret was created
kubectl get secret aws-credentials -n kserve
```

### Rotate credentials

If credentials change, update `k8s/aws-secret.yaml` with the new values, re-seal, commit, and re-apply:

```bash
kubeseal --format yaml < k8s/aws-secret.yaml > k8s/aws-secret-sealed.yaml
git add k8s/aws-secret-sealed.yaml
git commit -m "Rotate AWS credentials"
kubectl apply -f k8s/aws-secret-sealed.yaml
```

## 7. Service Account

Create a service account that references the AWS secret so KServe pods can pull the model from S3:

```bash
kubectl apply -f k8s/service-account.yaml
```

Verify:

```bash
kubectl get serviceaccount kserve-s3-sa -n kserve
```

## 8. Deploy the InferenceService

Update the `storageUri` in `k8s/inference-service.yaml` with your S3 bucket path, then apply:

```bash
kubectl apply -f k8s/inference-service.yaml
```

Check the deployment status:

```bash
kubectl get inferenceservice churn-model -n kserve
kubectl describe inferenceservice churn-model -n kserve
```

Wait until `READY` is `True`:

```
NAME          URL                                              READY
churn-model   http://churn-model.kserve.example.com/v1/...   True
```

## 9. Run a Test Prediction

```bash
# Get the ingress host
INGRESS_HOST=$(kubectl get svc kourier -n kourier-system -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

curl -X POST http://${INGRESS_HOST}/v1/models/churn-model:predict \
  -H "Content-Type: application/json" \
  -H "Host: churn-model.kserve.example.com" \
  -d '{
    "instances": [[34, 4, 22.0, 88.0, 3, 0, 5.5, 1, 0, 0]]
  }'
```
