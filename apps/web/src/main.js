import { callPythonApi, retryAsync } from "@repo/js-helpers";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

const itemsInput = document.getElementById("items-input");
const batchSizeInput = document.getElementById("batch-size");
const runBtn = document.getElementById("run-btn");
const outputEl = document.getElementById("output");

function renderBatchSummary(result) {
  const stats = result.char_stats;
  const previews = result.batch_previews
    .map(
      (batch) =>
        `  ${batch.batch_index + 1}. ${batch.item_count} items: ${batch.first_item} → ${batch.last_item}`,
    )
    .join("\n");

  outputEl.textContent = [
    `Items: ${result.total_items} (${result.non_empty_items} non-empty)`,
    `Batch size: ${result.batch_size}`,
    `Batch count: ${result.batch_count}`,
    `Character count: ${stats.total_chars} total, ${stats.min_chars} min, ${stats.max_chars} max, ${stats.avg_chars} average`,
    "",
    "Batch previews:",
    previews || "  No batches",
  ].join("\n");
}

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

    renderBatchSummary(result);
  } catch (err) {
    outputEl.textContent = `Request failed:\n${err.message}\n\nMake sure FastAPI is running on ${API_BASE_URL}.`;
  } finally {
    runBtn.disabled = false;
  }
}

runBtn.addEventListener("click", handleBatchSummary);
