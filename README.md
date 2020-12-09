# Connector for a Docker host to Tenable.io Container Security

This is only a sample application. It looks for any running containers on the Docker host and derives their image.
It then checks with Tenable.io Container Security to see if that image has been assessed.  If it has not been assessed,
it tags the image for a push to Tenable.io Container Security for assessment and then initiates the push.  
Image assessment results can then be seen in Tenable.io's web interface.


To run, make sure you have the following environment variables set:
```
export TIO_ACCESS_KEY=******
export TIO_SECRET_KEY=******
python3 tiocs-docker-connector.py 
```