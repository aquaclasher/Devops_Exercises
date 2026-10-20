# Exercise 6: Real-Time Operations Monitoring and Alerting

## Objective
Simulate real-time operational delivery metrics for a quick-commerce service using Python, scrape and evaluate alert rules using Prometheus, visualize key performance indicators with Grafana dashboards, and automate deployment via a Jenkins pipeline on Windows.

## Prerequisites
- Windows 10/11 with Docker Desktop installed and running
- Python 3.10+ installed
- PowerShell 5.1+ or PowerShell 7+
- Prometheus Python client library installed:
  ```powershell
  pip install prometheus-client
  ```

## Implementation Files
- `delivery_metrics.py`: Simulates live delivery operations (total, pending, on-the-way, average delivery time) and exposes Prometheus metrics on HTTP port 8000 (`/metrics`).
- `prometheus.yml`: Configures Prometheus with `host.docker.internal` targets to scrape host metrics on Windows.
- `alert_rules.yml`: Defines alert thresholds for `HighPendingDeliveries` (>10 for 15s) and `HighAverageDeliveryTime` (>30s for 15s).
- `Dockerfile`: Containerizes the metric simulator.
- `requirements.txt`: Python package requirement (`prometheus-client`).
- `Jenkinsfile`: Declarative Jenkins pipeline automating container builds, app deployment, and monitoring stack spin-up.

## Steps to Execute (Windows PowerShell)

### Step 1: Run the Metrics Simulator
In PowerShell:
```powershell
python delivery_metrics.py
```
In a second PowerShell window, verify the metrics endpoint:
```powershell
curl.exe http://localhost:8000/metrics
```

### Step 2: Start Prometheus in Docker
From the `Exercise6` directory in PowerShell:
```powershell
docker run -d --name prometheus -p 9090:9090 -v "${PWD}\prometheus.yml:/etc/prometheus/prometheus.yml" -v "${PWD}\alert_rules.yml:/etc/prometheus/alert_rules.yml" prom/prometheus
```
Access Prometheus at [http://localhost:9090](http://localhost:9090):
- Go to **Status -> Targets**: Confirm that `delivery_service` (pointing to `host.docker.internal:8000`) is in state **UP**.
- Go to **Alerts**: Verify `HighPendingDeliveries` and `HighAverageDeliveryTime` transitions from **PENDING** to **FIRING**.

### Step 3: Start Grafana in Docker
In PowerShell:
```powershell
docker run -d --name grafana -p 3000:3000 grafana/grafana
```
1. Open [http://localhost:3000](http://localhost:3000) in your web browser.
2. Log in using `admin` for both Username and Password (skip password reset).
3. Navigate to **Connections -> Data sources -> Add data source -> Prometheus**.
4. Set the **Prometheus server URL** to:
   ```text
   http://host.docker.internal:9090
   ```
5. Click **Save & Test** to confirm successful connection.

### Step 4: Create Delivery Operations Dashboard
In Grafana, create a new Dashboard and add 4 visualization panels:
1. **Total Deliveries**: Query `total_deliveries` (Stat or Gauge)
2. **Pending Deliveries**: Query `pending_deliveries` (Time Series or Gauge)
3. **On-the-Way Deliveries**: Query `on_the_way_deliveries` (Time Series)
4. **Average Delivery Time**: Query `average_delivery_time_sum / average_delivery_time_count` (Stat)

### Step 5: Automate via Jenkins Pipeline
1. Start the Jenkins container in PowerShell:
   ```powershell
   docker run -d --name jenkins -p 8080:8080 -p 50000:50000 `  -v jenkins_home:/var/jenkins_home `  -v //var/run/docker.sock:/var/run/docker.sock `  -u root `  jenkins/jenkins:lts
   ```
2. Retrieve the initial admin password:
   ```powershell
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Open [http://localhost:8080](http://localhost:8080) and create a **Pipeline** job using `Jenkinsfile`.

## Clean Up (Windows PowerShell)
```powershell
docker stop prometheus grafana jenkins
docker rm prometheus grafana jenkins
```
