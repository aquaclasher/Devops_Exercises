"""Build, run, inspect, and stop the Flask container with an AppArmor profile."""

import docker

IMAGE = "flask-apparmor"
PROFILE = "my-apparmor-profile"

client = docker.from_env()

print("Building image from Dockerfile...")
client.images.build(path=".", tag=IMAGE)

print("Running container with AppArmor profile...")
container = client.containers.run(
    IMAGE,
    ports={"5000/tcp": 5000},
    security_opt=[f"apparmor={PROFILE}"],
    detach=True,
)

try:
    print(f"Container started: {container.short_id}")
    container_info = client.api.inspect_container(container.id)
    print(f"AppArmor profile applied: {container_info['HostConfig']['SecurityOpt']}")
finally:
    print("Stopping container...")
    container.stop()
