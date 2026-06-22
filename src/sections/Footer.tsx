import { BarChart3 } from "lucide-react";

const productLinks = [
  { label: "Revenue Command Room", href: "/command-room" },
  { label: "Company Brain OS", href: "/brain" },
  { label: "Booking", href: "/book-call" },
];

export default function Footer() {
  return (
    <footer className="border-t border-[#15807A]/10 bg-[#0A1F1E] py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 grid gap-8 md:grid-cols-3">
          <div className="md:col-span-1">
            <div className="mb-4 flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#15807A]">
                <BarChart3 className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-xl font-bold text-white">Dealix</p>
                <p className="text-xs text-[#8CB3B0]">
                  AI Operating Systems for Saudi B2B
                </p>
              </div>
            </div>
            <p className="max-w-md text-sm leading-7 text-[#8CB3B0]">
              منصة تشغيل تربط الإيرادات، WhatsApp، القرارات، الحوكمة، وتسليم
              العملاء داخل workflow واحد قابل للمراجعة اليومية.
            </p>
          </div>

          <div>
            <h4 className="mb-4 font-bold text-white">المنتج</h4>
            <ul className="space-y-2">
              {productLinks.map((item) => (
                <li key={item.label}>
                  <a
                    href={item.href}
                    className="text-sm text-[#8CB3B0] transition-colors hover:text-[#15807A]"
                  >
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="mb-4 font-bold text-white">مبادئ التشغيل</h4>
            <ul className="space-y-2 text-sm text-[#8CB3B0]">
              <li>draft_only افتراضيًا</li>
              <li>مراجعة بشرية قبل الإرسال الحساس</li>
              <li>تقليل البيانات وسجل أحداث واضح</li>
              <li>لا وعود ROI غير مثبتة</li>
            </ul>
          </div>
        </div>

        <div className="flex flex-col gap-4 border-t border-[#15807A]/10 pt-8 md:flex-row md:items-center md:justify-between">
          <p className="text-sm text-[#8CB3B0]">
            © 2026 Dealix. جميع الحقوق محفوظة.
          </p>
          <p className="text-xs text-[#8CB3B0]">
            يعتمد على human oversight وcompliance-friendly defaults.
          </p>
        </div>
      </div>
    </footer>
  );
}