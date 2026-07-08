#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function simulateApiCall(job) {
  // Deterministic failure behavior for demo/testing purposes.
  const shouldFail = job.failuresBeforeSuccess && job.attempt <= job.failuresBeforeSuccess;
  await sleep(80);
  if (shouldFail) {
    throw new Error(`Transient failure for ${job.id} on attempt ${job.attempt}`);
  }
  return { id: job.id, status: "processed", payload: job.payload };
}

async function processWithRetry(job, maxRetries, baseBackoffMs) {
  let attempt = 0;
  while (attempt <= maxRetries) {
    attempt += 1;
    try {
      const result = await simulateApiCall({ ...job, attempt });
      return { ok: true, attempt, result };
    } catch (error) {
      if (attempt > maxRetries) {
        return { ok: false, attempt, error: error.message };
      }
      const backoff = baseBackoffMs * 2 ** (attempt - 1);
      await sleep(backoff);
    }
  }
  return { ok: false, attempt, error: "Unexpected retry loop exit" };
}

async function run() {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error("Usage: node process_jobs.js <jobs.json>");
    process.exit(1);
  }

  const resolvedInputPath = path.resolve(inputPath);
  if (!fs.existsSync(resolvedInputPath)) {
    console.error(`Input file not found: ${resolvedInputPath}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(resolvedInputPath, "utf-8");
  const config = JSON.parse(raw);
  const jobs = config.jobs || [];
  const maxRetries = config.maxRetries ?? 2;
  const baseBackoffMs = config.baseBackoffMs ?? 100;

  const summary = {
    totalJobs: jobs.length,
    succeeded: 0,
    failed: 0,
    results: [],
  };

  for (const job of jobs) {
    const outcome = await processWithRetry(job, maxRetries, baseBackoffMs);
    if (outcome.ok) {
      summary.succeeded += 1;
      console.log(`[SUCCESS] ${job.id} attempt=${outcome.attempt}`);
    } else {
      summary.failed += 1;
      console.log(`[FAILED] ${job.id} attempt=${outcome.attempt} error=${outcome.error}`);
    }
    summary.results.push({ jobId: job.id, ...outcome });
  }

  console.log("\nBatch Summary");
  console.log(JSON.stringify(summary, null, 2));
}

run().catch((error) => {
  console.error(`Fatal error: ${error.message}`);
  process.exit(1);
});
