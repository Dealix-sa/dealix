import type { ReactNode } from "react";
import { FounderNav } from "./founder-nav";

export function PageShell({
  currentPath,
  children,
}: {
  currentPath: string;
  children: ReactNode;
}) {
  return (
    <main className="dlx-grid">
      <FounderNav currentPath={currentPath} />
      {children}
    </main>
  );
}
