# stasi

Collect data from various sensors and use [`rrdtool`](https://oss.oetiker.ch/rrdtool/doc/rrdtool.en.html) to generate graphs.

# Building

The Docker image can be built for Raspberry Pi using `docker buildx build --platform=linux/arm64 .`

# Pre-built images

You can run a pre-built image from Docker Hub directly on your Raspberry Pi using:

`docker run -v IMGDIR:/images -v DATADIR:/data -v ~/.ssh:/home/stasi/.ssh:ro --name stasi --rm -d -it ibz0/stasi:v0.0.1`

(Replace `IMGDIR` and `DATADIR` with two local directories. Also, make sure you have a SSH key in your `~/.ssh`.)

# Accessing the graphs

You can serve the graphs using

`docker run -p 8123:80 -v IMGDIR:/usr/share/nginx/html --name stasi-nginx --rm -d -it nginx`
