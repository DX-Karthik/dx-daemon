# Retry Batch Runner (JavaScript sample)

This sample demonstrates a practical backend use case: processing a batch of jobs with retry and exponential backoff.

## What it shows

- per-job retry logic
- exponential backoff between attempts
- success/failure summary output for the batch
- deterministic failure simulation for testing behavior

## Run

```bash
cd javascript_samples/retry_batch_runner
node process_jobs.js sample_jobs.json
```

## Input format

The JSON file should look like:

```json
{
  "maxRetries": 3,
  "baseBackoffMs": 100,
  "jobs": [
    { "id": "job-101", "payload": { "task": "sync-users" }, "failuresBeforeSuccess": 0 }
  ]
}
```

`failuresBeforeSuccess` is only for this sample to emulate transient failures.
