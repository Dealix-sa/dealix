"use client";

import { usePathname } from "next/navigation";
import Link from "next/link";
import { useState } from "react";

interface NavItem {
  label: string;
  labelAr: string;
  href: string;
}

interface NavSection {
  sectionAr: string;
  items: NavItem[];
}

const NAV_SECTIONS: NavSection[] = [
  {
    sectionAr: "القيادة",
    items: [
      { label: "War Room", labelAr: "غرفة الحرب", href: "/app/command-room" },
      { label: "Command Center", labelAr: "مركز القيادة", href: "/command-center" },
      { label: "Growth Command", labelAr: "قيادة النمو", href: "/growth-command-center" },
      { label: "Daily Brief", labelAr: "الملخص اليومي", href: "/daily-draft" },
    ],
  },
  {
    sectionAr: "المبيعات",
    items: [
      { label: "CRM", labelAr: "إدارة العملاء", href: "/crm" },
      { label: "Lead Engine", labelAr: "محرك العملاء", href: "/lead-engine" },
      { label: "Pipeline", labelAr: "خط المبيعات", href: "/pipeline" },
      { label: "Deals", labelAr: "الصفقات", href: "/deals" },
      { label: "Quotes", labelAr: "عروض الأسعار", href: "/quotes" },
      { label: "Sales Machine", labelAr: "آلة المبيعات", href: "/sales-machine" },
      { label: "Outreach Lab", labelAr: "مختبر التواصل", href: "/outreach-lab" },
    ],
  },
  {
    sectionAr: "التسليم",
    items: [
      { label: "Client Delivery", labelAr: "تسليم العملاء", href: "/app/client-delivery" },
      { label: "Delivery OS", labelAr: "نظام التسليم", href: "/delivery-os" },
      { label: "Delivery Workspace", labelAr: "مساحة التسليم", href: "/delivery-workspace" },
      { label: "Proof Vault", labelAr: "خزانة الإثبات", href: "/proof-vault" },
    ],
  },
  {
    sectionAr: "الثقة",
    items: [
      { label: "Trust Control", labelAr: "ضبط الثقة", href: "/app/trust-control" },
      { label: "Review Queue", labelAr: "طابور المراجعة", href: "/review-queue" },
      { label: "Safety", labelAr: "الأمان", href: "/safety" },
      { label: "Approvals", labelAr: "الموافقات", href: "/approvals" },
    ],
  },
  {
    sectionAr: "المالية",
    items: [
      { label: "Revenue OS", labelAr: "نظام الإيرادات", href: "/revenue-os" },
      { label: "KPI Finance", labelAr: "مؤشرات مالية", href: "/kpi-finance" },
      { label: "Revenue Machine", labelAr: "آلة الإيرادات", href: "/revenue-machine" },
      { label: "Data Room", labelAr: "غرفة البيانات", href: "/data-room" },
    ],
  },
  {
    sectionAr: "الأنظمة",
    items: [
      { label: "Agents", labelAr: "الوكلاء الذكيون", href: "/agents" },
      { label: "Control Plane", labelAr: "لوحة التحكم", href: "/control-plane" },
      { label: "Company Brain OS", labelAr: "نظام دماغ الشركة", href: "/company-brain-os" },
      { label: "Automation", labelAr: "الأتمتة", href: "/automated-sales" },
    ],
  },
];

function getPageTitle(pathname: string): { en: string; ar: string } {
  for (const section of NAV_SECTIONS) {
    for (const item of section.items) {
      if (pathname === item.href || pathname.startsWith(item.href + "/")) {
        return { en: item.label, ar: item.labelAr };
      }
    }
  }
  return { en: "App", ar: "التطبيق" };
}

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pageTitle = getPageTitle(pathname);

  return (
    <div className="min-h-screen bg-[#070A12] text-white flex" dir="rtl">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-black/60 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed inset-y-0 right-0 z-30 w-64 bg-[#0D1117] border-l border-white/10 flex flex-col
          transform transition-transform duration-200 ease-in-out
          md:static md:translate-x-0
          ${sidebarOpen ? "translate-x-0" : "translate-x-full md:translate-x-0"}
        `}
      >
        {/* Logo */}
        <div className="flex items-center justify-between border-b border-white/10 px-4 py-4">
          <Link href="/app/command-room" className="flex items-center gap-2">
            <span className="text-amber-300 font-bold text-lg tracking-tight">Dealix</span>
            <span className="text-[10px] text-white/30 font-mono">OS</span>
          </Link>
          <button
            onClick={() => setSidebarOpen(false)}
            className="md:hidden text-white/40 hover:text-white text-lg"
            aria-label="Close sidebar"
          >
            x
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-6">
          {NAV_SECTIONS.map((section) => (
            <div key={section.sectionAr}>
              <p className="text-[10px] uppercase tracking-widest text-white/30 font-mono px-2 mb-2">
                {section.sectionAr}
              </p>
              <ul className="space-y-0.5">
                {section.items.map((item) => {
                  const isActive =
                    pathname === item.href || pathname.startsWith(item.href + "/");
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        onClick={() => setSidebarOpen(false)}
                        className={`
                          flex items-center justify-between rounded-lg px-3 py-2 text-sm transition-colors
                          ${
                            isActive
                              ? "bg-amber-400/15 text-amber-300 border border-amber-400/20"
                              : "text-white/60 hover:text-white hover:bg-white/5"
                          }
                        `}
                      >
                        <span>{item.labelAr}</span>
                        <span className="text-[10px] text-white/20">{item.label}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </nav>

        {/* Bottom status */}
        <div className="border-t border-white/10 px-4 py-3">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 flex-shrink-0" />
            <span className="text-xs text-white/40">PDPL-Compliant · No auto-send</span>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top header */}
        <header className="sticky top-0 z-10 border-b border-white/10 bg-[#070A12]/95 backdrop-blur px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="md:hidden text-white/50 hover:text-white p-1"
              aria-label="Open sidebar"
            >
              <span className="block w-5 h-0.5 bg-current mb-1" />
              <span className="block w-5 h-0.5 bg-current mb-1" />
              <span className="block w-5 h-0.5 bg-current" />
            </button>
            <div>
              <span className="text-sm font-medium text-white/90">{pageTitle.ar}</span>
              <span className="text-xs text-white/30 mr-2">· {pageTitle.en}</span>
            </div>
          </div>
          <Link
            href="/war-room"
            className="text-xs text-amber-300/60 hover:text-amber-300 font-mono transition-colors"
          >
            غرفة الحرب
          </Link>
        </header>

        {/* Page content */}
        <div className="flex-1">
          {children}
        </div>
      </div>
    </div>
  );
}
