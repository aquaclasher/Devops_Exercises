# Exercise 9: Jenkins Multi-Stage Pipeline for Deploying a Python Application

## Objective
Create and execute a multi-stage Jenkins Declarative Pipeline that automates the lifecycle of a Python Flask application across **Build**, **Test**, **Deploy**, **Run Application**, and **Test Application** stages.

## Prerequisites
- Windows 10/11 with Docker Desktop running
- Jenkins running (from Exercise 7 at [http://localhost:8080](http://localhost:8080))
- Pipeline plugin installed in Jenkins
- Python 3 installed on Windows

## Implementation Files
- `app.py`: Flask web application returning `"Hello, Jenkins Multi-Stage Pipeline!"`.
- `requirements.txt`: Python dependencies (`flask==2.1.2`).
- `test_app.py`: Unit test verifying HTTP 200 status code and response payload.
- `Jenkinsfile`: Declarative Pipeline defining build, test, mock deployment, and validation stages.

## Steps to Execute (Windows PowerShell)

### Step 1: Verify Tests Locally on Windows
In PowerShell:
```powershell
pip install -r requirements.txt
python -m unittest discover -s .
```

### Step 2: Push Files to Git Repository
In PowerShell:
```powershell
git init
git add app.py requirements.txt test_app.py Jenkinsfile
git commit -m "Add multi-stage pipeline and application"
git branch -M main
git remote add origin https://github.com/<your-username>/devops-sample-code.git
git push -u origin main
```

### Step 3: Install Python Dependencies Inside Jenkins Container
Because the pipeline executes tests and runs the mock application inside the Jenkins container, install Python and Flask into the container from PowerShell:
```powershell
docker exec -u root jenkins bash -c "apt-get update && apt-get install -y python3 python3-pip python3-flask"
```

### Step 4: Create and Configure Jenkins Pipeline
1. In the Jenkins dashboard, click **New Item**.
2. Name the project `Python-MultiStage-Pipeline`, select **Pipeline**, and click **OK**.
3. Under the **Pipeline** configuration section:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/<your-username>/devops-sample-code.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
4. Click **Save**.

### Step 5: Run the Pipeline and Verify Stages
1. Click **Build Now** to trigger execution.
2. Monitor the Stage View in Jenkins:
   - **Build**: Resolves environment and dependencies.
   - **Test**: Executes `python3 -m unittest discover -s .` with passing status.
   - **Deploy**: Copies application code to `${WORKSPACE}/python-app-deploy`.
   - **Run Application**: Launches Flask with `nohup` in the background and saves PID.
   - **Test Application**: Runs integration tests against the active application.
   - **Post Actions**: Reports `Pipeline completed successfully!`.
3. Open **Console Output** to verify `Finished: SUCCESS`.
