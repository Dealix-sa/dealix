import { useState } from 'react';
import {
  Target, Flag
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const okrs = [
  {
    id: 1, quarter: 'Q2 2025', objective: 'تسريع النمو المالي',
    krs: [
      { id: 1, title: 'الوصول إلى 50 عميل مدفوع', current: 32, target: 50, unit: 'عميل' },
      { id: 2, title: 'تحقيق 500K ريال إيرادات شهري', current: 320000, target: 500000, unit: 'ريال' },
      { id: 3, title: 'رفع معدل الاحتفاظ إلى 85%', current: 78, target: 85, unit: '%' },
    ]
  },
  {
    id: 2, quarter: 'Q2 2025', objective: 'توسيع القطاعات',
    krs: [
      { id: 4, title: 'دخول 3 قطاعات جديدة', current: 1, target: 3, unit: 'قطاع' },
      { id: 5, title: 'إغلاق 5 صفقات مؤسسية', current: 2, target: 5, unit: 'صفقة' },
      { id: 6, title: 'بناء 10 دراسات حالة', current: 4, target: 10, unit: 'دراسة' },
    ]
  },
];

const progressData = [
  { month: 'يناير', financial: 45, expansion: 30, product: 60 },
  { month: 'فبراير', financial: 52, expansion: 38, product: 65 },
  { month: 'مارس', financial: 58, expansion: 42, product: 70 },
  { month: 'أبريل', financial: 65, expansion: 50, product: 72 },
  { month: 'مايو', financial: 70, expansion: 55, product: 78 },
  { month: 'يونيو', financial: 78, expansion: 62, product: 85 },
];

export default function StrategyPage() {
  const [activeQuarter, setActiveQuarter] = useState('Q2 2025');

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">الاستراتيجية والأهداف</h1>
          <p className="text-sm text-gray-500 mt-1">OKRs والتخطيط الاستراتيجي للربع</p>
        </div>
        <div className="flex items-center gap-2">
          {['Q1 2025', 'Q2 2025', 'Q3 2025'].map((q) => (
            <button key={q} onClick={() => setActiveQuarter(q)} className={`px-4 py-2 text-sm font-bold rounded-lg transition-all ${
              activeQuarter === q ? 'bg-dealix-charcoal text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}>{q}</button>
          ))}
        </div>
      </div>

      {/* Vision Banner */}
      <div className="bg-gradient-to-r from-dealix-charcoal to-dealix-forest rounded-xl p-6 text-white">
        <div className="flex items-center gap-3 mb-3">
          <Flag className="w-6 h-6 text-dealix-gold" />
          <h3 className="text-lg font-bold">رؤية 2025</h3>
        </div>
        <p className="text-white/80 text-lg leading-relaxed">
          أن نصبح المنصة السعودية الأولى لإدارة الإيرادات بالذكاء الاصطناعي، مع 200+ عميل مدفوع وإيرادات سنوية تتجاوز 10 مليون ريال
        </p>
      </div>

      {/* OKRs */}
      {okrs.map((okr) => (
        <div key={okr.id} className="bg-white rounded-xl shadow-card border border-gray-100">
          <div className="p-6 border-b border-gray-100">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-dealix-emerald/10 flex items-center justify-center">
                <Target className="w-5 h-5 text-dealix-emerald" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900">{okr.objective}</h3>
                <p className="text-xs text-gray-500">{okr.quarter}</p>
              </div>
            </div>
          </div>
          <div className="divide-y divide-gray-100">
            {okr.krs.map((kr) => {
              const pct = Math.round((kr.current / kr.target) * 100);
              return (
                <div key={kr.id} className="p-6">
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="font-medium text-gray-800">{kr.title}</h4>
                    <span className="text-sm font-bold text-dealix-emerald">{kr.current.toLocaleString()} / {kr.target.toLocaleString()} {kr.unit}</span>
                  </div>
                  <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                    <div className="h-full rounded-full bg-gradient-to-r from-dealix-emerald to-dealix-gold transition-all" style={{ width: `${Math.min(pct, 100)}%` }} />
                  </div>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-xs text-gray-400">{pct}% مكتمل</span>
                    <span className={`text-xs ${pct >= 80 ? 'text-green-600' : pct >= 50 ? 'text-amber-600' : 'text-red-500'}`}>
                      {pct >= 80 ? 'في المسار' : pct >= 50 ? 'يتطلب اهتمام' : 'متأخر'}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}

      {/* Progress Chart */}
      <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
        <h3 className="font-bold text-gray-900 mb-4">تطور الأهداف</h3>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={progressData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="month" tick={{fontSize: 12}} />
            <YAxis tick={{fontSize: 12}} />
            <Tooltip />
            <Bar dataKey="financial" fill="#1B5E3B" name="مالي" radius={[4, 4, 0, 0]} />
            <Bar dataKey="expansion" fill="#C9A94C" name="توسع" radius={[4, 4, 0, 0]} />
            <Bar dataKey="product" fill="#6B7280" name="منتج" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
