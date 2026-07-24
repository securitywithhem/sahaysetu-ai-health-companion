import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function ChronicTracker() {
  const [value, setValue] = useState("");
  const [trend, setTrend] = useState(null);

  const logReading = async () => {
    if (!value) return;
    const res = await fetch(`${API_BASE}/api/chronic/log`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        metric: "blood_sugar",
        value: Number(value),
        unit: "mg/dL",
        timestamp: new Date().toISOString(),
      }),
    });
    setTrend(await res.json());
    setValue("");
  };

  return (
    <div className="bg-white rounded-xl p-4 border space-y-3">
      <h2 className="font-semibold">Log today's blood sugar (mg/dL)</h2>
      <div className="flex gap-2">
        <input
          type="number"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          className="rounded-lg border px-3 py-2 flex-1"
          placeholder="e.g. 138"
        />
        <button
          onClick={logReading}
          className="rounded-lg bg-slate-900 text-white px-4 py-2 font-medium"
        >
          Log
        </button>
      </div>
      {trend && (
        <div
          className={`rounded-lg p-3 text-sm ${
            trend.unhealthy_trend ? "bg-yellow-50 border border-yellow-400" : "bg-green-50 border border-green-400"
          }`}
        >
          {trend.message}
        </div>
      )}
    </div>
  );
}
