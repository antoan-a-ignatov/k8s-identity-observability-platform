# Identity and Observability Platform

A Kubernetes-based platform demonstrating GitOps deployment, centralized logging, identity management, and CI/CD using GitLab, ArgoCD, Keycloak, PostgreSQL and ELK.


identity-devops-platform/
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
