import { RepoSummary } from "@/lib/github";

export function RepoCard({
  repo,
  onSelect,
}: {
  repo: RepoSummary;
  onSelect: (repo: RepoSummary) => void;
}) {
  return (
    <button
      onClick={() => onSelect(repo)}
      className="focus-ring group w-full rounded-lg border border-border bg-surface p-5 text-left transition-colors hover:border-ember/50 hover:bg-surfaceRaised"
    >
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h4 className="truncate font-mono text-sm text-ink group-hover:text-ember">
            {repo.repo_name}
          </h4>
          <p className="mt-1 line-clamp-2 text-sm text-muted">
            {repo.description || "No description provided."}
          </p>
        </div>
        <div className="flex shrink-0 items-center gap-3 text-xs text-muted">
          <span>★ {repo.stars}</span>
          <span>⑂ {repo.forks}</span>
        </div>
      </div>
      <div className="mt-3 flex items-center gap-2 font-mono text-[11px] text-muted">
        {repo.primary_language && (
          <span className="rounded border border-border px-2 py-0.5">
            {repo.primary_language}
          </span>
        )}
        {repo.updated_at && (
          <span>updated {new Date(repo.updated_at).toLocaleDateString()}</span>
        )}
      </div>
    </button>
  );
}