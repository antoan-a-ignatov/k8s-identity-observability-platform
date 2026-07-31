# Identity and Observability Platform

> **Note:** This repository is mirrored from GitLab, where active development, CI/CD pipelines, and merge request history live: https://gitlab.com/your-username/k8s-identity-observability-platform

A Kubernetes-based platform demonstrating GitOps deployment, centralized logging, identity management, and CI/CD using GitLab, ArgoCD, Keycloak, PostgreSQL and ELK.

```
k8s-identity-observability-platform//
│
├── app/
│   ├── src/
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/
│   ├── app/
│   ├── argocd/
│   ├── logging/
│   ├── keycloak/
│   └── postgres/
│
├── scripts/
│
├── docs/
│   └── screenshots/
│
├── .gitignore
├── .gitlab-ci.yml
├── README.md
└── kind-config.yaml
```
