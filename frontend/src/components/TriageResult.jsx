const STYLES = {
  GREEN: { bg: "bg-green-50", border: "border-green-400", label: "HOME CARE" },
  YELLOW: { bg: "bg-yellow-50", border: "border-yellow-400", label: "CONSULT DOCTOR WITHIN 48 HOURS" },
  RED: { bg: "bg-red-50", border: "border-red-400", label: "VISIT HOSPITAL IMMEDIATELY" },
};

export default function TriageResult({ result }) {
  const style = STYLES[result.level] || STYLES.GREEN;

  return (
    <div className={`rounded-xl border-2 ${style.border} ${style.bg} p-4 space-y-2`}>
      <span className="inline-block text-xs font-bold uppercase tracking-wide px-2 py-1 rounded bg-white/70">
        {result.level}: {style.label}
      </span>
      <p className="text-sm">{result.explanation}</p>
      <p className="text-xs text-slate-600">
        Confidence: {(result.confidence * 100).toFixed(0)}%
      </p>
      {result.red_flags.length > 0 && (
        <p className="text-xs text-slate-600">
          Flags noticed: {result.red_flags.join(", ")}
        </p>
      )}
      <p className="text-sm font-medium mt-2">Next step: {result.recommended_next_step}</p>
    </div>
  );
}
