"use client";

// Local notification preferences service. Persists to localStorage until a
// server-side preferences endpoint is wired.

export type NotificationType = string;

export interface QuietHours {
  enabled: boolean;
  start: string;
  end: string;
}

export interface NotificationPreferences {
  email: boolean;
  push: boolean;
  inApp: boolean;
  types: Record<NotificationType, boolean>;
  quietHours: QuietHours;
}

const STORAGE_KEY = "dealix_notification_prefs";

const DEFAULT_PREFERENCES: NotificationPreferences = {
  email: true,
  push: true,
  inApp: true,
  types: {
    deals: true,
    tasks: true,
    mentions: true,
    system: true,
  },
  quietHours: { enabled: false, start: "22:00", end: "08:00" },
};

export function getNotificationPreferences(): NotificationPreferences {
  if (typeof window === "undefined") return DEFAULT_PREFERENCES;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return DEFAULT_PREFERENCES;
    const parsed = JSON.parse(raw) as Partial<NotificationPreferences>;
    return {
      ...DEFAULT_PREFERENCES,
      ...parsed,
      types: { ...DEFAULT_PREFERENCES.types, ...(parsed.types ?? {}) },
      quietHours: { ...DEFAULT_PREFERENCES.quietHours, ...(parsed.quietHours ?? {}) },
    };
  } catch {
    return DEFAULT_PREFERENCES;
  }
}

export function saveNotificationPreferences(prefs: NotificationPreferences): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
  } catch {
    // Ignore storage failures (private mode, quota, etc.).
  }
}

// ── Notifications ──────────────────────────────────────────────────────────

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  titleAr: string;
  description: string;
  descriptionAr: string;
  priority: string;
  read: boolean;
  createdAt: string;
  actionUrl?: string;
}

const PRIORITY_ORDER: Record<string, number> = { high: 0, medium: 1, low: 2 };

const PRIORITY_COLORS: Record<string, string> = {
  high: "text-red-500",
  medium: "text-amber-500",
  low: "text-muted-foreground",
};

/** Number of unread notifications. */
export function getUnreadCount(notifications: Notification[]): number {
  return notifications.filter((n) => !n.read).length;
}

/** Tailwind text-color class for a notification priority. */
export function getNotificationColor(priority: string): string {
  return PRIORITY_COLORS[priority] ?? PRIORITY_COLORS.low;
}

/** Notifications sorted by priority (high → low), then newest first. */
export function getNotificationsByPriority(notifications: Notification[]): Notification[] {
  return [...notifications].sort((a, b) => {
    const pa = PRIORITY_ORDER[a.priority] ?? 99;
    const pb = PRIORITY_ORDER[b.priority] ?? 99;
    if (pa !== pb) return pa - pb;
    return b.createdAt.localeCompare(a.createdAt);
  });
}

/** Mark a single notification as read (returns the updated list). */
export function markAsRead(notifications: Notification[], id: string): Notification[] {
  return notifications.map((n) => (n.id === id ? { ...n, read: true } : n));
}

/** Mark all notifications as read (returns the updated list). */
export function markAllAsRead(notifications: Notification[]): Notification[] {
  return notifications.map((n) => ({ ...n, read: true }));
}
