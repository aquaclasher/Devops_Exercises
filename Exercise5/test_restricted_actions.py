"""Verify that the AppArmor profile blocks protected reads and binary execution."""

import docker

IMAGE = "flask-apparmor"
PROFILE = "my-apparmor-profile"

client = docker.from_env()
container = client.containers.run(
    IMAGE,
    security_opt=[f"apparmor={PROFILE}"],
    detach=True,
)

try:
    print(f"Container started: {container.short_id}")

    # Use Python so the request reaches /etc/passwd rather than failing because
    # the profile also denies executing /usr/bin/cat.
    exit_code, output = container.exec_run(
        ["python", "-c", "print(open('/etc/passwd').read())"]
    )
    print(f"Attempt to read /etc/passwd: Exit Code {exit_code}, Output: {output.decode()}")

    exit_code, output = container.exec_run(["/bin/bash", "-c", "echo should-not-run"])
    print(f"Attempt to execute /bin/bash: Exit Code {exit_code}, Output: {output.decode()}")
finally:
    container.stop()
    print("Container stopped")
