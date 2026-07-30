export function Spinner({ label }: { label?: string }) {
  return (
    <div className="flex items-center gap-3 text-muted">
      <div className="h-4 w-4 animate-spin rounded-full border-2 border-border border-t-ember" />
      {label && <span className="font-mono text-xs">{label}</span>}
    </div>
  );
}