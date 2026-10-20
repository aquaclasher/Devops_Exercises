# Exercise 3: Scaling Flask App on Single Node Using ReplicaSets

## Objective
Understand Kubernetes ReplicaSets and Pod lifecycle, scale a Flask flash-sale application dynamically, observe pod distribution, and verify automatic self-healing when a pod is terminated.

## Prerequisites
- Docker Desktop
- Minikube
- kubectl CLI

## Implementation Files
- `app.py`: Flask application simulating an e-commerce flash sale with `/`, `/buy`, and `/health` endpoints. Displays the serving Pod hostname.
- `requirements.txt`: Python package dependencies (`flask`, `gunicorn`).
- `Dockerfile`: Container image packaging the application with Gunicorn.
- `flashsale-replicaset.yaml`: Kubernetes `ReplicaSet` (initial replicas: 3) with readiness/liveness probes and resource limits, along with a ClusterIP `Service`.

## Steps to Execute

1. **Build and Load the Docker Image**:
   ```bash
   docker build -t flashsale:1.0 .
   minikube image load flashsale:1.0
   ```

2. **Apply the ReplicaSet Configuration**:
   ```bash
   kubectl apply -f flashsale-replicaset.yaml
   ```

3. **Verify Pods and ReplicaSet (Initial State = 3 replicas)**:
   ```bash
   kubectl get rs flashsale-rs
   kubectl get pods -l app=flashsale -o wide
   ```

4. **Scale the ReplicaSet to 5 Replicas**:
   ```bash
   kubectl scale rs flashsale-rs --replicas=5
   ```

5. **Verify the Scaled Replicas**:
   ```bash
   kubectl get rs flashsale-rs
   kubectl get pods -l app=flashsale -o wide
   ```

6. **Demonstrate Self-Healing**:
   Delete one of the running pods manually:
   ```bash
   kubectl delete pod <pod-name>
   ```
   Watch the pods to verify ReplicaSet instantly launches a replacement:
   ```bash
   kubectl get pods -l app=flashsale -w
   ```

7. **Test Endpoints via Port Forwarding**:
   ```bash
   kubectl port-forward service/flashsale-svc 8080:80
   ```
   In a separate terminal:
   ```bash
   curl http://127.0.0.1:8080/
   curl "http://127.0.0.1:8080/buy?user=student"
   curl http://127.0.0.1:8080/health
   ```

## Clean Up
```bash
kubectl delete -f flashsale-replicaset.yaml
```

---

## Questions & Answers

**Q1: What is the initial number of replicas in the ReplicaSet?**  
**A1:** 3

**Q2: How many pods are running after applying the ReplicaSet configuration?**  
**A2:** 3

**Q3: What happens when you scale the ReplicaSet to 5 replicas?**  
**A3:** Kubernetes creates 2 additional pods to match the desired replica count of 5.

**Q4: What happens when you delete one pod?**  
**A4:** Kubernetes automatically creates a new replacement pod to maintain the desired count of 5 replicas.

**Q5: How does Kubernetes maintain the desired number of replicas?**  
**A5:** The ReplicaSet controller continuously monitors the cluster state, compares actual running pods matching the label selector against `spec.replicas`, and adds or terminates pods to reconcile differences.

**Q6: How many nodes are running?**  
**A6:** 1 (single-node Minikube cluster).

**Q7: Where are the pods running with respect to nodes?**  
**A7:** All 5 pods are scheduled and running on the single `minikube` node.
