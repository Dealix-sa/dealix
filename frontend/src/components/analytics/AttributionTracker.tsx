"use client";

import { useEffect } from "react";

import { captureFirstTouchAttribution } from "@/lib/utm";

/**
 * App-wide, null-rendering tracker. Records first-touch marketing attribution
 * (UTM params / ad-click ids / referrer / landing path) on initial load so it can be
 * attached to governed lead submissions later. localStorage only — no network call,
 * no external send.
 */
export function AttributionTracker() {
  useEffect(() => {
    captureFirstTouchAttribution();
  }, []);
  return null;
}
