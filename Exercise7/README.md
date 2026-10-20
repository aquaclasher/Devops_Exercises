# Exercise 7: Jenkins Installation and Introduction to CI/CD Tools

## Objective
Understand the core principles and benefits of Continuous Integration (CI), examine industry-standard CI/CD tools, deploy Jenkins LTS using Docker Desktop on Windows, and complete initial administrative configuration.

## Prerequisites
- Windows 10/11 with Docker Desktop installed and running
- PowerShell
- Web browser (Chrome, Edge, Firefox)

## Continuous Integration (CI) Overview
Continuous Integration is a software engineering practice where team members integrate code changes frequently into a shared version-controlled repository. Automated builds and test suites execute on every push, providing immediate feedback and preventing regression defects.

### Key Benefits
- **Early Bug Detection**: Catches integration flaws and regressions immediately.
- **Fast Feedback Loop**: Developers know within minutes if a commit broke compilation or test suites.
- **Automated Consistency**: Eliminates manual build discrepancies between local machines.
- **Higher Software Reliability**: Ensures the main branch remains stable and release-ready.

### Major CI/CD Tools Comparison
| Tool | Platform | Core Strength |
| :--- | :--- | :--- |
| **Jenkins** | Self-hosted / Open Source | Highly extensible with 1,800+ plugins; industry standard |
| **GitHub Actions** | Hosted (GitHub) | Native repository integration, rich YAML workflow ecosystem |
| **GitLab CI/CD** | GitLab Platform | Integrated Auto-DevOps, native container registries |
| **CircleCI** | Cloud / Self-hosted | Optimized for Docker containers, fast parallel build runners |
| **Azure DevOps** | Microsoft Azure | Robust enterprise project management and multi-cloud pipelines |
| **TeamCity** | JetBrains | Advanced build chain analytics, native JetBrains IDE ecosystem |

---

## Steps to Execute (Windows PowerShell)

### Step 1: Run the Jenkins Container
Open Windows PowerShell and run:
```powershell
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```
*Alternatively, launch using Docker Compose:*
```powershell
docker compose up -d
```

### Step 2: Verify Jenkins Status
```powershell
docker ps --filter "name=jenkins"
```

### Step 3: Retrieve Initial Admin Password
Extract the auto-generated administrator password from the persistent volume:
```powershell
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Copy the printed 32-character key.

### Step 4: Complete the Jenkins Setup Wizard
1. Open [http://localhost:8080](http://localhost:8080) in your web browser.
2. Paste the administrator key on the **Unlock Jenkins** page and click **Continue**.
3. Choose **Install suggested plugins** to set up common Git, Pipeline, and SCM capabilities.
4. Create your administrator account (or continue as admin).
5. Verify the Instance Configuration URL (`http://localhost:8080/`).
6. Click **Save and Finish** to arrive at the Jenkins Dashboard.

## Clean Up (Windows PowerShell)
```powershell
docker stop jenkins
docker rm jenkins
```
