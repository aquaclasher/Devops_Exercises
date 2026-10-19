# Exercise 1: Kubernetes Hello Pod

This exercise deploys the Nginx web server as a Kubernetes Pod and exposes it through a `NodePort` Service.

## Prerequisites installed

- Docker Desktop
- Minikube v1.39.0
- kubectl v1.36.1

## Run

```powershell
minikube start --driver=docker
kubectl apply -f pod.yaml
kubectl apply -f service.yaml
kubectl get pods -w
kubectl get services
minikube service hello-k8s
```

## Files

- `pod.yaml` defines the `hello-k8s` Pod, running Nginx on port 80.
- `service.yaml` defines a `NodePort` Service that selects that Pod using its `app: hello-k8s` label.

## Clean up

```powershell
kubectl delete -f service.yaml
kubectl delete -f pod.yaml
```
