# simple_streaming_pipeline.py
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
import time

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
        # 1. Read from Pub/Sub
        messages = p | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(
            subscription='projects/silent-octagon-460701-a0/subscriptions/stream-topic-sub')
        


        # 2. Parse JSON (no error handling)
        parsed = (messages
                 | 'ParseJSON' >> beam.Map(lambda x: json.loads(x.decode('utf-8')))
                 )

        # 3. Write to BigQuery (new table and schema with timestamp as STRING)
        _ = (parsed
             | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                 table='silent-octagon-460701-a0:stream_topic_dataset.stream_topic_table2',
                 schema='user_id:INTEGER,action:STRING,product:STRING,timestamp:STRING',
                 create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                 write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
             )

      

if __name__ == '__main__':
    run()