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
elif [ "$1" == "atribucion" ]; then
    echo "Building and pushing atribucion image"
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/atribucion:latest . -f atribucion.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/atribucion:latest
elif [ "$1" == "comisiones" ]; then
    echo "Building and pushing comisiones image"
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/comisiones:latest . -f comisiones.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/comisiones:latest
elif [ "$1" == "bff" ]; then
    echo "Building and pushing bff image"
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/bff:latest . -f bff.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/bff:latest
else
    echo "Building and pushing all images"
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/marketing:latest . -f marketing.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/marketing:latest
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/tracking:latest . -f tracking.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/tracking:latest
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/atribucion:latest . -f atribucion.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/atribucion:latest
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/comisiones:latest . -f comisiones.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/comisiones:latest
    docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/bff:latest . -f bff.Dockerfile
    docker push us-central1-docker.pkg.dev/tutoriales-miso/alpespartners/bff:latest
fi

         