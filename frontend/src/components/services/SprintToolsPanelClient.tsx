"use client";

import dynamic from "next/dynamic";

// next/dynamic with ssr:false is only valid inside a Client Component.
// This thin wrapper lets the server-rendered services page mount the
// browser-only SprintToolsPanel without forcing the page to be a client
// component.
const SprintToolsPanel = dynamic(() => import("./SprintToolsPanel"), {
  ssr: false,
});

export default SprintToolsPanel;
