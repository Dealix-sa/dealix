"use client";

import dynamic from "next/dynamic";

const SprintToolsPanel = dynamic(
  () => import("@/components/services/SprintToolsPanel"),
  { ssr: false },
);

interface ServicesSprintPanelProps {
  locale: string;
}

export function ServicesSprintPanel({ locale }: ServicesSprintPanelProps) {
  return (
    <div className="mt-10">
      <SprintToolsPanel locale={locale} />
    </div>
  );
}
