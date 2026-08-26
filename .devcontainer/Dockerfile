FROM ghcr.io/prefix-dev/pixi:v0.70.0 # pin pixi to avoid breaking changes

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt-get/lists/*