FROM ghcr.io/prefix-dev/pixi:0.18.0 AS build

COPY . /app
WORKDIR /app
RUN pixi install --frozen --environment build
RUN pixi install --frozen --environment prod
RUN pixi run -e build -vv build-wheel
RUN pixi run -e prod -vv postinstall-production
RUN pixi shell-hook -e prod > /shell-hook
RUN echo 'pycashier "$@"' >> /shell-hook

# cleanup unnecessary files from environment to reduce image size
RUN bash docker/purge.sh

FROM debian:bookworm-slim as production

RUN groupadd -g 2009 pycashier && useradd -u 2009 -g 2009 pycashier
USER pycashier

# only copy the production environment into prod container
COPY --from=build /app/.pixi/envs/prod /app/.pixi/envs/prod
COPY --from=build /shell-hook /shell-hook
WORKDIR /data
ENTRYPOINT ["/bin/bash", "/shell-hook"]
