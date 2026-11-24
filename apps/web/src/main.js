import { callPythonApi, retryAsync } from "@repo/js-helpers";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const itemsInput = document.getElementById("items-input");
const batchSizeInput = document.getElementById("batch-size");
const runBtn = document.getElementById("run-btn");
const outputEl = document.getElementById("output");

async function handleBatchSummary() {
  const items = itemsInput.value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);

  const batchSize = Number.parseInt(batchSizeInput.value, 10) || 2;

  if (items.length === 0) {
    outputEl.textContent = "Please enter at least one comma-separated item.";
    return;
  }

  runBtn.disabled = true;
  outputEl.textContent = "Calling FastAPI service...";

  try {
    const result = await retryAsync(
      () =>
        callPythonApi(API_BASE_URL, "/api/batch-summary", {
          items,
          batch_size: batchSize,
        }),
      { retries: 2, delayMs: 200 },
    );

    outputEl.textContent = JSON.stringify(result, null, 2);
  } catch (err) {
    outputEl.textContent = `Request failed:\n${err.message}\n\nMake sure FastAPI is running on ${API_BASE_URL}.`;
  } finally {
    runBtn.disabled = false;
  }
}

runBtn.addEventListener("click", handleBatchSummary);
