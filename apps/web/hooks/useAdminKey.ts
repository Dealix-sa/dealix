"use client";

import { useCallback, useEffect, useState } from "react";

const STORAGE_KEY = "dealix_admin_api_key";

/**
 * Founder admin-key gate. Persists the X-Admin-API-Key in localStorage on the
 * founder's own device (never committed, never sent anywhere but the API).
 *
 * Returns the current key, a setter that persists it, a clear function, and a
 * `ready` flag so callers can avoid flashing the input before hydration.
 */
export function useAdminKey() {
  const [adminKey, setAdminKeyState] = useState<string>("");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    try {
      setAdminKeyState(localStorage.getItem(STORAGE_KEY) ?? "");
    } catch {
      // localStorage unavailable (SSR / privacy mode) — fall back to empty.
    }
    setReady(true);
  }, []);

  const setAdminKey = useCallback((value: string) => {
    const trimmed = value.trim();
    setAdminKeyState(trimmed);
    try {
      if (trimmed) localStorage.setItem(STORAGE_KEY, trimmed);
      else localStorage.removeItem(STORAGE_KEY);
    } catch {
      // ignore persistence failures
    }
  }, []);

  const clearAdminKey = useCallback(() => setAdminKey(""), [setAdminKey]);

  return { adminKey, setAdminKey, clearAdminKey, ready };
}
