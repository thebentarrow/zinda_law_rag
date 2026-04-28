# Deploying on GCP e2-standard-2 (Compute Engine)

This guide deploys the full application stack — FastAPI backend and React frontend — on a
single GCP Compute Engine VM using Docker Compose.

**Instance spec:** e2-standard-2 · 2 vCPU · 8 GB RAM · ~$49 / month  
**Estimated setup time:** 20 minutes

---

## Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and initialised
  (`gcloud init`)
- A GCP project with billing enabled
- Your OpenAI API key

All commands below run from your **local machine** unless prefixed with `[VM]`.

---

## 1. Create the VM

```bash
gcloud compute instances create zinda-law-demo \
  --project=YOUR_PROJECT_ID \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-standard \
  --tags=http-server,https-server
```

Replace `YOUR_PROJECT_ID` with your GCP project ID.

The `--tags` flag is used in step 2 to open port 80 via a firewall rule.

---

## 2. Open port 80 in the firewall

The frontend is served on port 80. If this rule does not already exist in your project:

```bash
gcloud compute firewall-rules create allow-http \
  --project=YOUR_PROJECT_ID \
  --allow=tcp:80 \
  --target-tags=http-server \
  --description="Allow HTTP traffic on port 80"
```

> Port 8000 (the backend API) does not need to be open publicly — the frontend container
> communicates with the backend over the Docker internal network.

---

## 3. SSH into the instance

```bash
gcloud compute ssh zinda-law-demo \
  --zone=us-central1-a \
  --project=YOUR_PROJECT_ID
```

All steps from here are run **inside the VM**.

---

## 4. Install Docker

```bash
# [VM] Install Docker CE
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

# Allow the current user to run Docker without sudo
sudo usermod -aG docker $USER
newgrp docker
```

Verify the installation:

```bash
docker --version
docker compose version
```

---

## 5. Clone the repository

```bash
# [VM]
git clone https://github.com/thebentarrow/zinda_law_rag.git
cd zinda_law_rag
```

---

## 6. Create the environment file

```bash
# [VM] — copy the example and fill in your values
cp .env.example .env
nano .env
```

Minimum required values to set:

```
OPENAI_API_KEY=sk-...          # your OpenAI key
CORS_ORIGINS=http://EXTERNAL_IP,http://localhost:5173,http://localhost
```

To find the external IP of your VM:

```bash
# [VM]
curl -s http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip \
  -H "Metadata-Flavor: Google"
```

Save and close the file (`Ctrl+X` → `Y` → `Enter` in nano).

---

## 7. Add a persistent cache volume for docling models

Docling downloads its layout model (~400 MB) on the first document upload. Adding a named
volume for the cache means the model survives container rebuilds.

Add the following to `docker-compose.yml` before deploying (the `volumes:` block at the
bottom of the file already exists — just add the new entry):

```yaml
services:
  backend:
    # ... existing config ...
    volumes:
      - app_data:/data
      - docling_cache:/root/.cache   # add this line

volumes:
  app_data:
  docling_cache:                     # add this line
```

---

## 8. Build and start the containers

```bash
# [VM] — from inside the zinda_law_rag directory
docker compose up -d --build
```

The first build takes 5–10 minutes (installs Python dependencies including docling).
Subsequent starts reuse the cached layers and take under a minute.

Check that both containers are running:

```bash
docker compose ps
```

Expected output:

```
NAME                        STATUS
zinda_law_rag-backend-1     Up
zinda_law_rag-frontend-1    Up
```

---

## 9. Verify the deployment

Check the backend health endpoint:

```bash
curl http://localhost:8000/api/health
```

Expected response:

```json
{"status":"ok","chat_model":"gpt-4o-mini","embedding_model":"text-embedding-3-small",...}
```

Then open the app in a browser using the external IP from step 6:

```
http://EXTERNAL_IP
```

---

## 10. Viewing logs

```bash
# [VM] — tail live logs from both containers
docker compose logs -f

# backend only
docker compose logs -f backend

# frontend only
docker compose logs -f frontend
```

---

## Stopping and restarting

### Stop the containers (keep the VM running)

Stops the app but keeps the VM alive and billable:

```bash
# [VM]
docker compose down
```

Data in the `app_data` and `docling_cache` volumes is preserved.

### Stop the VM (pause billing)

Stops the VM entirely. You are no longer charged for compute, but the
**persistent disk (~$1.20/month for 30 GB) continues to accrue a small charge**.

```bash
# local machine
gcloud compute instances stop zinda-law-demo \
  --zone=us-central1-a \
  --project=YOUR_PROJECT_ID
```

### Restart the VM after stopping

```bash
# local machine
gcloud compute instances start zinda-law-demo \
  --zone=us-central1-a \
  --project=YOUR_PROJECT_ID
```

> **Note:** The external IP changes each time the VM starts unless you reserve a static IP
> (see below). Remember to update `CORS_ORIGINS` in `.env` with the new IP and run
> `docker compose up -d` after restarting.

### Start the containers after a VM restart

```bash
# local machine — SSH back in
gcloud compute ssh zinda-law-demo --zone=us-central1-a --project=YOUR_PROJECT_ID

# [VM]
cd zinda_law_rag
docker compose up -d
```

### Delete the VM entirely (stop all charges)

```bash
# local machine
gcloud compute instances delete zinda-law-demo \
  --zone=us-central1-a \
  --project=YOUR_PROJECT_ID
```

This permanently deletes the VM and its boot disk. The Docker volumes (app data, docling
cache) are stored on the boot disk and will also be deleted. Back up the SQLite database
first if needed:

```bash
# [VM] — copy the database to your local machine before deleting
gcloud compute scp zinda-law-demo:/var/lib/docker/volumes/zinda_law_rag_app_data/_data/app.db \
  ./app_backup.db \
  --zone=us-central1-a \
  --project=YOUR_PROJECT_ID
```

---

## Optional: Reserve a static external IP

Reserving a static IP means it does not change when the VM is stopped and restarted,
avoiding the need to update `.env` each time.

```bash
# Reserve a static IP
gcloud compute addresses create zinda-law-ip \
  --region=us-central1 \
  --project=YOUR_PROJECT_ID

# Assign it to the VM
gcloud compute instances delete-access-config zinda-law-demo \
  --access-config-name="External NAT" \
  --zone=us-central1-a \
  --project=YOUR_PROJECT_ID

gcloud compute instances add-access-config zinda-law-demo \
  --access-config-name="External NAT" \
  --address=$(gcloud compute addresses describe zinda-law-ip \
    --region=us-central1 --format="value(address)") \
  --zone=us-central1-a \
  --project=YOUR_PROJECT_ID
```

A reserved static IP costs ~$0.01/hour when not attached to a running VM.

---

## Cost summary

| Resource | Active | Stopped |
|---|---|---|
| e2-standard-2 compute | ~$0.067/hr (~$49/mo) | $0 |
| 30 GB pd-standard disk | ~$1.20/mo | ~$1.20/mo |
| Static IP (optional) | $0 | ~$0.01/hr |
| Egress / API calls | Variable | $0 |
