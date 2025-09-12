#!/bin/bash
# Script to build and push images to GCR
# It can receive the name of the image as an argument between "marketing" and "tracking"
# If no argument is provided, it will build and push all images
# If the argument is "marketing", it will build and push the marketing image
# If the argument is "tracking", it will build and push the tracking image

if [ "$1" == "marketing" ]; then
    echo "Building and pushing marketing image"
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/marketing:latest . -f marketing.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/marketing:latest
elif [ "$1" == "tracking" ]; then
    echo "Building and pushing tracking image"
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/tracking:latest . -f tracking.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/tracking:latest
else
    echo "Building and pushing all images"
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/marketing:latest . -f marketing.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/marketing:latest
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/tracking:latest . -f tracking.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/tracking:latest
fi

         