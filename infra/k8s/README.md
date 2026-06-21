# Homer LLM Kubernetes Deployment

This directory contains Kubernetes manifests for deploying Homer LLM services using Ollama and Open WebUI.

For full infrastructure setup, cluster creation, teardown, and local `kind` instructions, see:

```text
../README.md
```

## Table of Contents

- [Manifests](#manifests)
  - [homer-namespace.yaml](#homer-namespaceyaml)
  - [homer-llm.yaml](#homer-llmyaml)
  - [homer-openweb-ui.yaml](#homer-openweb-uiyaml)
- [Deployment](#deployment)
  - [Deploy All Services](#deploy-all-services)
  - [Deploy Individual Services](#deploy-individual-services)
  - [Verify Deployment](#verify-deployment)
  - [Logs](#logs)
  - [Restart Services](#restart-services)
- [Access URLs](#access-urls)
  - [Inside Kubernetes](#inside-kubernetes)
  - [Local kind](#local-kind)
  - [Raspberry Pi k3s](#raspberry-pi-k3s)
- [Model Management](#model-management)
  - [Download Models](#download-models)
  - [Available Models](#available-models)
  - [API Endpoints](#api-endpoints)
- [Storage & Cleanup](#storage--cleanup)
  - [Storage Notes](#storage-notes)
  - [Port Forwarding (Fallback)](#port-forwarding-fallback)
  - [Testing From Inside the Cluster](#testing-from-inside-the-cluster)
  - [Delete Services](#delete-services)

## Manifests

### homer-namespace.yaml

Creates the `homer` namespace, which is the shared namespace for all Homer application resources.

- **Namespace**: `homer`

### homer-llm.yaml

Deploys the Ollama LLM inference server with persistent model storage.

**Resources:**

- **PersistentVolumeClaim** (`homer-llm-data`)
  - Persistent storage for downloaded Ollama models and cache data
  - Size: `10Gi`
  - Mounted at `/root/.ollama` inside the container

- **Deployment** (`homer-llm`)
  - Runs the Ollama inference server
  - Image: `ollama/ollama:latest`
  - Container port: `11434`
  - Environment: `OLLAMA_HOST=0.0.0.0:11434`
  - Resource requests: Memory `2Gi`, CPU `1`
  - Resource limits: Memory `6Gi`, CPU `3`

- **Service** (`homer-llm`)
  - Type: `NodePort`
  - Service port: `11434`
  - Target port: `11434`
  - Node port: `31434`

### homer-openweb-ui.yaml

Deploys Open WebUI, a web-based interface for interacting with Ollama models.

**Resources:**

- **Deployment** (`homer-open-webui`)
  - Runs the Open WebUI interface
  - Image: `ghcr.io/open-webui/open-webui:main`
  - Container port: `8080`
  - Environment variables:
    - `OLLAMA_BASE_URL=http://homer-llm:11434` (connects to Ollama service)
    - `WEBUI_AUTH=false` (disables authentication for local development)
  - Resource requests: Memory `2Gi`, CPU `1`
  - Resource limits: Memory `3Gi`, CPU `2`

- **Service** (`homer-open-webui`)
  - Type: `NodePort`
  - Service port: `80`
  - Target port: `8080`
  - Node port: `30080`

## Deployment

### Deploy All Services

Deploy the complete Homer stack (namespace, Ollama, and Open WebUI):

```bash
kubectl apply -f infra/k8s/homer-namespace.yaml
kubectl apply -f infra/k8s/homer-llm.yaml
kubectl apply -f infra/k8s/homer-openweb-ui.yaml
```

Or deploy all at once:

```bash
kubectl apply -f infra/k8s/
```

### Deploy Individual Services

Deploy only the namespace:

```bash
kubectl apply -f infra/k8s/homer-namespace.yaml
```

Deploy only the LLM service:

```bash
kubectl apply -f infra/k8s/homer-llm.yaml
```

Deploy only the Open WebUI:

```bash
kubectl apply -f infra/k8s/homer-openweb-ui.yaml
```

### Verify Deployment

Check pod status:

```bash
kubectl get pods -n homer
```

Check services:

```bash
kubectl get svc -n homer
```

Check persistent volume claims:

```bash
kubectl get pvc -n homer
```

Watch pods until running:

```bash
kubectl get pods -n homer -w
```

### Logs

Check Ollama logs:

```bash
kubectl logs -n homer deployment/homer-llm
```

Check Open WebUI logs:

```bash
kubectl logs -n homer deployment/homer-open-webui
```

Follow logs in real-time:

```bash
kubectl logs -n homer deployment/homer-llm -f
kubectl logs -n homer deployment/homer-open-webui -f
```

### Restart Services

Restart the Ollama deployment:

```bash
kubectl rollout restart deployment/homer-llm -n homer
```

Restart Open WebUI:

```bash
kubectl rollout restart deployment/homer-open-webui -n homer
```

Watch rollout status:

```bash
kubectl rollout status deployment/homer-llm -n homer
kubectl rollout status deployment/homer-open-webui -n homer
```

## Access URLs

### Inside Kubernetes

Other services running inside the same Kubernetes cluster should use the internal service names:

- **Ollama**: `http://homer-llm:11434`
- **Open WebUI**: `http://homer-open-webui`

Example environment variables:

```env
OLLAMA_BASE_URL=http://homer-llm:11434
OPEN_WEBUI_URL=http://homer-open-webui
```

### Local kind

When running locally with `kind`:

- **Ollama**: `http://localhost:31434`
- **Open WebUI**: `http://localhost:30080`

Test Ollama:

```bash
curl http://localhost:31434/api/tags
```

Access Open WebUI in browser: http://localhost:30080

### Raspberry Pi k3s

When running on the Raspberry Pi with `k3s`, use the Raspberry Pi IP address and the NodePort:

- **Ollama**: `http://<raspberry-ip>:31434`
- **Open WebUI**: `http://<raspberry-ip>:30080`

Example:

```bash
curl http://192.168.1.50:31434/api/tags
```

Replace `192.168.1.50` with the actual Raspberry Pi IP address.

## Deploy

Deploy only the LLM service:

```bash
kubectl apply -f infra/k8s/homer-llm.yaml
```

Verify:

```bash
kubectl get pods -n homer
kubectl get svc -n homer
kubectl get pvc -n homer
```

Watch the pod until it is running:

```bash
kubectl get pods -n homer -w
```

## Model Management

### Download Models

Before making the first request to Ollama, download a model.

#### Local kind

Recommended model for local development:

```bash
curl http://localhost:31434/api/pull \
  -d '{"name":"llama3.2:3b"}'
```

Small test model:

```bash
curl http://localhost:31434/api/pull \
  -d '{"name":"tinyllama"}'
```

#### Raspberry Pi k3s

Recommended small model:

```bash
curl http://<raspberry-ip>:31434/api/pull \
  -d '{"name":"tinyllama"}'
```

Alternative lightweight model:

```bash
curl http://<raspberry-ip>:31434/api/pull \
  -d '{"name":"llama3.2:1b"}'
```

### Available Models

Common models to pull:

- `tinyllama` - Lightweight model, useful for testing.
- `llama3.2:1b` - Small Llama 3.2 model.
- `llama3.2:3b` - Recommended local development model.
- `mistral` - Larger model, requires more resources.
- `phi3:mini` - Lightweight model with good reasoning capabilities.

For resource-constrained devices such as Raspberry Pi, start with `tinyllama` or `llama3.2:1b`.

For local development on a machine with more RAM, use `llama3.2:3b`.

### API Endpoints

#### List installed models

Local kind:

```bash
curl http://localhost:31434/api/tags
```

Raspberry Pi k3s:

```bash
curl http://<raspberry-ip>:31434/api/tags
```

#### Generate completions

Local kind:

```bash
curl -N http://localhost:31434/api/generate \
  -d '{
    "model": "llama3.2:3b",
    "prompt": "Why is the sky blue?"
  }'
```

Raspberry Pi k3s:

```bash
curl -N http://<raspberry-ip>:31434/api/generate \
  -d '{
    "model": "tinyllama",
    "prompt": "Why is the sky blue?"
  }'
```

#### Pull additional models

Local kind:

```bash
curl http://localhost:31434/api/pull \
  -d '{"name":"llama3.2:1b"}'
```

Raspberry Pi k3s:

```bash
curl http://<raspberry-ip>:31434/api/pull \
  -d '{"name":"llama3.2:1b"}'
```

## Storage & Cleanup

### Storage Notes

Downloaded Ollama models are stored in the PersistentVolumeClaim:

```text
homer-llm-data
```

Mounted inside the container at:

```text
/root/.ollama
```

The default requested storage is `10Gi`. If the PVC is deleted, downloaded models will be lost and must be pulled again.

### Port Forwarding (Fallback)

If NodePort access is not working, use port-forwarding as a fallback:

```bash
kubectl port-forward -n homer svc/homer-llm 11434:11434
kubectl port-forward -n homer svc/homer-open-webui 8080:8080
```

Then test from another terminal:

```bash
curl http://localhost:11434/api/tags
```

Access Open WebUI: http://localhost:8080

### Testing From Inside the Cluster

Run a temporary curl pod to test connectivity:

```bash
kubectl run curl-test -n homer --rm -it --image=curlimages/curl -- sh
```

Inside the temporary pod:

```sh
curl http://homer-llm:11434/api/tags
curl http://homer-open-webui
```

### Delete Services

Delete only the Open WebUI:

```bash
kubectl delete -f infra/k8s/homer-openweb-ui.yaml
```

Delete only the LLM service:

```bash
kubectl delete -f infra/k8s/homer-llm.yaml
```

Delete only the namespace (will delete all resources in it):

```bash
kubectl delete -f infra/k8s/homer-namespace.yaml
```

Delete all Homer services:

```bash
kubectl delete -f infra/k8s/
```

For full infrastructure cleanup, see:

```text
../README.md
```