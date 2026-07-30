import { Button } from "@/components/ui/Button";
import { githubLoginUrl } from "@/lib/auth";

export default function LandingPage() {
  return (
    <main className="flex min-h-screen flex-col">
      <header className="flex items-center justify-between px-8 py-6">
        <span className="font-display text-lg tracking-tight text-ink">
          Skill<span className="text-ember">Forge</span>
        </span>
      </header>

      <section className="mx-auto flex max-w-3xl flex-1 flex-col justify-center px-8 py-20">
        <p className="font-mono text-xs uppercase tracking-widest text-muted">
          not another github analytics tool
        </p>

        <h1 className="mt-6 font-display text-4xl leading-tight text-ink sm:text-5xl">
          Stop asking{" "}
          <span className="text-muted line-through decoration-ember/40">
            &ldquo;how many commits have I made?&rdquo;
          </span>
        </h1>
        <h2 className="mt-3 font-display text-4xl leading-tight text-ember sm:text-5xl">
          Start asking what to build next.
        </h2>

        <p className="mt-6 max-w-xl text-base leading-relaxed text-muted">
          SkillForge reads your repos the way a senior engineer would — real
          strengths, honest gaps, and the exact skill you&apos;re missing for
          the job you actually want. No scores. No leaderboards. Evidence, or
          nothing.
        </p>

        <div className="mt-10">
          <a href={githubLoginUrl()}>
            <Button className="text-base">
              Log in with GitHub
              <span aria-hidden>→</span>
            </Button>
          </a>
        </div>

        <p className="mt-4 font-mono text-xs text-muted">
          public repos only · no data sold · read-only access
        </p>
      </section>

      <footer className="border-t border-border px-8 py-6">
        <p className="font-mono text-xs text-muted">
          strengths · weaknesses · missing skills — grounded in your actual
          code, never invented
        </p>
      </footer>
    </main>
  );
}