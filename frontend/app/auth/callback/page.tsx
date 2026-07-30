import { Suspense } from "react";
import AuthCallbackClient from "./AuthCallbackClient";

export default function AuthCallbackPage() {
  return (
    <Suspense
      fallback={
        <main className="flex min-h-screen items-center justify-center bg-graphite">
          Loading...
        </main>
      }
    >
      <AuthCallbackClient />
    </Suspense>
  );
}