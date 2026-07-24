import { useState } from "react";
import SymptomChecker from "./components/SymptomChecker";
import ChronicTracker from "./components/ChronicTracker";

export default function App() {
  const [tab, setTab] = useState("triage");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">AI Health Companion</h1>
        <nav className="flex gap-2">
          <button
            className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
              tab === "triage" ? "bg-slate-900 text-white" : "bg-slate-100"
            }`}
            onClick={() => setTab("triage")}
          >
            Symptom Checker
          </button>
          <button
            className={`px-3 py-1.5 rounded-lg text-sm font-medium ${
              tab === "chronic" ? "bg-slate-900 text-white" : "bg-slate-100"
            }`}
            onClick={() => setTab("chronic")}
          >
            Chronic Tracker
          </button>
        </nav>
      </header>

      <main className="max-w-2xl mx-auto p-6">
        {tab === "triage" ? <SymptomChecker /> : <ChronicTracker />}
        <p className="text-xs text-slate-400 mt-8 text-center">
          This app assists — it never diagnoses. In an emergency, call your local
          emergency number immediately.
        </p>
      </main>
    </div>
  );
}
