"use client";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type MemberType = "full-time" | "part-time" | "contractor" | "planned";
type MemberStatus = "active" | "probation" | "planned" | "inactive";
type MilestoneStatus = "triggered" | "upcoming" | "planned";

interface TeamMember {
  id: string;
  name_ar: string;
  name_en: string;
  role_ar: string;
  role_en: string;
  type: MemberType;
  status: MemberStatus;
  monthly_cost_sar: number;
  joined: string;
}

interface HiringMilestone {
  id: string;
  role_ar: string;
  role_en: string;
  mrr_threshold_sar: number;
  status: MilestoneStatus;
  note_ar: string;
  note_en: string;
}

interface TeamDashboardProps {
  locale: string;
}

// ---------------------------------------------------------------------------
// Demo data
// ---------------------------------------------------------------------------

const TEAM_MEMBERS: TeamMember[] = [
  {
    id: "TM-001",
    name_ar: "بسام العسيري",
    name_en: "Bassam Al-Assiri",
    role_ar: "المؤسس ومدير العمليات",
    role_en: "Founder & Operations Director",
    type: "full-time",
    status: "active",
    monthly_cost_sar: 0,
    joined: "2025-11-01",
  },
  {
    id: "TM-002",
    name_ar: "ريم الشمري",
    name_en: "Reem Al-Shammari",
    role_ar: "مدير نجاح العملاء",
    role_en: "Customer Success Manager",
    type: "full-time",
    status: "active",
    monthly_cost_sar: 8000,
    joined: "2026-02-01",
  },
  {
    id: "TM-003",
    name_ar: "علي القحطاني",
    name_en: "Ali Al-Qahtani",
    role_ar: "مهندس تقنية البيانات",
    role_en: "Data Engineering Specialist",
    type: "contractor",
    status: "active",
    monthly_cost_sar: 6000,
    joined: "2026-03-15",
  },
  {
    id: "TM-004",
    name_ar: "سلمى الدوسري",
    name_en: "Salma Al-Dawsari",
    role_ar: "متخصص تطوير المبيعات",
    role_en: "Sales Development Representative",
    type: "part-time",
    status: "probation",
    monthly_cost_sar: 3500,
    joined: "2026-05-01",
  },
  {
    id: "TM-005",
    name_ar: "دور مخطط — CSM ثاني",
    name_en: "Planned Role — CSM #2",
    role_ar: "مدير نجاح العملاء (الثاني)",
    role_en: "Customer Success Manager #2",
    type: "planned",
    status: "planned",
    monthly_cost_sar: 8500,
    joined: "—",
  },
];

const HIRING_MILESTONES: HiringMilestone[] = [
  {
    id: "HM-001",
    role_ar: "مدير نجاح العملاء",
    role_en: "Customer Success Manager",
    mrr_threshold_sar: 15000,
    status: "triggered",
    note_ar: "تم تعيينه — فبراير 2026",
    note_en: "Hired — February 2026",
  },
  {
    id: "HM-002",
    role_ar: "متخصص تطوير المبيعات",
    role_en: "Sales Development Representative",
    mrr_threshold_sar: 25000,
    status: "triggered",
    note_ar: "تم التعيين — مايو 2026",
    note_en: "Hired — May 2026",
  },
  {
    id: "HM-003",
    role_ar: "CSM ثاني",
    role_en: "CSM #2",
    mrr_threshold_sar: 45000,
    status: "upcoming",
    note_ar: "قريب — MRR الحالي 42,800 ر.س",
    note_en: "Near threshold — current MRR 42,800 SAR",
  },
  {
    id: "HM-004",
    role_ar: "مدير شراكات",
    role_en: "Partnerships Manager",
    mrr_threshold_sar: 70000,
    status: "planned",
    note_ar: "مخطط بعد تجاوز 70,000 ر.س MRR",
    note_en: "Planned after 70,000 SAR MRR",
  },
  {
    id: "HM-005",
    role_ar: "رئيس العمليات",
    role_en: "Head of Operations",
    mrr_threshold_sar: 100000,
    status: "planned",
    note_ar: "مخطط بعد تجاوز 100,000 ر.س MRR",
    note_en: "Planned after 100,000 SAR MRR",
  },
];

