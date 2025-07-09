output "pubsub_topic" {
  value       = google_pubsub_topic.stream_topic.name
  description = "Pub/Sub topic name for streaming input"
}

output "gcs_bucket" {
  value       = google_storage_bucket.stream_bucket.name
  description = "GCS bucket name for raw data archive"
}

output "bigquery_table" {
  value       = "${google_bigquery_dataset.stream_dataset.dataset_id}.${google_bigquery_table.stream_table.table_id}"
  description = "Fully qualified BigQuery table name"
}


