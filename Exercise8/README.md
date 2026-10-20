# Exercise 8: Creating "Hello World" CI/CD Jenkins Job

## Objective
Create and configure an automated Jenkins Freestyle job on Windows that clones a repository from GitHub containing a shell script (`hello-world.sh`), executes it inside a build step, and verifies execution logs.

## Prerequisites
- Jenkins running locally on Windows (from Exercise 7 at [http://localhost:8080](http://localhost:8080))
- Git installed on Windows
- GitHub account

## Implementation Files
- `hello-world.sh`: Shell script printing `"Hello, Jenkins!"`.

## Steps to Execute (Windows PowerShell)

### Step 1: Verify the Shell Script
The `hello-world.sh` script in this folder contains:
```bash
#!/bin/bash
echo "Hello, Jenkins!"
```

### Step 2: Push the Script to GitHub
Open Windows PowerShell in the `Exercise8` directory and run:
```powershell
git init
git add hello-world.sh
git commit -m "Add hello-world.sh"
git branch -M main
git remote add origin https://github.com/<your-username>/devops-sample-code.git
git push -u origin main
```

### Step 3: Create Jenkins Freestyle Project
1. Open Jenkins at [http://localhost:8080](http://localhost:8080).
2. Click **New Item** on the top-left sidebar.
3. Enter name: `HelloWorld`.
4. Select **Freestyle project** and click **OK**.

### Step 4: Configure Job Settings
1. **General**:
   - Description: `Hello World! Jenkins job.`
2. **Source Code Management**:
   - Select **Git**.
   - Repository URL: `https://github.com/<your-username>/devops-sample-code.git`
   - Branch Specifier: `*/main`
3. **Build Steps**:
   - Click **Add build step** -> **Execute shell**.
   - Command:
     ```bash
     sh hello-world.sh
     ```
4. Click **Save**.

### Step 5: Run Build and Inspect Output
1. Click **Build Now** on the project page.
2. Under **Build History**, click build `#1`.
3. Select **Console Output** to view execution logs:
   ```text
   Started by user admin
   Building in workspace /var/jenkins_home/workspace/HelloWorld
   [HelloWorld] $ /bin/sh -xe /tmp/jenkins...sh
   + sh hello-world.sh
   Hello, Jenkins!
   Finished: SUCCESS
   ```
