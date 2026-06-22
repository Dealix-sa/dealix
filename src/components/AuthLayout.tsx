import type { ReactNode } from "react";
import { LOGIN_PATH } from "@/const";
import { useAuth } from "@/hooks/useAuth";
import { AuthLayoutSkeleton } from "./AuthLayoutSkeleton";
import { Button } from "./ui/button";

export default function AuthLayout({
  children,
}: {
  children: ReactNode;
}) {
  const { isLoading, user } = useAuth();

  if (isLoading) {
    return <AuthLayoutSkeleton />;
  }

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-6">
        <div className="w-full max-w-md rounded-2xl border bg-card p-8 text-center shadow-sm">
          <h1 className="text-2xl font-semibold tracking-tight">
            Sign in to continue
          </h1>
          <p className="mt-3 text-sm text-muted-foreground">
            Access to this workspace requires authentication.
          </p>
          <Button
            className="mt-6 w-full"
            size="lg"
            onClick={() => {
              window.location.href = LOGIN_PATH;
            }}
          >
            Sign in
          </Button>
        </div>
      </div>
    );
  }

  return <main className="min-h-screen bg-background">{children}</main>;
}
