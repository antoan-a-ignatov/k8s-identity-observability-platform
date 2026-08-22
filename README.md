# GitOps Identity and Observability Platform

## Project Status

**Current Version:** 0.2.0

**Status:** Milestones 1 and 2 complete - self-hosted GitLab Runner registered, CI pipeline (lint, build, scan, push) running green on every push to main. kind cluster provisioned with namespaces, PostgreSQL deployed and operated, Python backup script verified. Identity, GitOps, and observability layers in progress.

## Introduction

Kubernetes-based platform demonstrating GitOps deployment, centralized logging, identity management, and CI/CD. Built to fill stack gaps from two target job listings (Junior DevOps Engineer; DevOps/Platform) not covered by other portfolio projects. The application is a minimal placeholder - the platform itself is the point.

## Table of Contents

1. [Skills Demonstrated](#skills-demonstrated)
2. [Architecture](#architecture)
3. [Repository Structure](#repository-structure)
4. [Technology Stack](#technology-stack)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Identity and Access](#identity-and-access)
7. [Observability](#observability)
8. [Portability](#portability)
9. [Engineering Challenges and Design Decisions](#engineering-challenges-and-design-decisions)
10. [Planned Improvements](#planned-improvements)
11. [AI Diligence Statement](#ai-diligence-statement)

## Skills Demonstrated

- GitLab CI/CD pipeline design, running on a self-hosted runner (no shared runner dependency)
- GitOps deployment workflow with ArgoCD
- Identity and access management with Keycloak, backed by an operated PostgreSQL instance
- Centralized logging with the ELK stack
- Kubernetes cluster operation on a resource-constrained local machine
- Python automation for operational tasks (backup, health checks)
- SDLC practice via GitLab Issues, Milestones, and a branch/MR/squash-merge workflow

## Architecture

**LATER:** architecture diagram (mermaid) once GitOps cutover and identity layer are live.

## Repository Structure

```
app/                Placeholder Flask application
k8s/                Kubernetes manifests
  kind-config.yaml  Local cluster configuration
  namespaces.yaml   Namespace definitions (app, identity, data, logging)
  data/             PostgreSQL StatefulSet and Service
scripts/            Automation scripts (backup, health-check, environment bootstrap)
docs/               Documentation and screenshots
.gitlab-ci.yml       CI/CD pipeline definition
```

## Technology Stack

- **Cluster:** kind (local)
- **CI/CD:** GitLab CI/CD, self-hosted GitLab Runner
- **GitOps:** ArgoCD
- **Identity:** Keycloak
- **Database:** PostgreSQL
- **Logging:** ELK (Elasticsearch, Fluent Bit / Logstash, Kibana)
- **Automation:** Python
- **Repository:** GitLab (primary), mirrored to GitHub

## CI/CD Pipeline

Pipeline runs on a self-hosted GitLab Runner (Docker executor), avoiding any dependency on GitLab's shared runners or a credit card. Stages: lint (ruff) -> build (Docker) -> scan (Trivy) -> push (GitLab Container Registry). Push only runs on `main`, gated behind a required passing pipeline.

**LATER:** screenshot of a green pipeline run.

## Identity and Access
Keycloak runs in production/optimized mode as a single replica, wired to the
existing PostgreSQL instance via a dedicated `keycloak` database and role.
The image is built via a two-stage Dockerfile (pre-baking `kc.sh build` output)
and published through a dedicated CI job to GitLab's Container Registry, since
the stock Keycloak image doesn't support `start --optimized` out of the box.

A `platform` realm and `placeholder-app` client (confidential, standard flow)
are configured for the application's SSO login, to be wired up in Milestone 4.

HA is not run in this environment due to local resource constraints. Keycloak
supports HA via an external distributed cache (Infinispan or Redis) for shared
session state across replicas, avoiding sticky-session dependence on a single
pod. This would require an external Infinispan/Redis cluster, `KC_CACHE=ispn`
with remote-store configuration, and multiple replicas behind a load balancer
with no session affinity requirement.

**LATER:** screenshot of Keycloak login flow.

## Observability

**LATER:** ELK stack setup, log flow from cluster to Kibana, Fluent Bit and Logstash configurations (staged separately).

**LATER:** screenshot of Kibana dashboard.

## Portability

The environment is reproducible on a second machine via two bootstrap scripts (`scripts/bootstrap-windows.ps1`, `scripts/bootstrap-wsl.sh`), covering WSL2, native Docker, kind/kubectl/helm, and GitLab Runner setup end to end. See `docs/travel-laptop-setup.md` for the full walkthrough.

## Engineering Challenges and Design Decisions

**No credit card, no shared runners:** GitLab requires card verification to use shared runners on GitLab.com. Solved by running a self-hosted GitLab Runner locally instead, registered against the project with shared/instance runners explicitly disabled.

**RAM-constrained local environment:** Developing on an 8GB machine ruled out running the full stack concurrently. Components are staged up and down deliberately, with WSL2's memory cap raised to 6GB and swap enabled as a buffer. Verified with a smoke test: a kind cluster plus a single-node Elasticsearch instance (512Mi heap) left roughly 3.9Gi available after settling, confirming the staging strategy has headroom before heavier components are added.

**Runner token exposure:** A runner authentication token was inadvertently shared during setup. Rotated immediately via `gitlab-runner reset-token` before continuing.

**Secrets over plaintext:** PostgreSQL credentials are generated with a random password and created directly as a Kubernetes Secret (`kubectl create secret`), never written to a committed manifest. A Secret alone is only base64-encoded, not encrypted, so this is treated as a floor, not a solution. Vault or External Secrets Operator, listed under Planned Improvements, is the intended path to real encryption at rest.

**LATER:** Keycloak HA and ELK staging notes, once those milestones are complete.

## Planned Improvements

- KrakenD API Gateway in front of the Keycloak-protected app
- Docker Swarm administration (separate demo)
- MLOps / GPU workloads in Kubernetes (separate project)
- Keycloak HA: external session store (Infinispan/Redis)
- Production secrets management: Vault or External Secrets Operator

## AI Diligence Statement

An AI assistant was used throughout this project to augment learning and expedite execution: explaining concepts, drafting manifests and scripts for review, and troubleshooting. All architectural decisions, command execution, and verification of results were performed by the author.
