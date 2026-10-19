# Exercise 4: Docker Networking with Multiple Containers

This exercise attaches a Flask API, MySQL database, and Redis cache to one user-defined Docker bridge network. Docker provides internal DNS, so containers can use `mysql` and `redis` as hostnames.

## Run (Windows PowerShell)

Build the API image and create the bridge network:

```powershell
$MYSQL_ROOT_PASSWORD = Read-Host -Prompt "Enter MySQL Root Password"
docker build -t flask-api .
docker network create --driver bridge my-bridge-net
docker network ls
docker network inspect my-bridge-net
```

Start all three containers. `MYSQL_ROOT_PASSWORD` is mandatory for current official MySQL images and is passed using the `-e` flag below.

```powershell
docker run -d --name mysql --net=my-bridge-net -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD mysql:latest
docker run -d --name redis --net=my-bridge-net redis:latest
docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
```

## Verify

```powershell
docker ps
docker network inspect my-bridge-net
Invoke-WebRequest http://127.0.0.1:5001/about | Select-Object -ExpandProperty Content
```

Test Docker DNS and TCP reachability from the Flask container:

```powershell
docker exec flask python -c "import socket; print('mysql:', socket.gethostbyname('mysql')); print('redis:', socket.gethostbyname('redis'))"
docker exec flask python -c "import socket; [print(host, socket.create_connection((host, port), 5).close() or 'TCP reachable') for host, port in [('mysql', 3306), ('redis', 6379)]]"
```

`python:3.9-slim` does not include the `ping` program. These commands verify the same important networking behavior: Docker DNS resolves the container names and the target ports accept connections.

## Clean up

```powershell
docker stop mysql redis flask
docker rm mysql redis flask
docker network rm my-bridge-net
```