// ---------------------------------------------------------------------------
// Display configs
// ---------------------------------------------------------------------------

const TYPE_LABELS: Record<MemberType, { ar: string; en: string }> = {
  "full-time": { ar: "دوام كامل", en: "Full-Time" },
  "part-time": { ar: "دوام جزئي", en: "Part-Time" },
  contractor: { ar: "متعاقد", en: "Contractor" },
  planned: { ar: "مخطط", en: "Planned" },
};

const STATUS_STYLES: Record<
  MemberStatus,
  { bg: string; text: string; ar: string; en: string }
> = {
  active: { bg: "bg-emerald-100", text: "text-emerald-800", ar: "نشط", en: "Active" },
  probation: { bg: "bg-amber-100", text: "text-amber-800", ar: "فترة تجربة", en: "Probation" },
  planned: { bg: "bg-gray-100", text: "text-gray-700", ar: "مخطط", en: "Planned" },
  inactive: { bg: "bg-red-100", text: "text-red-800", ar: "غير نشط", en: "Inactive" },
};

const MILESTONE_STYLES: Record<
  MilestoneStatus,
  { dotBg: string; lineBg: string; ar: string; en: string }
> = {
  triggered: {
    dotBg: "bg-emerald-500",
    lineBg: "bg-emerald-200",
    ar: "مكتمل",
    en: "Triggered",
  },
  upcoming: {
    dotBg: "bg-amber-400",
    lineBg: "bg-amber-200",
    ar: "قريب",
    en: "Upcoming",
  },
  planned: {
    dotBg: "bg-gray-300",
    lineBg: "bg-gray-200",
    ar: "مخطط",
    en: "Planned",
  },
};

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function SectionHeading({ ar, en }: { ar: string; en: string }) {
  return (
    <div className="mb-4">
      <h2 className="text-xl font-bold text-gray-900">{ar}</h2>
      <p className="text-xs text-gray-400 mt-0.5">{en}</p>
    </div>
  );
}

