# homer
Homer is an AI-powered home assistant focused on meal planning and kitchen management. It helps you build a food database, plan meals, track what you want to cook, generate shopping lists, monitor food expiration dates, and learn your favorite meals over time.

# Raspberry Pi
```bash
kubectl get nodes
kubectl create namespace homer
kubectl apply -f infra/k8s/llm/
kubectl -n homer get pods
kubectl -n homer get svc
```

# Computah
### Example Flow

```bash
kind create cluster --name homer
kubectl get nodes
kubectl create namespace homer
kubectl apply -f infra/k8s/llm/
kubectl -n homer get pods
kubectl -n homer get svc
```