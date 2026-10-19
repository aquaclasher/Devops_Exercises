# Exercise 3: Scale a Flask Flash-Sale App with a ReplicaSet

This exercise runs a flash-sale Flask application in a Kubernetes `ReplicaSet`. Kubernetes begins with three identical Pods, scales to five, and replaces a manually deleted Pod to preserve the desired count.

## Prerequisites

- Docker Desktop running
- A running, single-node Minikube cluster
- kubectl

> The existing Minikube cluster is already single-node. Do not run `minikube delete`: it would remove the running work from earlier exercises and is not needed for this exercise.

## Build and deploy (Windows PowerShell)

```powershell
docker build -t flashsale:1.0 .
minikube image load flashsale:1.0
kubectl apply -f flashsale-replicaset.yaml
kubectl wait --for=condition=ready pod -l app=flashsale --timeout=120s
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
```

## Demonstrate scaling

```powershell
kubectl scale rs flashsale-rs --replicas=5
kubectl wait --for=condition=ready pod -l app=flashsale --timeout=120s
kubectl get rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
```

## Demonstrate self-healing

Choose a current Pod name from `kubectl get pods -l app=flashsale`, then run:

```powershell
kubectl delete pod <pod-name>
kubectl get pods -l app=flashsale -w
```

The ReplicaSet creates a replacement Pod so that five Pods are again ready. Press `Ctrl+C` to stop watching once it appears.

## Test through the Service

Because `flashsale-svc` is a `ClusterIP` Service, port-forward it locally for testing:

```powershell
kubectl port-forward service/flashsale-svc 8080:80
```

In a second terminal:

```powershell
curl http://127.0.0.1:8080/
curl "http://127.0.0.1:8080/buy?user=student"
curl http://127.0.0.1:8080/health
```

The JSON response includes the Pod hostname. Repeating requests can show different Pods serving traffic.

## Verify

```powershell
kubectl describe rs flashsale-rs
kubectl get pods -l app=flashsale -o wide
kubectl logs -l app=flashsale --prefix --tail=20
```

## Clean up

```powershell
kubectl delete -f flashsale-replicaset.yaml
```
