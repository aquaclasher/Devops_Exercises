# Exercise 10: Multi-Node Kubernetes Cluster with Multiple Applications and ReplicaSets

## Objective
Deploy a distributed multi-tier e-commerce architecture (Product Catalog and Shopping Cart) onto a 3-node Minikube cluster on Windows using ReplicaSets and Pod Anti-Affinity rules to guarantee high availability and node redundancy.

## Architecture
- **Product Catalog (AppA)**: 2 replicas, scheduled across different cluster nodes. Exposes `/products`.
- **Shopping Cart (AppB)**: 3 replicas, scheduled across all 3 nodes using `podAntiAffinity`. Exposes `/cart` (GET & POST).

## Prerequisites
- Windows 10/11 with Docker Desktop running
- Minikube and kubectl CLI installed on Windows
- PowerShell

## Implementation Files
- `product_catalog.py`: Flask service exposing product inventory.
- `shopping_cart.py`: Flask service managing shopping carts.
- `Dockerfile.product`: Container specification for Product Catalog.
- `Dockerfile.shopping`: Container specification for Shopping Cart.
- `product_catalog_deployment.yaml`: Deployment manifest (2 replicas, `podAntiAffinity` on `kubernetes.io/hostname`).
- `shopping_cart_deployment.yaml`: Deployment manifest (3 replicas, `podAntiAffinity` on `kubernetes.io/hostname`).
- `product_catalog_service.yaml`: NodePort Service for Product Catalog.
- `shopping_cart_service.yaml`: NodePort Service for Shopping Cart.
- `requirements.txt`: Python dependencies (`flask`).

## Steps to Execute (Windows PowerShell)

### Step 1: Start 3-Node Minikube Cluster
In PowerShell:
```powershell
minikube start --nodes 3 -p devops-multinode --driver=docker
```
Verify all 3 nodes are Ready:
```powershell
kubectl get nodes
```
Expected output:
```text
NAME                     STATUS   ROLES           AGE   VERSION
devops-multinode         Ready    control-plane   1m    v1.31.0
devops-multinode-m02     Ready    <none>          45s   v1.31.0
devops-multinode-m03     Ready    <none>          30s   v1.31.0
```

### Step 2: Build and Load Docker Images into Minikube
Build the images locally in PowerShell:
```powershell
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
```
Load the built images into the multi-node Minikube cluster:
```powershell
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

### Step 3: Deploy Applications and Services
```powershell
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml
kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml
```

### Step 4: Verify Multi-Node Distribution
Inspect running pods with their node assignments:
```powershell
kubectl get pods -o wide
```
Verify node spread:
- The 2 `product-catalog` pods run on two separate nodes.
- The 3 `shopping-cart` pods run across all three distinct nodes (`devops-multinode`, `devops-multinode-m02`, `devops-multinode-m03`) as enforced by `podAntiAffinity`.

### Step 5: Access and Test Services via Minikube
Open separate PowerShell windows to start service tunnels:
```powershell
minikube -p devops-multinode service product-catalog-service --url
minikube -p devops-multinode service shopping-cart-service --url
```

Test endpoints in PowerShell using `curl.exe` or `Invoke-RestMethod`:
```powershell
# Test Product Catalog
curl.exe <product-catalog-url>/products

# Test Shopping Cart (GET initial empty cart)
curl.exe <shopping-cart-url>/cart

# Add item to Shopping Cart (POST)
Invoke-RestMethod -Uri "<shopping-cart-url>/cart" -Method Post -ContentType "application/json" -Body '{"id": 1, "name": "Laptop", "quantity": 1}'
```

## Clean Up (Windows PowerShell)
```powershell
kubectl delete -f shopping_cart_service.yaml
kubectl delete -f product_catalog_service.yaml
kubectl delete -f shopping_cart_deployment.yaml
kubectl delete -f product_catalog_deployment.yaml
minikube stop -p devops-multinode
```
