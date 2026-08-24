terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }

  required_version = ">= 1.5.0"
}

provider "google" {
  project = "habot-devops-project-506510"
  region  = "asia-south1"
}

# =========================================================
# D0 - RAW LANDING GCS BUCKET
# =========================================================

resource "google_storage_bucket" "d0_raw_landing" {
  name     = "habot-d0-raw-landing-506510"
  location = "ASIA-SOUTH1"

  # IAM controls access instead of object ACLs
  uniform_bucket_level_access = true

  # Keep previous versions of objects
  versioning {
    enabled = true
  }

  # Prevent accidental public access
  public_access_prevention = "enforced"

  labels = {
    environment = "staging"
    data_layer  = "d0-raw"
    project     = "habot"
  }
}

# =========================================================
# D1 - STAGED / ENFORCED BIGQUERY DATASET
# =========================================================

resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id = "d1_staged_enforced"
  location   = "asia-south1"

  description = "Staged and enforced dataset for validated application data"

  labels = {
    environment = "staging"
    data_layer  = "d1-staged-enforced"
    project     = "habot"
  }
}

# =========================================================
# D1 - STUDENT DATA TABLE
# =========================================================

resource "google_bigquery_table" "student_data" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = "student_data"

  schema = jsonencode([
    {
      name = "student_id"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "student_name"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "parent_email"
      type = "STRING"
      mode = "REQUIRED"
    },
    {
      name = "needs_support"
      type = "BOOL"
      mode = "REQUIRED"
    }
  ])
}

# =========================================================
# DEDICATED SERVICE ACCOUNT
# =========================================================

resource "google_service_account" "data_pipeline" {
  account_id   = "habot-data-pipeline"
  display_name = "Habot Data Pipeline Service Account"
}

# =========================================================
# LEAST-PRIVILEGE ACCESS TO D0 RAW LANDING
# =========================================================

resource "google_storage_bucket_iam_member" "raw_landing_viewer" {
  bucket = google_storage_bucket.d0_raw_landing.name

  role = "roles/storage.objectViewer"

  member = "serviceAccount:${google_service_account.data_pipeline.email}"

  # Restrict the permission to objects inside this bucket
  condition {
    title       = "RawLandingAccess"
    description = "Allow the data pipeline to access objects in the D0 raw landing bucket."

    expression = "resource.name.startsWith('projects/_/buckets/${google_storage_bucket.d0_raw_landing.name}/objects/')"
  }
}

# =========================================================
# BIGQUERY ROW-LEVEL SECURITY
# =========================================================
#
# ASSUMPTION:
# The hiring document requires RLS but does not define
# the exact business rule.
#
# For our demonstration, the data pipeline can access
# only rows where needs_support = TRUE.
#
# This assumption should be documented in the final
# project documentation/presentation.
# =========================================================

resource "google_bigquery_row_access_policy" "student_data_rls" {
  dataset_id = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id   = google_bigquery_table.student_data.table_id
  policy_id  = "student_data_access"

  filter_predicate = "needs_support = TRUE"

  grantees = [
    "serviceAccount:${google_service_account.data_pipeline.email}"
  ]
}