import type { Route } from "next";

export interface Command {
  id: string;
  label: string;
  labelAr: string;
  category: string;
  shortcut?: string;
  action: () => void;
}

type NavigateFn = (href: Route<string>) => void;

let navigateFn: NavigateFn = () => {};
let closeFn: () => void = () => {};

/** Wire the command palette to the router + close handler from the component. */
export function registerCommandActions(navigate: NavigateFn, close: () => void): void {
  navigateFn = navigate;
  closeFn = close;
}

function go(href: string): void {
  navigateFn(href as Route<string>);
}

export const COMMANDS: Command[] = [
  { id: "nav-dashboard", label: "Dashboard", labelAr: "لوحة التحكم", category: "navigation", action: () => go("/dashboard") },
  { id: "nav-leads", label: "Leads", labelAr: "العملاء المحتملون", category: "navigation", action: () => go("/leads") },
  { id: "nav-partners", label: "Partners", labelAr: "الشركاء", category: "navigation", action: () => go("/partners/dashboard") },
  { id: "nav-commissions", label: "Commissions", labelAr: "العمولات", category: "navigation", action: () => go("/partners/commissions") },
  { id: "nav-invoices", label: "Invoices", labelAr: "الفواتير", category: "navigation", action: () => go("/subscriptions/invoices") },
  { id: "nav-settings", label: "Settings", labelAr: "الإعدادات", category: "navigation", action: () => go("/settings") },
  { id: "action-close", label: "Close palette", labelAr: "إغلاق", category: "action", action: () => closeFn() },
];

export function searchCommands(query: string, locale: string): Command[] {
  const q = query.trim().toLowerCase();
  if (!q) return COMMANDS;
  const isAr = locale === "ar";
  return COMMANDS.filter((cmd) => {
    const label = isAr ? cmd.labelAr : cmd.label;
    return (
      label.toLowerCase().includes(q) ||
      cmd.label.toLowerCase().includes(q) ||
      cmd.id.toLowerCase().includes(q)
    );
  });
}
