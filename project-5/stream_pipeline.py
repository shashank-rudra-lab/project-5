# simple_streaming_pipeline.py
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam import window
import json

def run():
    options = PipelineOptions(
        runner='DataflowRunner',
        project='silent-octagon-460701-a0',
        region='us-central1',
        job_name='new-table',
        temp_location='gs://stream-topic-bucket/temp',
        streaming=True
    )

    with beam.Pipeline(options=options) as p:
        # 1. Read from Pub/Sub and decode bytes to string
        messages = (
            p
            | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(
                subscription='projects/silent-octagon-460701-a0/subscriptions/stream-topic-sub'
            ).with_output_types(bytes)
            | 'DecodeMessage' >> beam.Map(lambda x: x.decode('utf-8'))
        )

        # 2. Write raw data to Cloud Storage using windowing to avoid
        #    GroupByKey errors with unbounded data
        _ = (
            messages
            | 'WindowRawMessages' >> beam.WindowInto(window.FixedWindows(60))
            | 'WriteRawToGCS' >> beam.io.WriteToText(
                'gs://stream-topic-bucket/raw/messages',
                file_name_suffix='.json'
            )
        )

        # 3. Parse JSON
        parsed = messages | 'ParseJSON' >> beam.Map(json.loads)

        # 4. Write to BigQuery (new table and schema with timestamp as STRING)
        _ = (
            parsed
            | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table='silent-octagon-460701-a0:stream_topic_dataset.stream_topic_table2',
                schema='user_id:INTEGER,action:STRING,product:STRING,timestamp:STRING',
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

      

if __name__ == '__main__':    run()