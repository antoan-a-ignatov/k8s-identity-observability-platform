import os
import requests

TOKEN = os.environ["GITLAB_TOKEN"]
PID = os.environ["GITLAB_PID"]
BASE = "https://gitlab.com/api/v4"
HEADERS = {"PRIVATE-TOKEN": TOKEN}

UPDATES = {
    7556311: (
        "2. Cluster and Data Layer",
        "Resource baseline smoke test (empty kind cluster plus Elasticsearch alone, "
        "checked against free -h and docker stats), kind cluster created with namespaces "
        "(app, identity, data, logging), PostgreSQL deployed and initialized. "
        "Deliverable: Python backup script (pg_dump) run once manually and confirmed.\n\n"
        "Estimated: 3h",
    ),
    7556312: (
        "3. Identity",
        "Keycloak deployed in production/optimized mode as a single replica, wired to "
        "Postgres, realm and client created for the app. Deliverable: HA design "
        "(Infinispan/Redis) documented in README as deferred.\n\n"
        "Estimated: 3h",
    ),
    7556313: (
        "4. Application Integration",
        "App deployed manually behind Keycloak, end-to-end SSO login flow verified. "
        "Deliverable: initial SSO login screenshot.\n\n"
        "Estimated: 2h",
    ),
    7556314: (
        "5. GitOps Cutover",
        "ArgoCD installed in-cluster, app and Keycloak manifests moved to the Git repo "
        "ArgoCD watches, manual deploys replaced with ArgoCD sync. Deliverable: GitOps "
        "loop verified (edit manifest -> commit -> auto-sync).\n\n"
        "Estimated: 3h",
    ),
    7556315: (
        "6. Observability",
        "Elasticsearch deployed with heap capped as a single node, Fluent Bit deployed "
        "and verified, swapped to Logstash (non-concurrent) and verified. Deliverable: Kibana "
        "deployed with dashboard screenshots, staged up only when needed.\n\n"
        "Estimated: 4h",
    ),
    7556316: (
        "7. Automation and Hardening",
        "Python ArgoCD sync and health-check script written, secrets review completed "
        "(Postgres creds, Keycloak admin in K8s Secrets, not plaintext). "
        "Deliverable: second MR demonstrating full SDLC workflow "
        "(issue -> branch -> MR -> checks -> squash merge).\n\n"
        "Estimated: 2h",
    ),
    7556317: (
        "8. Documentation and Wrap-up",
        "README updated with architecture summary and component walkthrough, "
        "screenshots added (Kibana, ArgoCD sync, Keycloak login), Planned "
        "Improvements section added. Deliverable: teardown performed and rebuild steps "
        "documented.\n\n"
        "Estimated: 2h",
    ),
}

for milestone_id, (title, description) in UPDATES.items():
    r = requests.put(
        f"{BASE}/projects/{PID}/milestones/{milestone_id}",
        headers=HEADERS,
        data={"title": title, "description": description},
    )
    r.raise_for_status()
    print(f"updated {milestone_id}: {title}")
