FROM ghcr.io/prefix-dev/pixi:latest

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt-get/lists/*