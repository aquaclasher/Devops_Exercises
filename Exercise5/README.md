# Exercise 5: Docker Security with AppArmor

This project contains a Flask container, an AppArmor confinement profile, and Docker SDK scripts to apply and test the profile.

## Important platform requirement

AppArmor is enforced by the **Linux Docker host kernel**, not by the container image. This Windows computer uses Docker Desktop's WSL backend, whose kernel reports AppArmor as disabled. Therefore, building the image works here, but loading or enforcing `my-apparmor-profile` does not.

Run the security-enforcement steps below on an Ubuntu/Debian Linux Docker host with AppArmor enabled. Verify first:

```bash
sudo aa-status
docker info | grep -i apparmor
```

## Build the application image

```bash
docker build -t flask-apparmor .
```

## Install and load the profile (Linux host only)

```bash
sudo apt-get update
sudo apt-get install -y apparmor apparmor-utils
sudo cp my-apparmor-profile /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
sudo aa-status | grep my-apparmor-profile
```

## Run with the profile

```bash
docker run --rm --security-opt="apparmor=my-apparmor-profile" -p 5000:5000 flask-apparmor
```

In another terminal:

```bash
curl http://127.0.0.1:5000/
```

## Docker SDK scripts (Linux host only)

```bash
python3 -m pip install -r requirements-dev.txt
python3 apply_apparmor.py
python3 test_restricted_actions.py
```

`apply_apparmor.py` builds the image, starts a container with the profile, prints `HostConfig.SecurityOpt`, and stops it. `test_restricted_actions.py` verifies that reading `/etc/passwd` and executing `/bin/bash` are denied.

## Evidence to capture

1. `aa-status` showing AppArmor enabled and `my-apparmor-profile` loaded.
2. `docker inspect` or `apply_apparmor.py` showing `apparmor=my-apparmor-profile` in `SecurityOpt`.
3. The restricted-action script showing non-zero exit codes for the protected read and `/bin/bash` execution.

## Why this cannot be enforced locally

The current Docker Desktop host reports `N` at `/sys/module/apparmor/parameters/enabled` and has no `name=apparmor` entry in `docker info` security options. Docker therefore cannot apply a custom AppArmor profile on this host.
