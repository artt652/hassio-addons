# Source: https://github.com/louislam/dockge/blob/master/docker/Dockerfile

############################################
# Healthcheck Binary
############################################
FROM louislam/dockge:build-healthcheck AS build_healthcheck

############################################
# Build
############################################
FROM louislam/dockge:base AS build
WORKDIR /app
COPY --chown=node:node ./package.json ./package.json
COPY --chown=node:node ./package-lock.json ./package-lock.json
RUN npm ci --omit=dev

############################################
# ⭐ Main Image
############################################
FROM louislam/dockge:base AS release
WORKDIR /app
COPY --chown=node:node --from=build_healthcheck /app/extra/healthcheck /app/extra/healthcheck
COPY --from=build /app/node_modules /app/node_modules
COPY --chown=node:node . .

# Создаём постоянный каталог данных для Home Assistant
RUN mkdir -p /data/addons_config/dockge/data
RUN rm -rf /app/data && ln -s /data/addons_config/dockge/data /app/data

# отключаем io_uring (см. оригинальный Dockerfile)
ENV UV_USE_IO_URING=0

# Объявляем том (для совместимости, но основной путь через /data/addons_config)
VOLUME /data

EXPOSE 5001
HEALTHCHECK --interval=60s --timeout=30s --start-period=60s --retries=5 CMD extra/healthcheck
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["tsx", "./backend/index.ts"]

############################################
# Mark as Nightly
############################################
FROM release AS nightly
RUN npm run mark-as-nightly