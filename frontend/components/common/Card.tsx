import { ReactNode } from "react";

export function Card({
  title,
  eyebrow,
  children,
}: {
  title?: string;
  eyebrow?: string;
  children: ReactNode;
}) {
  return (
    <div className="rounded-lg border border-border bg-surface p-6">
      {eyebrow && (
        <div className="mb-1 font-mono text-[11px] uppercase tracking-wider text-ember">
          {eyebrow}
        </div>
      )}
      {title && <h3 className="mb-4 font-display text-lg text-ink">{title}</h3>}
      {children}
    </div>
  );
}