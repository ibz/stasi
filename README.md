# stasi

Collect data from various sensors (see [`gan`](https://github.com/ibz/gan)) and use [`rrdtool`](https://oss.oetiker.ch/rrdtool/doc/rrdtool.en.html) to generate graphs.

My own home monitoring setup involves one instance of `stasi` running directly on my [Umbrel](https://getumbrel.com/), which syncs data from multiple Raspberry Pi Zero devices that collect data using `gan`.

## Running pre-built images

On [Umbrel](https://github.com/getumbrel/umbrel/) you can run `stasi` using `docker-compose up -d`. This will run a pre-built Docker image and mount `/mnt/data/umbrel/stasi/` and `/home/umbrel/.ssh`, which need to exist.

## Building

Build the Docker image yourself using `docker buildx build --platform=linux/arm64 .`

## TODO

I use this system for my own home monitoring setup and it works fine, but it might not work for everyone nor is it easy enough to install for everyone.
