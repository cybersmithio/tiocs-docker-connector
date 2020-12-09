import docker
from tenable.io import TenableIO
import os
from tenable.errors import NotFoundError
import re

tio_access_key = os.environ['TIO_ACCESS_KEY']
tio_secret_key = os.environ['TIO_SECRET_KEY']

# Gather running containers
docker_client = docker.from_env()

# Check Tenable.io for a previous assessment, and if one doesn't exist then trigger an assessment
tio = TenableIO(tio_access_key, tio_secret_key)

for i in docker_client.containers.list():
    #print("Docker container name: ", i.name)
    #print("Docker container ID: ", i.id)
    #print("Docker short container ID: ", i.short_id)
    print("Docker image tags: ", i.image.tags)
    print("Docker image ID: ", i.image.id)
    print("Docker image short ID: ", i.image.short_id)
    image_id = re.search("sha256:([0-9a-f]{12}).*", i.image.id)
    if image_id is not None:
        print("Image ID:", image_id[1])
        querystring = {"image_id": image_id[1]}
        url = "container-security/api/v1/reports/by_image"
        try:
            response = tio.get(url, params=querystring)
            json_response = response.json()
            print(f"Image risk score: {json_response['risk_score']}")
        except NotFoundError:
            print("Image not assessed previously by Tenable.io CS")
            i.image.tag(f"registry.cloud.tenable.com/{i.image.tags[0]}")
            #target_image = docker_client.images.get(f"registry.cloud.tenable.com/{i.image.tags[0]}")
            docker_client.images.push(f"registry.cloud.tenable.com/{i.image.tags[0]}", auth_config={"username": tio_access_key, "password": tio_secret_key})
            print(f"Image should now be assessed in Tenable.io. Image pushed to registry.cloud.tenable.com/{i.image.tags[0]}")

