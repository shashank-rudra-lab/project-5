provider "google" {
  project = "silent-octagon-460701-a0"
  region  = "us-central1"
}

# Pub/Sub Topic
resource "google_pubsub_topic" "stream_topic" {
  name = "stream-topic"
}

# Cloud Storage Bucket
resource "google_storage_bucket" "stream_bucket" {
  name          = "stream-topic-bucket"
  location      = "us-central1"
  force_destroy = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # Days
    }
  }
}

# BigQuery Dataset
resource "google_bigquery_dataset" "stream_dataset" {
  dataset_id    = "stream_topic_dataset"
  friendly_name = "Stream processing dataset"
  description   = "Dataset for processed streaming data"
  location      = "us-central1"
}

# BigQuery Table
resource "google_bigquery_table" "stream_table" {
  dataset_id = google_bigquery_dataset.stream_dataset.dataset_id
  table_id   = "stream_topic_table1"

  time_partitioning {
    type = "DAY"  # Recommended for streaming data
  }

  schema = <<EOF
[
  {
    "name": "userid",
    "type": "NUMERIC",
    "mode": "REQUIRED"
  },
  {
    "name": "action",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "product",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "timestamp",
    "type": "TIMESTAMP",
    "mode": "REQUIRED"
  }
]
EOF
}



data "google_project" "project" {}