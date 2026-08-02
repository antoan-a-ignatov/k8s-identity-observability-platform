# Travel Laptop Setup

Bootstraps a fresh Windows 11 laptop to work on this project, using the scripts
in `scripts/setup/`. Assumes no prior WSL/Docker/tooling installed.

## 1. New laptop: run the Windows bootstrap script

Open PowerShell **as Administrator**:

```powershell
iwr -useb https://gitlab.com/your-username/k8s-identity-observability-platform/-/raw/main/scripts/setup/bootstrap-windows.ps1 -OutFile bootstrap-windows.ps1
.\bootstrap-windows.ps1
```

- Installing Ubuntu-24.04 opens a window asking for a username/password - fill it in.
- If the script says a reboot is needed, reboot and rerun the same command.

## 2. New laptop: run the WSL bootstrap script

Open the `Ubuntu-24.04` terminal:

```bash
curl -o bootstrap-wsl.sh https://gitlab.com/your-username/k8s-identity-observability-platform/-/raw/main/scripts/setup/bootstrap-wsl.sh
chmod +x bootstrap-wsl.sh
./bootstrap-wsl.sh
```

- If systemd wasn't already enabled, it'll tell you to run `wsl --shutdown` in
  PowerShell, reopen `Ubuntu-24.04`, and rerun this same script - safe to rerun.
- It'll print an SSH public key and pause - add it in GitLab under Edit profile
  > SSH Keys, then press Enter to continue.
- First SSH connection to GitLab asks to confirm a host fingerprint - type `yes`.
- It'll prompt for your git name/email - enter them.

## 3. Log out and back into the Ubuntu-24.04 terminal

Needed for Docker group membership to apply before running docker without sudo.

## 4. Register the GitLab Runner on this machine

In GitLab: Settings > CI/CD > Runners > New project runner. Tag it `travel-docker`
(distinct from the home PC's runner tag). Create it, copy the token, then:

```bash
sudo gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.com" \
  --token "PASTE_TOKEN_HERE" \
  --executor "docker" \
  --docker-image "docker:24.0.5"
```

## Not scriptable - manual either way

- VS Code + Remote-WSL extension, if you want that workflow (Windows-side,
  one-time install, no automation possible)
- When back home: restart the home PC's runner if it was stopped, and consider
  removing/disabling the travel laptop's runner once done with it
