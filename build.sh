#!/bin/bash

trap "exit" INT

VERSION=v0.0.17

declare -a architectures=("amd64" "arm64")

for architecture in "${architectures[@]}"; do
  echo "Building ${VERSION} for ${architecture}..."
  docker buildx build --platform linux/${architecture} --tag ibz0/stasi-${architecture}:${VERSION} --output "type=registry" .
done

echo "Creating manifest list..."
for architecture in "${architectures[@]}"; do
  echo " ibz0/stasi-${architecture}:${VERSION}"
done | xargs docker manifest create ibz0/stasi:${VERSION}

for architecture in "${architectures[@]}"; do
  echo "Annotating manifest for ${architecture}..."
  docker manifest annotate ibz0/stasi:${VERSION} ibz0/stasi-${architecture}:${VERSION} --arch ${architecture} --os linux
done

echo "Pushing manifest list..."
docker manifest push --purge ibz0/stasi:${VERSION}
