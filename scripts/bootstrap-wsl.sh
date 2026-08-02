#!/bin/bash
# bootstrap-wsl.sh
set -e

echo "=== Checking systemd ==="
if [ "$(ps -p 1 -o comm=)" != "systemd" ]; then
    echo "systemd not active. Writing /etc/wsl.conf..."
    if ! grep -q "\[boot\]" /etc/wsl.conf 2>/dev/null; then
        echo -e "[boot]\nsystemd=true" | sudo tee -a /etc/wsl.conf
    fi
    echo "Now run 'wsl --shutdown' in PowerShell, reopen Ubuntu-24.04, and rerun this script."
    exit 0
fi

echo "=== Installing Docker (native) ==="
if ! command -v docker &> /dev/null; then
    sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    sudo apt update
    sudo apt install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo systemctl enable --now docker
    sudo usermod -aG docker "$(whoami)"
    echo "Docker installed. You'll need to log out/in for group membership to apply."
else
    echo "Docker already installed, skipping."
fi

echo "=== Installing kind ==="
if ! command -v kind &> /dev/null; then
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
else
    echo "kind already installed, skipping."
fi

echo "=== Installing kubectl ==="
if ! command -v kubectl &> /dev/null; then
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    sudo mv kubectl /usr/local/bin/kubectl
else
    echo "kubectl already installed, skipping."
fi

echo "=== Installing helm ==="
if ! command -v helm &> /dev/null; then
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod +x get_helm.sh
    ./get_helm.sh
    rm -f get_helm.sh
else
    echo "helm already installed, skipping."
fi

echo "=== Installing gitlab-runner ==="
if ! command -v gitlab-runner &> /dev/null; then
    curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
    sudo apt install -y gitlab-runner
else
    echo "gitlab-runner already installed, skipping."
fi

echo "=== Git identity ==="
read -p "Git user.name: " GIT_NAME
read -p "Git user.email: " GIT_EMAIL
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"

echo "=== SSH key for GitLab ==="
if [ ! -f ~/.ssh/gitlab_ed25519 ]; then
    ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f ~/.ssh/gitlab_ed25519 -N ""
fi
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/gitlab_ed25519

mkdir -p ~/.ssh
if ! grep -q "Host gitlab.com" ~/.ssh/config 2>/dev/null; then
    cat >> ~/.ssh/config << 'EOF'
Host gitlab.com
  HostName gitlab.com
  User git
  IdentityFile ~/.ssh/gitlab_ed25519
EOF
fi

echo ""
echo "=== Add this public key to GitLab (Edit profile > SSH Keys), then press Enter ==="
cat ~/.ssh/gitlab_ed25519.pub
read -p "Press Enter once added..."

echo "=== Testing GitLab SSH connection (type 'yes' if prompted) ==="
ssh -T git@gitlab.com || true

echo "=== Cloning repo ==="
if [ ! -d ~/k8s-identity-observability-platform ]; then
    git clone git@gitlab.com:your-username/k8s-identity-observability-platform.git ~/k8s-identity-observability-platform
fi

echo ""
echo "=== Done ==="
echo "Next: log out/in for docker group, then register the runner manually"
echo "with a fresh token from GitLab (Settings > CI/CD > Runners > New project runner)."
