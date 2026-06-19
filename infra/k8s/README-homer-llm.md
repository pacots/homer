# Homer LLM Kubernetes Deployment

This manifest deploys the Homer LLM service using Ollama, an open-source LLM inference server.

For full infrastructure setup, cluster creation, teardown, and local `kind` instructions, see:

```text
../README.md
```

## Manifest

The service is defined in:

```text
infra/k8s/homer-llm.yaml
```

## What It Deploys

The `homer-llm.yaml` manifest defines the following Kubernetes resources.

### Namespace

- **homer**: Shared namespace for Homer application resources.

### PersistentVolumeClaim

- **homer-llm-data**: Persistent storage for downloaded Ollama models and cache data.
  - Size: `10Gi`
  - Mounted at `/root/.ollama` inside the container.

### Deployment

- **homer-llm**: Runs the Ollama inference server.
  - Image: `ollama/ollama:latest`
  - Container port: `11434`
  - Environment: `OLLAMA_HOST=0.0.0.0:11434`
  - Resource requests:
    - Memory: `2Gi`
    - CPU: `1`
  - Resource limits:
    - Memory: `6Gi`
    - CPU: `3`

### Service

- **homer-llm**: Exposes the Ollama deployment through a NodePort service.
  - Type: `NodePort`
  - Service port: `11434`
  - Target port: `11434`
  - Node port: `31434`

## Access URLs

### Inside Kubernetes

Other services running inside the same Kubernetes cluster should use the internal service name:

```text
http://homer-llm:11434
```

Example environment variable for the future Homer agent:

```env
OLLAMA_BASE_URL=http://homer-llm:11434
```

### Local kind

When running locally with `kind`, use:

```text
http://localhost:31434
```

Example:

```bash
curl http://localhost:31434/api/tags
```

### Raspberry Pi k3s

When running on the Raspberry Pi with `k3s`, use the Raspberry Pi IP address and the NodePort:

```text
http://<raspberry-ip>:31434
```

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

## Download Models

Before making the first request to Ollama, download a model.

### Local kind

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

### Raspberry Pi k3s

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

## Available Models

Common models to pull:

- `tinyllama` - Lightweight model, useful for testing.
- `llama3.2:1b` - Small Llama 3.2 model.
- `llama3.2:3b` - Recommended local development model.
- `mistral` - Larger model, requires more resources.
- `phi3:mini` - Lightweight model with good reasoning capabilities.

For resource-constrained devices such as Raspberry Pi, start with:

```text
tinyllama
```

or:

```text
llama3.2:1b
```

For local development on a machine with more RAM, use:

```text
llama3.2:3b
```

## API Endpoints

### List installed models

Local kind:

```bash
curl http://localhost:31434/api/tags
```

Raspberry Pi k3s:

```bash
curl http://<raspberry-ip>:31434/api/tags
```

### Generate completions

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

### Pull additional models

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

## Restart

Restart the LLM deployment:

```bash
kubectl rollout restart deployment/homer-llm -n homer
```

Watch the rollout:

```bash
kubectl rollout status deployment/homer-llm -n homer
```

## Logs

Check Ollama logs:

```bash
kubectl logs -n homer deployment/homer-llm
```

Follow logs:

```bash
kubectl logs -n homer deployment/homer-llm -f
```

## Port Forward Fallback

If NodePort access is not working, use port-forwarding:

```bash
kubectl port-forward -n homer svc/homer-llm 11434:11434
```

Then test from another terminal:

```bash
curl http://localhost:11434/api/tags
```

## Test From Inside the Cluster

Run a temporary curl pod:

```bash
kubectl run curl-test -n homer --rm -it --image=curlimages/curl -- sh
```

Inside the temporary pod:

```sh
curl http://homer-llm:11434/api/tags
```

## Storage Notes

Downloaded Ollama models are stored in the PersistentVolumeClaim:

```text
homer-llm-data
```

Mounted inside the container at:

```text
/root/.ollama
```

The default requested storage is:

```text
10Gi
```

If the PVC is deleted, downloaded models will be lost and must be pulled again.

## Delete

Delete only the LLM service:

```bash
kubectl delete -f infra/k8s/homer-llm.yaml
```

For full infrastructure cleanup, see:

```text
../README.md
```