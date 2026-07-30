"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { getToken, clearToken, fetchCurrentUser, CurrentUser } from "@/lib/auth";
import {
  listUserRepos,
  getRepoFeedback,
  getCareerAnalysis,
  RepoSummary,
  FeedbackResponse,
  CareerAnalysisResponse,
} from "@/lib/github";
import { RepoCard } from "@/components/repository/RepoCard";
import { RepoFeedbackPanel } from "@/components/repository/RepoFeedbackPanel";
import { CareerAnalysisPanel } from "@/components/repository/CareerAnalysisPanel";
import { Card } from "@/components/common/Card";
import { Button } from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);

  const [viewingUsername, setViewingUsername] = useState<string>("");
  const [usernameInput, setUsernameInput] = useState<string>("");

  const [repos, setRepos] = useState<RepoSummary[]>([]);
  const [loadingRepos, setLoadingRepos] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [careerGoal, setCareerGoal] = useState("Backend Engineer");
  const [analysis, setAnalysis] = useState<CareerAnalysisResponse | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  const [selectedRepo, setSelectedRepo] = useState<RepoSummary | null>(null);
  const [feedback, setFeedback] = useState<FeedbackResponse | null>(null);
  const [loadingFeedback, setLoadingFeedback] = useState(false);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.replace("/");
      return;
    }

    fetchCurrentUser(token)
      .then((u) => {
        setUser(u);
        setViewingUsername(u.username);
        setUsernameInput(u.username);
      })
      .catch((err) => setError(err.message || "Something went wrong."));
  }, [router]);

  useEffect(() => {
    if (!viewingUsername) return;

    setLoadingRepos(true);
    setAnalysis(null);
    setSelectedRepo(null);
    setFeedback(null);
    setError(null);
    setRepos([]);

    listUserRepos(viewingUsername)
      .then((r) => setRepos(r))
      .catch((err) => {
        setRepos([]);
        setError(err.message || "Could not load that profile's repos.");
      })
      .finally(() => setLoadingRepos(false));
  }, [viewingUsername]);

  function extractGithubUsername(input: string): string {
    const trimmed = input.trim();
    const match = trimmed.match(/github\.com\/([^\/\s?#]+)/i);
    return match ? match[1] : trimmed;
  }

  function handleViewProfile() {
    const username = extractGithubUsername(usernameInput);
    if (!username) return;
    setUsernameInput(username);
    setViewingUsername(username);
  }

  function handleBackToMyProfile() {
    if (!user) return;
    setUsernameInput(user.username);
    setViewingUsername(user.username);
  }

  async function handleAnalyze() {
    if (!viewingUsername) return;
    setAnalyzing(true);
    setAnalysis(null);
    try {
      const result = await getCareerAnalysis(viewingUsername, careerGoal);
      setAnalysis(result);
    } catch (err: any) {
      setError(err.message || "Analysis failed.");
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleSelectRepo(repo: RepoSummary) {
    setSelectedRepo(repo);
    setFeedback(null);
    setLoadingFeedback(true);
    try {
      const result = await getRepoFeedback(repo.url);
      setFeedback(result);
    } catch (err: any) {
      setError(err.message || "Could not review this repo.");
    } finally {
      setLoadingFeedback(false);
    }
  }

  function handleLogout() {
    clearToken();
    router.replace("/");
  }

  if (!user) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-graphite">
        <Spinner label="loading" />
      </main>
    );
  }

  const isOwnProfile = viewingUsername === user.username;

  return (
    <main className="min-h-screen bg-graphite">
      <header className="flex items-center justify-between border-b border-border px-8 py-4">
        <span className="font-display text-lg text-ink">
          Skill<span className="text-ember">Forge</span>
        </span>
        <div className="flex items-center gap-3">
          {user.avatar_url && (
            <Image
              src={user.avatar_url}
              alt={user.username}
              width={28}
              height={28}
              className="rounded-full"
            />
          )}
          <span className="font-mono text-sm text-muted">{user.username}</span>
          <Button variant="ghost" onClick={handleLogout} className="px-3 py-1.5 text-xs">
            Log out
          </Button>
        </div>
      </header>

      <div className="mx-auto max-w-6xl px-8 py-10">
        {error && (
          <div className="mb-6 rounded-md border border-ember/40 bg-ember/10 px-4 py-3 text-sm text-ember">
            {error}
          </div>
        )}

        <Card eyebrow="Whose profile?" title="Look up any public GitHub profile">
          <div className="flex flex-wrap items-end gap-3">
            <div className="flex-1 min-w-[220px]">
              <label className="mb-1 block font-mono text-xs text-muted">
                github username
              </label>
              <input
                value={usernameInput}
                onChange={(e) => setUsernameInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleViewProfile()}
                placeholder="e.g. a friend's github username"
                className="focus-ring w-full rounded-md border border-border bg-surfaceRaised px-3 py-2 text-sm text-ink placeholder:text-muted"
              />
            </div>
            <Button onClick={handleViewProfile} disabled={!usernameInput.trim()}>
              View profile
            </Button>
            {!isOwnProfile && (
              <Button variant="ghost" onClick={handleBackToMyProfile}>
                Back to my profile
              </Button>
            )}
          </div>
          <p className="mt-3 font-mono text-[11px] text-muted">
            {isOwnProfile
              ? "Currently viewing your own profile."
              : `Currently viewing ${viewingUsername}'s public profile.`}
          </p>
        </Card>

        <div className="mt-6">
          <Card eyebrow="Step 2" title={`What is ${isOwnProfile ? "your" : `${viewingUsername}'s`} target role?`}>
            <div className="flex flex-wrap items-end gap-3">
              <div className="flex-1 min-w-[220px]">
                <label className="mb-1 block font-mono text-xs text-muted">
                  career goal
                </label>
                <input
                  value={careerGoal}
                  onChange={(e) => setCareerGoal(e.target.value)}
                  placeholder="e.g. Backend Engineer, AI Engineer"
                  className="focus-ring w-full rounded-md border border-border bg-surfaceRaised px-3 py-2 text-sm text-ink placeholder:text-muted"
                />
              </div>
              <Button onClick={handleAnalyze} disabled={analyzing || !careerGoal.trim()}>
                {analyzing ? "Reading the profile…" : "Analyze this profile"}
              </Button>
            </div>
          </Card>
        </div>

        {analyzing && (
          <div className="mt-6">
            <Spinner label="cross-referencing repos against the goal" />
          </div>
        )}

        {analysis && (
          <div className="mt-6">
            <CareerAnalysisPanel result={analysis} />
          </div>
        )}

        <div className="mt-10 grid gap-8 lg:grid-cols-[1fr_1.2fr]">
          <div>
            <h3 className="mb-4 font-mono text-xs uppercase tracking-wider text-muted">
              Repositories ({repos.length})
            </h3>
            {loadingRepos ? (
              <Spinner label="fetching repos" />
            ) : (
              <div className="space-y-3">
                {repos.map((repo) => (
                  <RepoCard key={repo.full_name} repo={repo} onSelect={handleSelectRepo} />
                ))}
                {repos.length === 0 && !error && (
                  <p className="text-sm text-muted">No public repositories found.</p>
                )}
              </div>
            )}
          </div>

          <div>
            <h3 className="mb-4 font-mono text-xs uppercase tracking-wider text-muted">
              {selectedRepo ? selectedRepo.repo_name : "Select a repo"}
            </h3>
            {!selectedRepo && (
              <Card>
                <p className="text-sm text-muted">
                  Click a repo on the left to get proactive AI feedback —
                  purpose, code quality, documentation, and what&apos;s
                  missing, whether you ask or not.
                </p>
              </Card>
            )}
            {loadingFeedback && <Spinner label="reviewing repository" />}
            {feedback && !loadingFeedback && <RepoFeedbackPanel feedback={feedback} />}
          </div>
        </div>
      </div>
    </main>
  );
}