"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useLocale } from "next-intl";
import { useAuth } from "@/lib/hooks/useAuth";

const AUTH_COOKIE = "dealix_auth";

export function setAuthCookie(active: boolean) {
  if (typeof document === "undefined") return;
  if (active) {
    document.cookie = `${AUTH_COOKIE}=1; path=/; max-age=604800; SameSite=Lax`;
  } else {
    document.cookie = `${AUTH_COOKIE}=; path=/; max-age=0`;
  }
}

interface AuthGuardProps {
  children: React.ReactNode;
}

export function AuthGuard({ children }: AuthGuardProps) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();

  const authRequired = process.env.NEXT_PUBLIC_AUTH_REQUIRED !== "0";

  useEffect(() => {
    if (!authRequired || isLoading) return;
    if (!isAuthenticated) {
      const next = encodeURIComponent(pathname || `/${locale}/dashboard`);
      router.replace(`/${locale}/login?next=${next}`);
    }
  }, [authRequired, isAuthenticated, isLoading, locale, pathname, router]);

  if (authRequired && isLoading) {
    return (
      <div className="min-h-[40vh] flex items-center justify-center text-muted-foreground text-sm">
        …
      </div>
    );
  }

  if (authRequired && !isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
