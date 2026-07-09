# Incident Summary (Ruby sample)

This sample script reads incident data from a JSONL file and prints a quick operational summary:

- incident count
- incidents by severity
- incidents by service
- mean time to resolution
- unresolved incident IDs

## Run

```bash
cd ruby_samples/incident_summary
ruby summarize_incidents.rb sample_incidents.jsonl
```

Output JSON instead of text:

```bash
ruby summarize_incidents.rb --format json sample_incidents.jsonl
```

## Input format

Each line in the input file should be a JSON object like:

```json
{"id":"INC-101","service":"payments","severity":"critical","opened_at":"2026-07-07T10:00:00Z","resolved_at":"2026-07-07T10:42:00Z"}
```

`resolved_at` can be empty for open incidents.
