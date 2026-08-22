# Stage 1: build - produces the pre-built Keycloak artifacts kc.sh needs for --optimized
FROM quay.io/keycloak/keycloak:26.6.4 AS builder

# Build-time only options
ENV KC_DB=postgres
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

RUN /opt/keycloak/bin/kc.sh build

# Stage 2: Runtime
FROM quay.io/keycloak/keycloak:26.6.4
COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start", "--optimized"]
