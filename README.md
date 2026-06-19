# homer
Homer is an AI-powered home assistant focused on meal planning and kitchen management. It helps you build a food database, plan meals, track what you want to cook, generate shopping lists, monitor food expiration dates, and learn your favorite meals over time.

# Raspberry Pi
## Task 1 TODO: Bootstrap Local Kubernetes LLM Runtime

Set up the first atomic version of Homer by preparing a local Kubernetes environment on a Raspberry Pi and deploying a lightweight LLM runtime as an isolated service.

### Goal

Create a minimal local Kubernetes setup capable of running an LLM service and exposing it internally so a future Homer agent can connect to it.

### Tasks

- [ ] Prepare the Raspberry Pi with a 64-bit Linux OS.
- [ ] Update the system packages.
- [ ] Install `k3s` as the local Kubernetes distribution.
- [ ] Verify the cluster is running with `kubectl get nodes`.
- [ ] Create a dedicated Kubernetes namespace called `homer`.
- [ ] Choose the first LLM runtime:
  - [ ] Start with `ollama/ollama` for the simplest Raspberry Pi setup.
  - [ ] Keep `vllm/vllm-openai-cpu` as a later experiment.
- [ ] Create a Kubernetes `Deployment` for the LLM runtime.
- [ ] Create a Kubernetes `Service` to expose the LLM runtime inside the cluster.
- [ ] Add a persistent volume claim for model storage.
- [ ] Pull a small model suitable for Raspberry Pi, such as:
  - `llama3.2:1b`
  - `qwen2.5:0.5b`
  - `qwen2.5:1.5b`
- [ ] Test the LLM service from inside the cluster using a temporary debug pod.
- [ ] Send a simple prompt to the model.
- [ ] Confirm the model returns a valid response.
- [ ] Document the commands needed to deploy, test, and remove the LLM service.

### Success Criteria

The Raspberry Pi runs a local Kubernetes cluster with one LLM runtime service deployed. The service should be reachable from inside the cluster and able to respond to a basic prompt.

Example expected flow:

```bash
kubectl get nodes
kubectl create namespace homer
kubectl apply -f infra/k8s/llm/
kubectl -n homer get pods
kubectl -n homer get svc
```

# Computah
## TODO: Run Homer LLM Runtime on Local Computer Kubernetes

Set up the same minimal Homer LLM runtime on a local computer, independently from the Raspberry Pi setup. The goal is to create a local Kubernetes environment where Ollama runs as an internal service and can be tested from another pod.

### Goal

Prepare a local Kubernetes cluster on the development machine and deploy Ollama as the first LLM runtime for Homer. This setup will be used for faster experimentation before deploying changes to the Raspberry Pi.

### Tasks

- [ ] Choose a local Kubernetes option:
  - [ ] Use `kind` for a lightweight, disposable local cluster.
  - [ ] Use `minikube` if GPU/device access or a more VM-like setup is preferred.
  - [ ] Use Docker Desktop Kubernetes if it is already enabled.
  - Using `kind`:
        Windows
        ├── Docker Desktop
        │   └── WSL2 backend
        │
        └── WSL2 Ubuntu
            ├── kubectl
            ├── kind
            └── cluster Kubernetes "homer"
                ├── node container
                └── namespace homer

- [ ] Install the required local tools:
  - [ ] `kubectl`
  - [ ] `kind` or `minikube`
  - [ ] Docker or another compatible container runtime.
- [ ] Create a local Kubernetes cluster for Homer.
- [ ] Verify the cluster is running with `kubectl get nodes`.
- [ ] Create a dedicated Kubernetes namespace called `homer`.
- [ ] Deploy Ollama using the existing Kubernetes manifests or a local-specific variant.
- [ ] Create a Kubernetes `Service` for Ollama.
- [ ] Add a persistent volume claim for local model storage.
- [ ] Verify that the Ollama pod starts successfully.
- [ ] Pull a small local model, such as:
  - `llama3.2:1b`
  - `qwen2.5:0.5b`
  - `qwen2.5:1.5b`
- [ ] Test the Ollama API from inside the cluster using a temporary debug pod.
- [ ] Send a simple prompt to the model.
- [ ] Confirm that the model returns a valid response.
- [ ] Optionally expose Ollama locally with `kubectl port-forward`.
- [ ] Document the commands needed to create, test, and delete the local cluster.

### Example Flow

```bash
kind create cluster --name homer
kubectl get nodes
kubectl create namespace homer
kubectl apply -f infra/k8s/llm/
kubectl -n homer get pods
kubectl -n homer get svc
```