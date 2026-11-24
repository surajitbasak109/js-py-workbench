import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  callPythonApi,
  debounce,
  retryAsync,
  safeJsonParse,
} from "./helpers.js";

describe("retryAsync", () => {
  it("succeeds after transient failures within retry budget", async () => {
    let attempts = 0;
    const result = await retryAsync(
      async () => {
        attempts += 1;
        if (attempts < 3) {
          throw new Error("temporary network hiccup");
        }
        return "recovered";
      },
      { retries: 3, delayMs: 10 },
    );

    assert.equal(result, "recovered");
    assert.equal(attempts, 3);
  });

  it("throws the last error once retries are exhausted", async () => {
    let attempts = 0;
    await assert.rejects(
      () =>
        retryAsync(
          async () => {
            attempts += 1;
            throw new Error("always fails");
          },
          { retries: 2, delayMs: 10 },
        ),
      /always fails/,
    );
    assert.equal(attempts, 3);
  });
});

describe("safeJsonParse", () => {
  it("parses valid JSON strings", () => {
    assert.deepEqual(safeJsonParse('{"ok":true,"count":2}'), {
      ok: true,
      count: 2,
    });
  });

  it("returns fallback on invalid JSON or non-strings", () => {
    assert.deepEqual(safeJsonParse("{bad json", { fallback: true }), {
      fallback: true,
    });
    assert.equal(safeJsonParse(undefined, null), null);
  });
});

describe("debounce", () => {
  it("collapses rapid calls and invokes once with the latest arguments", async () => {
    const calls = [];
    const debounced = debounce((val) => calls.push(val), 30);

    debounced("first");
    debounced("second");
    debounced("third");

    assert.equal(calls.length, 0);
    await new Promise((r) => setTimeout(r, 60));
    assert.deepEqual(calls, ["third"]);
  });
});

describe("callPythonApi", () => {
  it("sends a POST payload and parses JSON response", async () => {
    const originalFetch = globalThis.fetch;
    let capturedUrl = "";
    let capturedInit = null;

    globalThis.fetch = async (url, init) => {
      capturedUrl = url;
      capturedInit = init;
      return {
        ok: true,
        json: async () => ({ batch_count: 2 }),
      };
    };

    try {
      const data = await callPythonApi(
        "http://127.0.0.1:8000/",
        "/api/batch-summary",
        {
          items: ["a", "b", "c"],
          batch_size: 2,
        },
      );

      assert.equal(capturedUrl, "http://127.0.0.1:8000/api/batch-summary");
      assert.equal(capturedInit.method, "POST");
      assert.equal(capturedInit.headers["Content-Type"], "application/json");
      assert.deepEqual(data, { batch_count: 2 });
    } finally {
      globalThis.fetch = originalFetch;
    }
  });

  it("throws a descriptive error on non-OK HTTP responses", async () => {
    const originalFetch = globalThis.fetch;
    globalThis.fetch = async () => ({
      ok: false,
      status: 422,
      text: async () => "Invalid batch_size",
    });

    try {
      await assert.rejects(
        () => callPythonApi("http://127.0.0.1:8000", "/api/batch-summary", {}),
        /Python API error \(422\): Invalid batch_size/,
      );
    } finally {
      globalThis.fetch = originalFetch;
    }
  });
});