// Milestone icon — SVG inline, no external library
function MilestoneIcon({ status }: { status: MilestoneStatus }) {
  if (status === "triggered") {
    return (
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        aria-hidden="true"
        className="flex-shrink-0"
      >
        <circle cx="10" cy="10" r="10" className="fill-emerald-500" />
        <path
          d="M6 10l3 3 5-5"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }
  if (status === "upcoming") {
    return (
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        aria-hidden="true"
        className="flex-shrink-0"
      >
        <circle cx="10" cy="10" r="9" stroke="#F59E0B" strokeWidth="2" fill="white" />
        <path
          d="M10 6v4l2.5 2.5"
          stroke="#F59E0B"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  }
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 20 20"
      fill="none"
      aria-hidden="true"
      className="flex-shrink-0"
    >
      <circle cx="10" cy="10" r="9" stroke="#D1D5DB" strokeWidth="2" fill="white" />
    </svg>
  );
}

// ---------------------------------------------------------------------------
// Root component
// ---------------------------------------------------------------------------

export default function TeamDashboard({ locale }: TeamDashboardProps) {
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  const activeMembers = TEAM_MEMBERS.filter(
    (m) => m.status === "active" || m.status === "probation"
  );
  const monthlyOverhead = TEAM_MEMBERS.filter((m) => m.status !== "planned").reduce(
    (sum, m) => sum + m.monthly_cost_sar,
    0
  );
  const openRoles = TEAM_MEMBERS.filter((m) => m.status === "planned").length;

  // CSM ratio: active clients (4 active subs from subscription_ops) vs active CSMs
  const activeCSMCount = TEAM_MEMBERS.filter(
    (m) =>
      (m.status === "active" || m.status === "probation") &&
      (m.role_en.toLowerCase().includes("customer success") ||
        m.role_en.toLowerCase().includes("csm"))
  ).length;
  const activeClientCount = 4; // matches SUB-001 through SUB-004 active state
  const csmRatio = activeCSMCount > 0 ? activeClientCount / activeCSMCount : 0;
  const ratioWarn = csmRatio > 6;
  const ratioPercent = Math.min(100, (csmRatio / 8) * 100); // scale: 8 clients/CSM = 100%

  return (
    <div className="max-w-7xl mx-auto space-y-8" dir={dir}>
      {/* Page heading */}
      <div>
        <h1 className="text-2xl font-extrabold text-gray-900">
          {isAr ? "لوحة تحكم الفريق" : "Team Dashboard"}
        </h1>
        <p className="text-sm text-gray-500 mt-0.5">
          {isAr
            ? "الطاقة الاستيعابية والتكاليف والتوظيف المخطط"
            : "Capacity, overhead, and hiring milestones"}
        </p>
      </div>

      {/* Team stats bar */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "إجمالي الفريق" : "Total Team"}
          </p>
          <p className="text-3xl font-extrabold text-gray-900 tabular-nums">
            {TEAM_MEMBERS.length}
          </p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "الأعضاء النشطون" : "Active Members"}
          </p>
          <p className="text-3xl font-extrabold text-emerald-700 tabular-nums">
            {activeMembers.length}
          </p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "التكلفة الشهرية" : "Monthly Overhead"}
          </p>
          <p className="text-2xl font-extrabold text-gray-800 tabular-nums">
            {monthlyOverhead.toLocaleString("ar-SA")}{" "}
            <span className="text-sm font-normal text-gray-500">
              {isAr ? "ر.س" : "SAR"}
            </span>
          </p>
        </div>
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "الأدوار المفتوحة" : "Open Roles"}
          </p>
          <p
            className={`text-3xl font-extrabold tabular-nums ${
              openRoles > 0 ? "text-blue-600" : "text-gray-900"
            }`}
          >
            {openRoles}
          </p>
        </div>
      </div>

      {/* Capacity gauge */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
        <p className="text-base font-bold text-gray-800 mb-1">
          {isAr ? "نسبة العملاء إلى مدير نجاح العملاء" : "Client : CSM Ratio"}
        </p>
        <p className="text-xs text-gray-400 mb-4">
          {isAr
            ? `${activeClientCount} عميل نشط / ${activeCSMCount} مدير CSM`
            : `${activeClientCount} active clients / ${activeCSMCount} CSM`}
        </p>
        <div className="flex items-center gap-4">
          <div className="flex-1 bg-gray-100 rounded-full h-3 overflow-hidden">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                ratioWarn ? "bg-amber-400" : "bg-emerald-500"
              }`}
              style={{ width: `${ratioPercent}%` }}
              role="progressbar"
              aria-valuenow={csmRatio}
              aria-valuemin={0}
              aria-valuemax={8}
              aria-label={isAr ? "نسبة العملاء إلى CSM" : "Client to CSM ratio"}
            />
          </div>
          <span
            className={`text-sm font-bold tabular-nums whitespace-nowrap ${
              ratioWarn ? "text-amber-600" : "text-emerald-700"
            }`}
          >
            {csmRatio.toFixed(1)}
            {isAr ? " : 1" : ":1"}
          </span>
        </div>
        {ratioWarn && (
          <p className="text-xs font-semibold text-amber-700 mt-2">
            {isAr
              ? "تحذير: نسبة العملاء تتجاوز 6 لكل CSM — فكر في التوظيف"
              : "Warning: client ratio exceeds 6 per CSM — consider hiring"}
          </p>
        )}
      </div>

      {/* Team table + Hiring milestones (two-column on large screens) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Team table — 2/3 width */}
        <section aria-labelledby="team-table-heading" className="lg:col-span-2">
          <SectionHeading
            ar="أعضاء الفريق"
            en="Team Members"
          />
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
            <table className="w-full text-sm" dir={dir}>
              <thead>
                <tr className="border-b border-gray-100 bg-gray-50">
                  <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                    {isAr ? "الاسم" : "Name"}
                  </th>
                  <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                    {isAr ? "الدور" : "Role"}
                  </th>
                  <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                    {isAr ? "النوع" : "Type"}
                  </th>
                  <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                    {isAr ? "الحالة" : "Status"}
                  </th>
                  <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                    {isAr ? "التكلفة الشهرية" : "Monthly Cost"}
                  </th>
                  <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                    {isAr ? "تاريخ الانضمام" : "Joined"}
                  </th>
                </tr>
              </thead>
              <tbody>
                {TEAM_MEMBERS.map((member, idx) => {
                  const statusStyle = STATUS_STYLES[member.status];
                  const typeLabel = TYPE_LABELS[member.type];
                  const isEven = idx % 2 === 0;
                  return (
                    <tr
                      key={member.id}
                      className={`border-b border-gray-50 ${isEven ? "bg-white" : "bg-gray-50/50"} hover:bg-blue-50/30 transition-colors`}
                    >
                      <td className="px-4 py-3">
                        <p className="font-semibold text-gray-900">
                          {isAr ? member.name_ar : member.name_en}
                        </p>
                        <p className="text-xs text-gray-400 font-mono">{member.id}</p>
                      </td>
                      <td className="px-4 py-3 text-gray-700">
                        {isAr ? member.role_ar : member.role_en}
                      </td>
                      <td className="px-4 py-3 text-gray-600 whitespace-nowrap">
                        {isAr ? typeLabel.ar : typeLabel.en}
                      </td>
                      <td className="px-4 py-3">
                        <span
                          className={`inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full ${statusStyle.bg} ${statusStyle.text}`}
                        >
                          {isAr ? statusStyle.ar : statusStyle.en}
                        </span>
                      </td>
                      <td className="px-4 py-3 tabular-nums font-semibold text-gray-800 whitespace-nowrap">
                        {member.monthly_cost_sar === 0
                          ? isAr
                            ? "—"
                            : "—"
                          : `${member.monthly_cost_sar.toLocaleString("ar-SA")} ${isAr ? "ر.س" : "SAR"}`}
                      </td>
                      <td className="px-4 py-3 text-gray-500 font-mono text-xs whitespace-nowrap">
                        {member.joined}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>

        {/* Hiring milestones — 1/3 width */}
        <section aria-labelledby="milestones-heading">
          <SectionHeading
            ar="مراحل التوظيف"
            en="Hiring Milestones"
          />
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
            <ol className="relative" aria-label={isAr ? "مراحل التوظيف" : "Hiring milestones"}>
              {HIRING_MILESTONES.map((milestone, idx) => {
                const style = MILESTONE_STYLES[milestone.status];
                const isLast = idx === HIRING_MILESTONES.length - 1;
                return (
                  <li key={milestone.id} className="flex gap-3 pb-6 last:pb-0 relative">
                    {/* Vertical connector line */}
                    {!isLast && (
                      <div
                        className={`absolute top-5 w-0.5 h-full ${style.lineBg}`}
                        style={isAr ? { right: "9px" } : { left: "9px" }}
                        aria-hidden="true"
                      />
                    )}

                    {/* Icon */}
                    <div className="relative z-10 flex-shrink-0 mt-0.5">
                      <MilestoneIcon status={milestone.status} />
                    </div>

                    {/* Content */}
                    <div className="min-w-0 flex-1">
                      <div className="flex flex-wrap items-center gap-1.5 mb-0.5">
                        <p className="text-sm font-bold text-gray-900">
                          {isAr ? milestone.role_ar : milestone.role_en}
                        </p>
                        <span
                          className={`text-xs font-semibold px-1.5 py-0.5 rounded-full ${
                            milestone.status === "triggered"
                              ? "bg-emerald-100 text-emerald-700"
                              : milestone.status === "upcoming"
                              ? "bg-amber-100 text-amber-700"
                              : "bg-gray-100 text-gray-500"
                          }`}
                        >
                          {isAr ? style.ar : style.en}
                        </span>
                      </div>
                      <p className="text-xs text-gray-500 tabular-nums">
                        {isAr ? "عند" : "At"}{" "}
                        <span className="font-semibold">
                          {milestone.mrr_threshold_sar.toLocaleString("ar-SA")}{" "}
                          {isAr ? "ر.س" : "SAR"}
                        </span>{" "}
                        MRR
                      </p>
                      <p className="text-xs text-gray-400 mt-0.5">
                        {isAr ? milestone.note_ar : milestone.note_en}
                      </p>
                    </div>
                  </li>
                );
              })}
            </ol>
          </div>
        </section>
      </div>
    </div>
  );
}
