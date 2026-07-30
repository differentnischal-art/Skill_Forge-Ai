"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { saveToken } from "@/lib/auth";
import { Spinner } from "@/components/ui/Spinner";

export default function AuthCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = searchParams.get("token");
    if (!token) {
      setError("No session token was returned. Please try logging in again.");
      return;
    }
    saveToken(token);
    router.replace("/dashboard");
  }, [searchParams, router]);

  return (
    <main className="flex min-h-screen items-center justify-center bg-graphite">
      {error ? (
        <div className="max-w-sm text-center">
          <p className="font-display text-lg text-ink">Login didn&apos;t complete</p>
          <p className="mt-2 text-sm text-muted">{error}</p>
          <a href="/" className="mt-4 inline-block text-sm text-ember underline">
            Back to login
          </a>
        </div>
      ) : (
        <Spinner label="signing you in" />
      )}
    </main>
  );
}