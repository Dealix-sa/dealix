"use client";

import { useState } from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type InvoiceState = "draft" | "issued" | "paid" | "overdue" | "cancelled";
type InvoiceType = "standard" | "simplified";
type ZatcaStatus = "reported" | "cleared" | "pending" | null;

interface LineItem {
  description_ar: string;
  description_en: string;
  quantity: number;
  unit_price_sar: number;
  line_total_sar: number;
}

interface Invoice {
  invoice_id: string;
  client_id: string;
  company_ar: string;
  company_en: string;
  invoice_number: string;
  issue_date: string;
  due_date: string;
  amount_sar: number;
  vat_15_sar: number;
  total_with_vat_sar: number;
  state: InvoiceState;
  payment_method: string | null;
  paid_at: string | null;
  zatca_status: ZatcaStatus;
  invoice_type: InvoiceType;
  line_items: LineItem[];
  uuid: string | null;
}

interface InvoiceDashboardProps {
  locale: string;
}

// ---------------------------------------------------------------------------
// Static demo data — matches api/routers/invoice_ops.py exactly
// ---------------------------------------------------------------------------

const INVOICES: Invoice[] = [
  {
    invoice_id: "INV-001",
    client_id: "CLT-001",
    company_ar: "شركة الرياض للتقنية",
    company_en: "Riyadh Tech Co",
    invoice_number: "INV-2026-001",
    issue_date: "2026-03-01",
    due_date: "2026-03-31",
    amount_sar: 10000.0,
    vat_15_sar: 1500.0,
    total_with_vat_sar: 11500.0,
    state: "paid",
    payment_method: "bank_transfer",
    paid_at: "2026-03-25T10:00:00+00:00",
    zatca_status: "cleared",
    invoice_type: "standard",
    line_items: [
      {
        description_ar: "خدمات استشارية — الربع الأول",
        description_en: "Consulting Services — Q1",
        quantity: 1,
        unit_price_sar: 10000.0,
        line_total_sar: 10000.0,
      },
    ],
    uuid: "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  },
  {
    invoice_id: "INV-002",
    client_id: "CLT-002",
    company_ar: "مجموعة الخليج للخدمات المالية",
    company_en: "Gulf Financial Services Group",
    invoice_number: "INV-2026-002",
    issue_date: "2026-03-15",
    due_date: "2026-04-14",
    amount_sar: 4999.0,
    vat_15_sar: 749.85,
    total_with_vat_sar: 5748.85,
    state: "paid",
    payment_method: "moyasar_card",
    paid_at: "2026-04-10T14:30:00+00:00",
    zatca_status: "reported",
    invoice_type: "simplified",
    line_items: [
      {
        description_ar: "اشتراك شهري — المؤسسي",
        description_en: "Monthly Subscription — Enterprise",
        quantity: 1,
        unit_price_sar: 4999.0,
        line_total_sar: 4999.0,
      },
    ],
    uuid: "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  },
  {
    invoice_id: "INV-003",
    client_id: "CLT-003",
    company_ar: "شركة سفا للخدمات اللوجستية",
    company_en: "Safa Logistics Co",
    invoice_number: "INV-2026-003",
    issue_date: "2026-04-01",
    due_date: "2026-05-01",
    amount_sar: 2999.0,
    vat_15_sar: 449.85,
    total_with_vat_sar: 3448.85,
    state: "overdue",
    payment_method: null,
    paid_at: null,
    zatca_status: "pending",
    invoice_type: "standard",
    line_items: [
      {
        description_ar: "اشتراك شهري — الأساسي",
        description_en: "Monthly Subscription — Essential",
        quantity: 1,
        unit_price_sar: 2999.0,
        line_total_sar: 2999.0,
      },
    ],
    uuid: "c3d4e5f6-a7b8-9012-cdef-123456789012",
  },
  {
    invoice_id: "INV-004",
    client_id: "CLT-004",
    company_ar: "تمكين الصحية",
    company_en: "Tamkeen Health Tech",
    invoice_number: "INV-2026-004",
    issue_date: "2026-04-15",
    due_date: "2026-05-15",
    amount_sar: 3999.0,
    vat_15_sar: 599.85,
    total_with_vat_sar: 4598.85,
    state: "issued",
    payment_method: null,
    paid_at: null,
    zatca_status: "cleared",
    invoice_type: "standard",
    line_items: [
      {
        description_ar: "اشتراك شهري — الاحترافي",
        description_en: "Monthly Subscription — Professional",
        quantity: 1,
        unit_price_sar: 3999.0,
        line_total_sar: 3999.0,
      },
    ],
    uuid: "d4e5f6a7-b8c9-0123-defa-234567890123",
  },
  {
    invoice_id: "INV-005",
    client_id: "CLT-005",
    company_ar: "شركة جازان للتصنيع",
    company_en: "Jazan Manufacturing Co",
    invoice_number: "INV-2026-005",
    issue_date: "2026-04-20",
    due_date: "2026-05-20",
    amount_sar: 15000.0,
    vat_15_sar: 2250.0,
    total_with_vat_sar: 17250.0,
    state: "overdue",
    payment_method: null,
    paid_at: null,
    zatca_status: "reported",
    invoice_type: "simplified",
    line_items: [
      {
        description_ar: "تطوير منصة الذكاء الاصطناعي المخصص",
        description_en: "Custom AI Platform Development",
        quantity: 1,
        unit_price_sar: 15000.0,
        line_total_sar: 15000.0,
      },
    ],
    uuid: "e5f6a7b8-c9d0-1234-efab-345678901234",
  },
  {
    invoice_id: "INV-006",
    client_id: "CLT-006",
    company_ar: "الوافي للتمويل",
    company_en: "Al-Wafi Finance",
    invoice_number: "INV-2026-006",
    issue_date: "2026-05-01",
    due_date: "2026-05-31",
    amount_sar: 1500.0,
    vat_15_sar: 225.0,
    total_with_vat_sar: 1725.0,
    state: "issued",
    payment_method: null,
    paid_at: null,
    zatca_status: null,
    invoice_type: "simplified",
    line_items: [
      {
        description_ar: "حزمة البيانات الشهرية",
        description_en: "Monthly Data Pack",
        quantity: 1,
        unit_price_sar: 1500.0,
        line_total_sar: 1500.0,
      },
    ],
    uuid: null,
  },
  {
    invoice_id: "INV-007",
    client_id: "CLT-007",
    company_ar: "شركة الأفق للتقنية",
    company_en: "Horizon Technology Co",
    invoice_number: "INV-2026-007",
    issue_date: "2026-05-10",
    due_date: "2026-06-09",
    amount_sar: 3999.0,
    vat_15_sar: 599.85,
    total_with_vat_sar: 4598.85,
    state: "draft",
    payment_method: null,
    paid_at: null,
    zatca_status: null,
    invoice_type: "standard",
    line_items: [
      {
        description_ar: "اشتراك شهري — الاحترافي",
        description_en: "Monthly Subscription — Professional",
        quantity: 1,
        unit_price_sar: 3999.0,
        line_total_sar: 3999.0,
      },
    ],
    uuid: null,
  },
  {
    invoice_id: "INV-008",
    client_id: "CLT-008",
    company_ar: "مجموعة الريادة للاستشارات",
    company_en: "Riyadah Consulting Group",
    invoice_number: "INV-2026-008",
    issue_date: "2026-05-15",
    due_date: "2026-06-14",
    amount_sar: 8500.0,
    vat_15_sar: 1275.0,
    total_with_vat_sar: 9775.0,
    state: "draft",
    payment_method: null,
    paid_at: null,
    zatca_status: null,
    invoice_type: "standard",
    line_items: [
      {
        description_ar: "تحليل السوق وخدمات الاستشارة الاستراتيجية",
        description_en: "Market Analysis and Strategic Consulting",
        quantity: 2,
        unit_price_sar: 4250.0,
        line_total_sar: 8500.0,
      },
    ],
    uuid: null,
  },
  {
    invoice_id: "INV-009",
    client_id: "CLT-009",
    company_ar: "شركة النخبة الطبية",
    company_en: "Elite Medical Co",
    invoice_number: "INV-2026-009",
    issue_date: "2026-02-01",
    due_date: "2026-03-01",
    amount_sar: 4999.0,
    vat_15_sar: 749.85,
    total_with_vat_sar: 5748.85,
    state: "cancelled",
    payment_method: null,
    paid_at: null,
    zatca_status: null,
    invoice_type: "simplified",
    line_items: [
      {
        description_ar: "اشتراك شهري — المؤسسي",
        description_en: "Monthly Subscription — Enterprise",
        quantity: 1,
        unit_price_sar: 4999.0,
        line_total_sar: 4999.0,
      },
    ],
    uuid: null,
  },
  {
    invoice_id: "INV-010",
    client_id: "CLT-010",
    company_ar: "التوسع العقاري السعودي",
    company_en: "Saudi Real Estate Expansion",
    invoice_number: "INV-2026-010",
    issue_date: "2026-05-20",
    due_date: "2026-06-19",
    amount_sar: 3999.0,
    vat_15_sar: 599.85,
    total_with_vat_sar: 4598.85,
    state: "issued",
    payment_method: null,
    paid_at: null,
    zatca_status: "cleared",
    invoice_type: "standard",
    line_items: [
      {
        description_ar: "اشتراك شهري — الاحترافي",
        description_en: "Monthly Subscription — Professional",
        quantity: 1,
        unit_price_sar: 3999.0,
        line_total_sar: 3999.0,
      },
    ],
    uuid: "f6a7b8c9-d0e1-2345-fabc-456789012345",
  },
];

// ---------------------------------------------------------------------------
// State badge configuration
// ---------------------------------------------------------------------------

const STATE_STYLES: Record<
  InvoiceState,
  { bg: string; text: string; ar: string; en: string }
> = {
  draft: { bg: "bg-gray-100", text: "text-gray-600", ar: "مسودة", en: "Draft" },
  issued: { bg: "bg-blue-100", text: "text-blue-700", ar: "صادرة", en: "Issued" },
  paid: { bg: "bg-emerald-100", text: "text-emerald-700", ar: "مدفوعة", en: "Paid" },
  overdue: { bg: "bg-red-100", text: "text-red-700", ar: "متأخرة", en: "Overdue" },
  cancelled: { bg: "bg-gray-200", text: "text-gray-700", ar: "ملغاة", en: "Cancelled" },
};

// ---------------------------------------------------------------------------
// ZATCA status badge configuration
// ---------------------------------------------------------------------------

const ZATCA_STYLES: Record<
  string,
  { bg: string; text: string; ar: string; en: string }
> = {
  reported: {
    bg: "bg-blue-50",
    text: "text-blue-700",
    ar: "مُبلَّغ",
    en: "Reported",
  },
  cleared: {
    bg: "bg-emerald-50",
    text: "text-emerald-700",
    ar: "محقق",
    en: "Cleared",
  },
  pending: {
    bg: "bg-amber-50",
    text: "text-amber-700",
    ar: "معلق",
    en: "Pending",
  },
  none: {
    bg: "bg-gray-100",
    text: "text-gray-500",
    ar: "—",
    en: "—",
  },
};

// ---------------------------------------------------------------------------
// Tooltip wrapper
// ---------------------------------------------------------------------------

function DisabledButtonWithTooltip({
  labelAr,
  labelEn,
  isAr,
}: {
  labelAr: string;
  labelEn: string;
  isAr: boolean;
}) {
  const [show, setShow] = useState(false);

  return (
    <div className="relative inline-block">
      <button
        type="button"
        disabled
        aria-disabled="true"
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
        onFocus={() => setShow(true)}
        onBlur={() => setShow(false)}
        className="text-sm font-semibold px-4 py-2 rounded-lg bg-gray-100 text-gray-400 border border-gray-200 cursor-not-allowed"
      >
        {isAr ? labelAr : labelEn}
      </button>
      {show && (
        <div
          role="tooltip"
          className="absolute z-20 bottom-full mb-2 start-0 bg-gray-900 text-white text-xs rounded-lg px-3 py-1.5 whitespace-nowrap shadow-lg"
        >
          {isAr
            ? "يتطلب موافقة المؤسس (APPROVAL_FIRST)"
            : "Requires founder approval (APPROVAL_FIRST)"}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------------------
// Root component
// ---------------------------------------------------------------------------

export default function InvoiceDashboard({ locale }: InvoiceDashboardProps) {
  const isAr = locale === "ar";
  const dir = isAr ? "rtl" : "ltr";

  const [filterState, setFilterState] = useState<string>("all");

  // Derived summary values
  const outstandingSar = INVOICES.filter(
    (inv) => inv.state === "issued" || inv.state === "overdue"
  ).reduce((sum, inv) => sum + inv.total_with_vat_sar, 0);

  const overdueCount = INVOICES.filter((inv) => inv.state === "overdue").length;

  const compliantCount = INVOICES.filter(
    (inv) => inv.zatca_status === "reported" || inv.zatca_status === "cleared"
  ).length;
  const zatcaCompliancePct = Math.round((compliantCount / INVOICES.length) * 100);

  const zatcaBadgeStyle =
    zatcaCompliancePct >= 80
      ? { bg: "bg-emerald-100", text: "text-emerald-800", border: "border-emerald-300" }
      : zatcaCompliancePct >= 60
      ? { bg: "bg-amber-100", text: "text-amber-800", border: "border-amber-300" }
      : { bg: "bg-red-100", text: "text-red-800", border: "border-red-300" };

  // Filtering
  const filtered = INVOICES.filter(
    (inv) => filterState === "all" || inv.state === filterState
  );

  const stateOptions: InvoiceState[] = [
    "draft",
    "issued",
    "paid",
    "overdue",
    "cancelled",
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6" dir={dir}>
      {/* Page heading */}
      <div>
        <h1 className="text-2xl font-extrabold text-gray-900">
          {isAr ? "لوحة الفواتير" : "Invoice Dashboard"}
        </h1>
        <p className="text-sm text-gray-500 mt-0.5">
          {isAr
            ? "إدارة الفواتير والامتثال لـ ZATCA المرحلة الثانية"
            : "Invoice lifecycle and ZATCA Phase 2 compliance"}
        </p>
      </div>

      {/* Summary bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "إجمالي الفواتير" : "Total Invoices"}
          </p>
          <p className="text-3xl font-extrabold text-gray-900 tabular-nums">
            {INVOICES.length}
          </p>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "المستحق (صادرة + متأخرة)" : "Outstanding SAR (issued + overdue)"}
          </p>
          <p className="text-3xl font-extrabold text-amber-700 tabular-nums">
            {outstandingSar.toLocaleString("ar-SA")}{" "}
            <span className="text-base font-semibold text-gray-500">
              {isAr ? "ر.س" : "SAR"}
            </span>
          </p>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-5">
          <p className="text-xs text-gray-400 mb-1">
            {isAr ? "عدد الفواتير المتأخرة" : "Overdue Count"}
          </p>
          <p
            className={`text-3xl font-extrabold tabular-nums ${
              overdueCount > 0 ? "text-red-600" : "text-gray-900"
            }`}
          >
            {overdueCount}
            {overdueCount > 0 && (
              <span className="ms-2 inline-block text-xs font-bold px-2 py-0.5 rounded-full bg-red-100 text-red-700 align-middle">
                {isAr ? "تنبيه" : "Alert"}
              </span>
            )}
          </p>
        </div>
      </div>

      {/* ZATCA compliance badge */}
      <div
        className={`rounded-xl border ${zatcaBadgeStyle.border} ${zatcaBadgeStyle.bg} p-5 flex items-center gap-4`}
      >
        <div
          className={`text-4xl font-extrabold tabular-nums ${zatcaBadgeStyle.text}`}
        >
          {zatcaCompliancePct}%
        </div>
        <div>
          <p className={`text-base font-bold ${zatcaBadgeStyle.text}`}>
            {isAr ? "امتثال ZATCA" : "ZATCA Compliant"}
          </p>
          <p className="text-xs text-gray-500 mt-0.5">
            {isAr
              ? `${compliantCount} من ${INVOICES.length} فاتورة متوافقة (مُبلَّغ أو محقق)`
              : `${compliantCount} of ${INVOICES.length} invoices compliant (reported or cleared)`}
          </p>
        </div>
      </div>

      {/* Filter bar + create button */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-4 flex flex-wrap gap-4 items-center">
        <div className="flex items-center gap-2">
          <label
            htmlFor="filter-state"
            className="text-sm font-semibold text-gray-700 whitespace-nowrap"
          >
            {isAr ? "الحالة" : "Status"}
          </label>
          <select
            id="filter-state"
            value={filterState}
            onChange={(e) => setFilterState(e.target.value)}
            className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">{isAr ? "الكل" : "All"}</option>
            {stateOptions.map((s) => (
              <option key={s} value={s}>
                {isAr ? STATE_STYLES[s].ar : STATE_STYLES[s].en}
              </option>
            ))}
          </select>
        </div>

        <p className="text-xs text-gray-400">
          {isAr
            ? `${filtered.length} نتيجة`
            : `${filtered.length} result${filtered.length !== 1 ? "s" : ""}`}
        </p>

        <div className="ms-auto">
          <DisabledButtonWithTooltip
            labelAr="إنشاء فاتورة"
            labelEn="Create Invoice"
            isAr={isAr}
          />
        </div>
      </div>

      {/* Invoice table */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-x-auto">
        <table className="w-full text-sm" dir={dir}>
          <thead>
            <tr className="border-b border-gray-100 bg-gray-50">
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "رقم الفاتورة" : "Invoice #"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الشركة" : "Company"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "النوع" : "Type"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الحالة" : "Status"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "المبلغ (ر.س)" : "Amount (SAR)"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "ضريبة 15%" : "VAT 15%"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "الإجمالي شامل الضريبة" : "Total with VAT"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "تاريخ الاستحقاق" : "Due Date"}
              </th>
              <th className="text-start px-4 py-3 font-semibold text-gray-600 whitespace-nowrap">
                {isAr ? "حالة ZATCA" : "ZATCA Status"}
              </th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td
                  colSpan={9}
                  className="text-center text-gray-400 py-10 text-sm"
                >
                  {isAr ? "لا توجد نتائج" : "No results"}
                </td>
              </tr>
            ) : (
              filtered.map((inv, idx) => {
                const stateStyle = STATE_STYLES[inv.state];
                const zatcaKey = inv.zatca_status ?? "none";
                const zatcaStyle = ZATCA_STYLES[zatcaKey] ?? ZATCA_STYLES.none;
                const isEven = idx % 2 === 0;

                return (
                  <tr
                    key={inv.invoice_id}
                    className={`border-b border-gray-50 ${
                      isEven ? "bg-white" : "bg-gray-50/50"
                    } hover:bg-blue-50/30 transition-colors`}
                  >
                    {/* Invoice # */}
                    <td className="px-4 py-3">
                      <p className="font-mono text-xs font-semibold text-gray-700">
                        {inv.invoice_number}
                      </p>
                      <p className="text-xs text-gray-400 font-mono">
                        {inv.invoice_id}
                      </p>
                    </td>

                    {/* Company */}
                    <td className="px-4 py-3">
                      <p className="font-semibold text-gray-900 whitespace-nowrap">
                        {isAr ? inv.company_ar : inv.company_en}
                      </p>
                      <p className="text-xs text-gray-400">{inv.client_id}</p>
                    </td>

                    {/* Type badge */}
                    <td className="px-4 py-3 whitespace-nowrap">
                      {inv.invoice_type === "standard" ? (
                        <span className="inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-700">
                          {isAr ? "قياسية" : "Standard"}
                        </span>
                      ) : (
                        <span className="inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full bg-purple-100 text-purple-700">
                          {isAr ? "مبسطة" : "Simplified"}
                        </span>
                      )}
                    </td>

                    {/* Status badge */}
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span
                        className={`inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full ${stateStyle.bg} ${stateStyle.text}`}
                      >
                        {isAr ? stateStyle.ar : stateStyle.en}
                      </span>
                    </td>

                    {/* Amount */}
                    <td className="px-4 py-3 tabular-nums text-gray-800 font-semibold whitespace-nowrap">
                      {inv.amount_sar.toLocaleString("ar-SA")}
                    </td>

                    {/* VAT */}
                    <td className="px-4 py-3 tabular-nums text-gray-600 whitespace-nowrap">
                      {inv.vat_15_sar.toLocaleString("ar-SA")}
                    </td>

                    {/* Total with VAT */}
                    <td className="px-4 py-3 tabular-nums font-bold text-gray-900 whitespace-nowrap">
                      {inv.total_with_vat_sar.toLocaleString("ar-SA")}
                    </td>

                    {/* Due Date */}
                    <td className="px-4 py-3 text-gray-600 font-mono text-xs whitespace-nowrap">
                      {inv.due_date}
                    </td>

                    {/* ZATCA Status */}
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span
                        className={`inline-block text-xs font-semibold px-2.5 py-0.5 rounded-full ${zatcaStyle.bg} ${zatcaStyle.text}`}
                      >
                        {isAr ? zatcaStyle.ar : zatcaStyle.en}
                      </span>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
