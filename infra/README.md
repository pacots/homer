# Homer Infrastructure

This directory contains the infrastructure configuration required to run Homer in Kubernetes-based environments.

It currently supports:

- Local development with `kind` running inside WSL2.
- Raspberry Pi deployment with `k3s`.

Both environments use the same Kubernetes manifests under `infra/k8s`.

## Directory Structure

```text
infra/
├── README.md
├── kind/
│   └── kind-config.yaml
└── k8s/
    ├── homer-llm.yaml
    └── README-homer-llm.md
```

## Environments

### Local development with kind

The local development environment runs Kubernetes inside WSL2 using `kind`, with Docker Desktop providing the container runtime.

```text
Windows
├── Docker Desktop
│   └── WSL2 backend
│
└── WSL2 Ubuntu
    ├── kubectl
    ├── kind
    └── Kubernetes cluster: "homer"
        ├── node container
        └── namespace: "homer"
```

The local `kind` configuration is stored in:

```text
infra/kind/kind-config.yaml
```

### Raspberry Pi with k3s

The Raspberry Pi environment runs Kubernetes using `k3s`.

The same manifests under `infra/k8s` can be applied to the Raspberry Pi cluster.

## Local kind Port Mapping

The local `kind` cluster maps Kubernetes NodePorts from the kind node container to the host machine.

For the LLM service, the expected mapping is:

```yaml
extraPortMappings:
  - containerPort: 31434
    hostPort: 31434
    protocol: TCP
```

This allows Ollama to be reached locally at:

```text
http://localhost:31434
```

If this port mapping changes, the local `kind` cluster must be recreated.

## Prerequisites

### Local development

Inside WSL2, verify that the required tools are available:

```bash
kubectl version --client
kind version
docker version
```

Docker Desktop must be running on Windows with WSL2 integration enabled.

### Raspberry Pi

On the Raspberry Pi, `k3s` should already be installed and running.

Check the cluster:

```bash
kubectl get nodes
```

## Create the Local kind Cluster From Scratch

From the project root:

```bash
kind create cluster --name homer --config infra/kind/kind-config.yaml
```

Verify the cluster:

```bash
kubectl cluster-info
kubectl get nodes
```

## Deploy the Infrastructure

Apply all Kubernetes manifests:

```bash
kubectl apply -f infra/k8s/
```

Verify the resources:

```bash
kubectl get all -n homer
kubectl get pvc -n homer
```

Watch pods until they are running:

```bash
kubectl get pods -n homer -w
```

## Deploy a Specific Service

To deploy only the LLM service:

```bash
kubectl apply -f infra/k8s/homer-llm.yaml
```

For details about the LLM service, see:

```text
infra/k8s/README-homer-llm.md
```

## Start an Existing Local kind Cluster

A `kind` cluster runs as Docker containers.

First, check if the cluster exists:

```bash
kind get clusters
```

If `homer` appears, make sure Docker Desktop is running and check the nodes:

```bash
kubectl get nodes
```

Then apply or re-apply the manifests:

```bash
kubectl apply -f infra/k8s/
```

## Stop the Local kind Cluster Temporarily

List running Docker containers:

```bash
docker ps
```

You should see a container similar to:

```text
homer-control-plane
```

Stop it:

```bash
docker stop homer-control-plane
```

Start it again later:

```bash
docker start homer-control-plane
```

Then verify the cluster:

```bash
kubectl get nodes
```

## Recreate the Local kind Cluster

Recreate the cluster when:

- The `kind-config.yaml` port mappings change.
- The local cluster is broken.
- You want a clean local environment.

Delete the cluster:

```bash
kind delete cluster --name homer
```

Create it again:

```bash
kind create cluster --name homer --config infra/kind/kind-config.yaml
```

Apply the manifests:

```bash
kubectl apply -f infra/k8s/
```

## Update the Infrastructure

After editing any Kubernetes manifest, apply the changes again:

```bash
kubectl apply -f infra/k8s/
```

Check rollout status for a deployment:

```bash
kubectl rollout status deployment/<deployment-name> -n homer
```

Example:

```bash
kubectl rollout status deployment/homer-llm -n homer
```

## Restart a Deployment

Restart a deployment without deleting the cluster:

```bash
kubectl rollout restart deployment/<deployment-name> -n homer
```

Example:

```bash
kubectl rollout restart deployment/homer-llm -n homer
```

Watch the rollout:

```bash
kubectl rollout status deployment/homer-llm -n homer
```

## Delete Kubernetes Resources

Delete all resources defined in `infra/k8s`:

```bash
kubectl delete -f infra/k8s/
```

Delete only the LLM service:

```bash
kubectl delete -f infra/k8s/homer-llm.yaml
```

Delete the full `homer` namespace:

```bash
kubectl delete namespace homer
```

Be careful: deleting the namespace also deletes resources inside it, including the PersistentVolumeClaim used by Ollama.

## Delete the Local kind Cluster

To completely remove the local cluster:

```bash
kind delete cluster --name homer
```

This removes the Kubernetes cluster and all resources running inside it.

## Troubleshooting

### Check all resources

```bash
kubectl get all -n homer
```

### Check pods

```bash
kubectl get pods -n homer
```

### Check services

```bash
kubectl get svc -n homer
```

### Check persistent volume claims

```bash
kubectl get pvc -n homer
```

### Describe a failing pod

```bash
kubectl describe pod -n homer <pod-name>
```

### Check logs for a deployment

```bash
kubectl logs -n homer deployment/<deployment-name>
```

Example:

```bash
kubectl logs -n homer deployment/homer-llm
```

### Test access from inside the cluster

Run a temporary curl pod:

```bash
kubectl run curl-test -n homer --rm -it --image=curlimages/curl -- sh
```

Inside the temporary pod, call the target service.

Example for the LLM service:

```sh
curl http://homer-llm:11434/api/tags
```

## Common Commands

Create local cluster:

```bash
kind create cluster --name homer --config infra/kind/kind-config.yaml
```

Deploy infrastructure:

```bash
kubectl apply -f infra/k8s/
```

Check resources:

```bash
kubectl get all -n homer
```

Delete resources:

```bash
kubectl delete -f infra/k8s/
```

Delete local cluster:

```bash
kind delete cluster --name homer
```