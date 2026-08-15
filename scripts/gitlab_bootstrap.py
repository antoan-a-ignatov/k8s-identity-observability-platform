import os
import sys
import requests

TOKEN = os.environ["GITLAB_TOKEN"]
PROJECT = os.environ["GITLAB_PROJECT"]
BASE = "https://gitlab.com/api/v4"
HEADERS = {"PRIVATE-TOKEN": TOKEN}


def project_id():
    r = requests.get(
        f"{BASE}/projects/{PROJECT.replace('/', '%2F')}", headers=HEADERS)
    r.raise_for_status()
    return r.json()["id"]


def me():
    r = requests.get(f"{BASE}/user", headers=HEADERS)
    r.raise_for_status()
    return r.json()["id"]


def create_milestone(pid, title, description):
    r = requests.post(
        f"{BASE}/projects/{pid}/milestones",
        headers=HEADERS,
        data={"title": title, "description": description},
    )
    r.raise_for_status()
    return r.json()


def close_milestone(pid, milestone_id):
    r = requests.put(
        f"{BASE}/projects/{pid}/milestones/{milestone_id}",
        headers=HEADERS,
        data={"state_event": "close"},
    )
    r.raise_for_status()


def create_issue(pid, title, description, milestone_id, assignee_id):
    r = requests.post(
        f"{BASE}/projects/{pid}/issues",
        headers=HEADERS,
        data={
            "title": title,
            "description": description,
            "milestone_id": milestone_id,
            "assignee_ids": [assignee_id],
        },
    )
    r.raise_for_status()
    return r.json()


MILESTONES = [
    ("M1 - CI Pipeline & Runner", "self-hosted runner, .gitlab-ci.yml, green pipeline"),
    ("M2 - Cluster & Data Layer", "kind cluster, namespaces, PostgreSQL, backup script"),
    ("M3 - Identity", "Keycloak, Postgres wiring, realm/client, HA doc"),
    ("M4 - Application Integration", "app behind Keycloak, SSO verified"),
    ("M5 - GitOps Cutover", "ArgoCD install, manifest migration, sync verified"),
    ("M6 - Observability", "Elasticsearch, Fluent Bit, Logstash, Kibana"),
    ("M7 - Automation & Hardening", "health-check script, secrets review, second MR"),
    ("M8 - Documentation & Wrap-up",
     "README, screenshots, planned improvements, teardown"),
]

M2_ISSUES = [
    ("Smoke test resource baseline (kind + Elasticsearch only)",
      "Bring up empty kind cluster, deploy Elasticsearch alone, monitor free -h / docker stats before adding other components."),
    ("Create kind cluster and namespaces",
      "Provision kind cluster. Create namespaces: app, identity, data, logging."),
    ("Deploy PostgreSQL, init DB and user",
     "Deploy PostgreSQL into data namespace. Initialize database and user for Keycloak backend."),
    ("Python backup script (pg_dump)",
     "Write pg_dump-based backup script. Run once manually to confirm output."),
]

def main():
    pid = project_id()
    uid = me()
    created = {}
    for title, desc in MILESTONES:
        m = create_milestone(pid, title, desc)
        created[title] = m["id"]
        print(f"created milestone: {title} (id={m['id']})")

    close_milestone(pid, created["M1 - CI Pipeline & Runner"])
    print("closed M1 (already done)")

    m2_id = created["M2 - Cluster & Data Layer"]
    for title, desc in M2_ISSUES:
        i = create_issue(pid, title, desc, m2_id, uid)
        print(f"created issue: {title} (iid={i['iid']})")

if __name__ == "__main__":
    main()
