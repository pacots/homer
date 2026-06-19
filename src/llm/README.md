# Ollama Kubernetes Deployment

## Overview

This directory contains Kubernetes manifests for deploying Ollama, an open-source LLM (Large Language Model) inference server, on a Kubernetes cluster.

## What's in the YAML

The `ollama.yaml` file defines the following Kubernetes resources:

### Namespace
- **ollama**: A dedicated namespace to isolate Ollama resources

### PersistentVolumeClaim
- **ollama-data**: A persistent storage volume (10Gi) for storing downloaded models and cache data
  - Mounted at `/root/.ollama` in the container

### Deployment
- **ollama**: Runs the Ollama inference server
  - Image: `ollama/ollama:latest`
  - Port: `11434` (internal)
  - Environment: `OLLAMA_HOST=0.0.0.0:11434`
  - Resource Requests: 2Gi RAM, 1 CPU
  - Resource Limits: 6Gi RAM, 3 CPUs

### Service
- **ollama**: Exposes the deployment via NodePort
  - Service Port: 11434
  - Node Port: 31434 (accessible from external machines)
  - Type: NodePort

## Deployment

Deploy Ollama to your Kubernetes cluster:

```bash
kubectl apply -f <path-to-yaml>/ollama.yaml
```

Verify the deployment:

```bash
kubectl get pods -n ollama
kubectl get svc -n ollama
```

## Downloading Models

Before making the first request to Ollama, you need to download a model. Use the following command (replace `<local-ip>` with your node's IP or localhost if accessing from the same machine):

```bash
curl http://<local-ip>:31434/api/pull -d '{"name":"tinyllama"}'
```

### Available Models
Common models to pull:
- `tinyllama` - Lightweight model (~1Gb)
- `llama2` - Larger model (~4Gb)
- `mistral` - Fast and efficient (~4Gb)
- `neural-chat` - Conversation optimized (~4Gb)

## API Endpoints

Once the model is downloaded, you can interact with Ollama:

### Generate Completions
```bash
curl http://<local-ip>:31434/api/generate -d '{
  "model": "tinyllama",
  "prompt": "Why is the sky blue?"
}'
```

### Pull Additional Models
```bash
curl http://<local-ip>:31434/api/pull -d '{"name":"llama2"}'
```

## Troubleshooting

- Check pod logs: `kubectl logs -n ollama deployment/ollama`
- Verify service connectivity: `kubectl port-forward -n ollama svc/ollama 11434:11434`
- Ensure sufficient disk space for model storage (default: 10Gi PVC)
