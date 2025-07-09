# project-5

This repository contains a small Apache Beam streaming example. Data is read
from a Pub/Sub subscription, archived to Cloud Storage and written to BigQuery.

### Running the pipeline

```
python stream_pipeline.py
```

`stream_simulator.py` can be used to publish test events to the Pub/Sub topic.