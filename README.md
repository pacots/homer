# homer
Homer is an AI-powered home assistant focused on meal planning and kitchen management. It helps you build a food database, plan meals, track what you want to cook, generate shopping lists, monitor food expiration dates, and learn your favorite meals over time.

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