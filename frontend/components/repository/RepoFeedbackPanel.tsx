import { FeedbackResponse } from "@/lib/github";
import { Card } from "@/components/common/Card";

export function RepoFeedbackPanel({ feedback }: { feedback: FeedbackResponse }) {
  return (
    <div className="space-y-4">
      <Card eyebrow="What this does" title="Purpose">
        <p className="text-sm leading-relaxed text-ink/90">{feedback.repo_purpose}</p>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2">
        <Card eyebrow="Code" title="Quality">
          <p className="text-sm leading-relaxed text-ink/90">
            {feedback.code_quality_estimate}
          </p>
          {feedback.files_reviewed.length > 0 && (
            <p className="mt-3 font-mono text-xs text-muted">
              reviewed {feedback.files_reviewed.length} of{" "}
              {feedback.total_source_files_found} files
            </p>
          )}
        </Card>
        <Card eyebrow="README" title="Documentation">
          <p className="text-sm leading-relaxed text-ink/90">
            {feedback.documentation_quality}
          </p>
        </Card>
      </div>

      {feedback.suggested_improvements.length > 0 && (
        <Card eyebrow="Next moves" title="Suggested improvements">
          <ul className="space-y-2">
            {feedback.suggested_improvements.map((item, i) => (
              <li key={i} className="flex gap-3 text-sm text-ink/90">
                <span className="mt-0.5 text-ember">→</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {feedback.missing_evidence_notes.length > 0 && (
        <Card eyebrow="Honest gaps" title="Could not be assessed">
          <ul className="space-y-2">
            {feedback.missing_evidence_notes.map((item, i) => (
              <li key={i} className="text-sm text-muted">
                {item}
              </li>
            ))}
          </ul>
        </Card>
      )}
    </div>
  );
}