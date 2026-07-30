import { CareerAnalysisResponse } from "@/lib/github";
import { Card } from "@/components/common/Card";

const readinessColor: Record<string, string> = {
  High: "text-good",
  Medium: "text-warn",
  Low: "text-ember",
  "Not applicable": "text-muted",
};

export function CareerAnalysisPanel({ result }: { result: CareerAnalysisResponse }) {
  const color = readinessColor[result.career_readiness.split(",")[0].trim()] || "text-muted";

  return (
    <div className="space-y-4">
      <Card eyebrow={`${result.repos_analyzed} repos analyzed`} title="Readiness">
        <p className={`font-display text-2xl ${color}`}>{result.career_readiness}</p>
        <p className="mt-3 text-sm leading-relaxed text-ink/90">{result.overall_summary}</p>
      </Card>

      <div className="grid gap-4 sm:grid-cols-3">
        <Card eyebrow="Evidence" title="Strengths">
          <ul className="space-y-2">
            {result.strengths.map((s, i) => (
              <li key={i} className="text-sm text-ink/90">
                {s}
              </li>
            ))}
          </ul>
        </Card>
        <Card eyebrow="Evidence" title="Weaknesses">
          <ul className="space-y-2">
            {result.weaknesses.map((w, i) => (
              <li key={i} className="text-sm text-ink/90">
                {w}
              </li>
            ))}
          </ul>
        </Card>
        <Card eyebrow="Build next" title="Missing skills">
          <ul className="space-y-2">
            {result.missing_skills.map((m, i) => (
              <li key={i} className="flex gap-2 text-sm text-ink/90">
                <span className="text-ember">→</span>
                {m}
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
}