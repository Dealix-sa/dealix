"use client";

import dynamic from "next/dynamic";

// `ssr: false` is only permitted inside a Client Component under Next 15,
// so this thin wrapper lets the (server) services page render the panel
// client-side without itself becoming a Client Component.
const SprintToolsPanel = dynamic(
  () => import("@/components/services/SprintToolsPanel"),
  { ssr: false },
);

export default SprintToolsPanel;
