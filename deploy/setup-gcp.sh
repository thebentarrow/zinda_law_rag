#!/usr/bin/env bash
# Run once to provision GCP infrastructure.
# Usage: PROJECT_ID=your-project-id bash deploy/setup-gcp.sh

set -euo pipefail

PROJECT_ID="${PROJECT_ID:?Set PROJECT_ID}"
REGION="us-central1"
REPO="zinda-law"
SA_NAME="zinda-law-sa"
BUCKET="${PROJECT_ID}-zinda-law-data"

echo "==> Enabling APIs"
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  secretmanager.googleapis.com \
  storage.googleapis.com \
  --project="$PROJECT_ID"

echo "==> Creating Artifact Registry repository"
gcloud artifacts repositories create "$REPO" \
  --repository-format=docker \
  --location="$REGION" \
  --project="$PROJECT_ID" || true

echo "==> Creating service account"
gcloud iam service-accounts create "$SA_NAME" \
  --display-name="Zinda Law Runtime SA" \
  --project="$PROJECT_ID" || true

SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "==> Granting IAM roles"
for ROLE in roles/secretmanager.secretAccessor roles/storage.objectUser; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="$ROLE"
done

echo "==> Creating GCS bucket for persistent data"
gcloud storage buckets create "gs://${BUCKET}" \
  --location="$REGION" \
  --project="$PROJECT_ID" || true

echo "==> Creating Secret Manager secrets (edit values after creation)"
for SECRET in openai-api-key chat-model embedding-model; do
  gcloud secrets create "$SECRET" --replication-policy=automatic --project="$PROJECT_ID" || true
done

echo ""
echo "Done. Next steps:"
echo "  1. Populate secrets:  echo -n 'sk-...' | gcloud secrets versions add openai-api-key --data-file=-"
echo "  2. Populate model secrets similarly for chat-model (e.g. gpt-4o-mini) and embedding-model"
echo "  3. Update deploy/cloudbuild.yaml _PROJECT_ID substitution"
echo "  4. Connect your GitHub repo to Cloud Build and configure the trigger"
