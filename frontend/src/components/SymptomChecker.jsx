import { useState } from "react";
import TriageResult from "./TriageResult";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

const COMMON_SYMPTOMS = [
  "fever", "cough", "headache", "chest pain", "difficulty breathing",
  "vomiting", "diarrhea", "sore throat", "fatigue", "rash",
];

export default function SymptomChecker() {
  const [selected, setSelected] = useState([]);
  const [durationDays, setDurationDays] = useState(1);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const toggle = (symptom) => {
    setSelected((prev) =>
      prev.includes(symptom) ? prev.filter((s) => s !== symptom) : [...prev, symptom]
    );
  };

  const submit = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/api/triage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          symptoms: selected,
          vitals: {},
          duration_days: durationDays,
          language: "en",
        }),
      });
      if (!res.ok) throw new Error("Request failed");
      setResult(await res.json());
    } catch (e) {
      setError("Could not reach the triage service. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl p-4 border">
        <h2 className="font-semibold mb-3">What symptoms are you experiencing?</h2>
        <div className="flex flex-wrap gap-2">
          {COMMON_SYMPTOMS.map((s) => (
            <button
              key={s}
              onClick={() => toggle(s)}
              className={`px-3 py-1.5 rounded-full text-sm border ${
                selected.includes(s)
                  ? "bg-slate-900 text-white border-slate-900"
                  : "bg-white border-slate-300"
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        <label className="block mt-4 text-sm font-medium">
          How many days have symptoms lasted?
          <input
            type="number"
            min={0}
            value={durationDays}
            onChange={(e) => setDurationDays(Number(e.target.value))}
            className="block mt-1 w-24 rounded-lg border px-2 py-1"
          />
        </label>

        <button
          onClick={submit}
          disabled={selected.length === 0 || loading}
          className="mt-4 w-full rounded-lg bg-slate-900 text-white py-2 font-medium disabled:opacity-40"
        >
          {loading ? "Checking..." : "Check my symptoms"}
        </button>
        {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
      </div>

      {result && <TriageResult result={result} />}
    </div>
  );
}
