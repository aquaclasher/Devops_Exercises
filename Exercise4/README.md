# Exercise 4: Docker Networking with Multiple Containers

## Objective
Understand Docker networking concepts, create a custom bridge network, and deploy a multi-tier containerized system consisting of a Flask API, MySQL database, and Redis cache communicating via container name DNS resolution.

## Prerequisites
- Docker Desktop

## Implementation Files
- `app.py`: REST API built with Flask exposing `/about` on port 5001.
- `requirements.txt`: Python package dependencies (`Flask==2.0.1`).
- `Dockerfile`: Container image specification based on `python:3.9-slim`.

## Steps to Execute

1. **Create the Custom Bridge Network**:
   ```bash
   docker network create --driver bridge my-bridge-net
   ```

2. **Verify and Inspect the Network**:
   ```bash
   docker network ls
   docker network inspect my-bridge-net
   ```

3. **Build the Flask API Container Image**:
   ```bash
   docker build -t flask-api .
   ```

4. **Launch the Multi-Container Stack**:
   Start MySQL, Redis, and Flask on the shared network:
   ```bash
   docker run -d --name mysql --net=my-bridge-net -e MYSQL_ROOT_PASSWORD=rootpassword mysql:latest
   docker run -d --name redis --net=my-bridge-net redis:latest
   docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
   ```

5. **Verify Running Containers**:
   ```bash
   docker ps
   ```

6. **Test Application Endpoint**:
   ```bash
   curl http://127.0.0.1:5001/about
   ```
   Expected response:
   ```json
   {
     "description": "This is a simple REST API built with Flask.",
     "name": "Simple REST API",
     "version": "1.0"
   }
   ```

7. **Test Inter-Container Connectivity**:
   Verify DNS name resolution and network reachability from the Flask container:
   ```bash
   docker exec flask python -c "import socket; print('mysql:', socket.gethostbyname('mysql')); print('redis:', socket.gethostbyname('redis'))"
   docker exec flask python -c "import socket; [print(h, socket.create_connection((h, p), 5).close() or 'reachable') for h, p in [('mysql', 3306), ('redis', 6379)]]"
   ```

## Clean Up
```bash
docker stop mysql redis flask
docker rm mysql redis flask
docker network rm my-bridge-net
```

---

## Questions & Answers

**Q1: What is the purpose of the `--net` flag in `docker run`?**  
**A1:** The `--net` (or `--network`) flag specifies the Docker network to which the container should be attached upon creation.

**Q2: How do containers communicate with each other on the same custom bridge network?**  
**A2:** Containers on a custom bridge network use Docker's embedded DNS server to resolve each other's container names into internal IP addresses.

**Q3: What is the difference between a bridge network and a host network?**  
**A3:** A bridge network provides network isolation, assigning containers their own private IP subnet and virtual network interface. A host network bypasses network isolation, placing the container directly on the host's network stack where container ports bind directly to host interfaces.

**Q4: How can you expose a container's port to the host machine?**  
**A4:** Use the `-p` (or `--publish`) flag during `docker run` in the format `-p <host_port>:<container_port>` (e.g., `-p 5001:5001`).
