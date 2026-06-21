import { useState } from 'react';
import {
  TrendingUp, DollarSign, Users, Target, ArrowUpRight,
  ArrowDownRight, Calendar, Download, Star, Activity, CheckCircle2
} from 'lucide-react';
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

const revenueData = [
  { month: 'يناير', revenue: 180000, expenses: 140000, profit: 40000 },
  { month: 'فبراير', revenue: 220000, expenses: 150000, profit: 70000 },
  { month: 'مارس', revenue: 280000, expenses: 160000, profit: 120000 },
  { month: 'أبريل', revenue: 350000, expenses: 175000, profit: 175000 },
  { month: 'مايو', revenue: 420000, expenses: 190000, profit: 230000 },
  { month: 'يونيو', revenue: 510000, expenses: 210000, profit: 300000 },
];

const metrics = [
  { label: 'ARR (إيرادات سنوية متكررة)', value: '6.12M', change: '+42%', positive: true, icon: DollarSign, color: 'text-green-600' },
  { label: 'MRR (إيرادات شهرية)', value: '510K', change: '+18%', positive: true, icon: TrendingUp, color: 'text-blue-600' },
  { label: 'NRR (معدل الاحتفاظ الصافي)', value: '128%', change: '+8%', positive: true, icon: Users, color: 'text-purple-600' },
  { label: 'CAC (تكلفة اكتساب)', value: '2,400', change: '-15%', positive: true, icon: Target, color: 'text-amber-600' },
  { label: 'LTV (قيمة العميل مدى الحياة)', value: '48,000', change: '+22%', positive: true, icon: Star, color: 'text-dealix-emerald' },
  { label: 'فترة الاسترداد', value: '4.2', change: '-1.1 شهر', positive: true, icon: Calendar, color: 'text-red-500' },
];

const burnData = [
  { month: 'يناير', burn: 140000, runway: 18 },
  { month: 'فبراير', burn: 150000, runway: 17 },
  { month: 'مارس', burn: 160000, runway: 16 },
  { month: 'أبريل', burn: 175000, runway: 15 },
  { month: 'مايو', burn: 190000, runway: 14 },
  { month: 'يونيو', burn: 210000, runway: 13 },
];

const capTable = [
  { stakeholder: 'المؤسس', shares: '45%', type: 'founder', color: '#1B5E3B' },
  { stakeholder: 'فريق العمل', shares: '15%', type: 'team', color: '#C9A94C' },
  { stakeholder: 'Seed Round', shares: '20%', type: 'seed', color: '#0D2818' },
  { stakeholder: 'خيارات الأسهم', shares: '10%', type: 'options', color: '#6B7280' },
  { stakeholder: 'مستثمرون استراتيجيون', shares: '10%', type: 'strategic', color: '#E8D5A3' },
];

const milestones = [
  { date: 'Q1 2025', title: 'إطلاق المنصة V1', status: 'done' },
  { date: 'Q2 2025', title: '100 عميل مدفوع', status: 'done' },
  { date: 'Q3 2025', title: 'الوصول للتعادل', status: 'in_progress' },
  { date: 'Q4 2025', title: 'جولة Series A', status: 'upcoming' },
  { date: 'Q1 2026', title: 'توسعة دولية', status: 'upcoming' },
  { date: 'Q2 2026', title: '10M ARR', status: 'upcoming' },
];

export default function InvestorPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'financial' | 'milestones'>('overview');

  const totalRaised = 2500000;
  const currentRunway = 13;
  const growthRate = 42;

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">علاقات المستثمرين</h1>
          <p className="text-sm text-gray-500 mt-1">لوحة تحكم المستثمرين والمؤشرات المالية</p>
        </div>
        <div className="flex items-center gap-2">
          {[
            { key: 'overview', label: 'نظرة عامة' },
            { key: 'financial', label: 'مالي' },
            { key: 'milestones', label: 'معالم' },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${
                activeTab === tab.key ? 'bg-dealix-charcoal text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
          <button className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white rounded-lg text-sm font-bold">
            <Download className="w-4 h-4" /> تصدير
          </button>
        </div>
      </div>

      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-dealix-emerald to-dealix-forest rounded-xl p-5 text-white">
          <DollarSign className="w-6 h-6 text-dealix-gold mb-2" />
          <p className="text-sm text-white/70">إجمالي التمويل المجمع</p>
          <p className="text-3xl font-bold">{(totalRaised / 1000000).toFixed(1)}M <span className="text-lg">ريال</span></p>
          <p className="text-xs text-white/60 mt-1">Seed Round + Angel</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <Activity className="w-6 h-6 text-blue-500 mb-2" />
          <p className="text-sm text-gray-500">معدل النمو السنوي</p>
          <p className="text-3xl font-bold text-gray-900">{growthRate}%</p>
          <p className="text-xs text-green-600 mt-1 flex items-center gap-1"><ArrowUpRight className="w-3 h-3" /> YoY</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <Calendar className="w-6 h-6 text-amber-500 mb-2" />
          <p className="text-sm text-gray-500">Runway (شهر)</p>
          <p className="text-3xl font-bold text-gray-900">{currentRunway}</p>
          <p className="text-xs text-amber-600 mt-1 flex items-center gap-1"><ArrowDownRight className="w-3 h-3" /> -1 من الشهر الماضي</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <Target className="w-6 h-6 text-purple-500 mb-2" />
          <p className="text-sm text-gray-500">LTV / CAC Ratio</p>
          <p className="text-3xl font-bold text-gray-900">20x</p>
          <p className="text-xs text-green-600 mt-1 flex items-center gap-1"><ArrowUpRight className="w-3 h-3" /> ممتاز</p>
        </div>
      </div>

      {activeTab === 'overview' && (
        <>
          {/* SaaS Metrics */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
            <h3 className="font-bold text-gray-900 mb-4">مؤشرات SaaS الرئيسية</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {metrics.map((m, i) => {
                const Icon = m.icon;
                return (
                  <div key={i} className="p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                    <div className="flex items-center gap-2 mb-2">
                      <Icon className={`w-4 h-4 ${m.color}`} />
                      <span className="text-xs text-gray-500">{m.label}</span>
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{m.value}</p>
                    <p className={`text-xs mt-1 flex items-center gap-1 ${m.positive ? 'text-green-600' : 'text-red-500'}`}>
                      {m.positive ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                      {m.change}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Revenue Chart */}
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-4">الإيرادات والأرباح</h3>
              <ResponsiveContainer width="100%" height={250}>
                <AreaChart data={revenueData}>
                  <defs>
                    <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#1B5E3B" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#1B5E3B" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="profGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#C9A94C" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#C9A94C" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="month" tick={{fontSize: 12}} />
                  <YAxis tick={{fontSize: 12}} />
                  <Tooltip />
                  <Area type="monotone" dataKey="revenue" stroke="#1B5E3B" fill="url(#revGrad)" name="الإيرادات" />
                  <Area type="monotone" dataKey="profit" stroke="#C9A94C" fill="url(#profGrad)" name="الربح" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Cap Table */}
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-4">هيكلية الملكية (Cap Table)</h3>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={capTable} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="shares" nameKey="stakeholder">
                    {capTable.map((e, i) => <Cell key={i} fill={e.color} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="space-y-2 mt-4">
                {capTable.map((c, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-3 h-3 rounded-full" style={{ backgroundColor: c.color }} />
                      <span className="text-sm text-gray-700">{c.stakeholder}</span>
                    </div>
                    <span className="font-bold text-gray-900 text-sm">{c.shares}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}

      {activeTab === 'financial' && (
        <>
          {/* Burn Rate */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
            <h3 className="font-bold text-gray-900 mb-4">Burn Rate & Runway</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={burnData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" tick={{fontSize: 12}} />
                <YAxis yAxisId="left" tick={{fontSize: 12}} />
                <YAxis yAxisId="right" orientation="right" tick={{fontSize: 12}} />
                <Tooltip />
                <Bar yAxisId="left" dataKey="burn" fill="#EF4444" name="Burn Rate" radius={[4, 4, 0, 0]} />
                <Bar yAxisId="right" dataKey="runway" fill="#1B5E3B" name="Runway (شهور)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-4">Unit Economics</h3>
              <div className="space-y-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">CAC (تكلفة الاكتساب)</span>
                    <span className="font-bold text-gray-900">2,400 ر.س</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div className="h-full bg-blue-500 rounded-full" style={{ width: '30%' }} />
                  </div>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">LTV (قيمة العميل)</span>
                    <span className="font-bold text-gray-900">48,000 ر.س</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div className="h-full bg-green-500 rounded-full" style={{ width: '85%' }} />
                  </div>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-600">ARPU (إيراد لكل مستخدم)</span>
                    <span className="font-bold text-gray-900">4,250 ر.س/شهر</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div className="h-full bg-dealix-emerald rounded-full" style={{ width: '65%' }} />
                  </div>
                </div>
                <div className="p-4 bg-gradient-to-r from-dealix-emerald to-dealix-forest rounded-lg text-white">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">LTV / CAC Ratio</span>
                    <span className="text-2xl font-bold">20x</span>
                  </div>
                  <p className="text-xs text-white/70 mt-1">صحي جداً - أعلى من 3x يعتبر ممتاز</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-4">التوزيع المالي</h3>
              <div className="space-y-3">
                {[
                  { label: 'البحث والتطوير', amount: 750000, percent: 30, color: 'bg-blue-500' },
                  { label: 'المبيعات والتسويق', amount: 625000, percent: 25, color: 'bg-green-500' },
                  { label: 'العمليات', amount: 500000, percent: 20, color: 'bg-amber-500' },
                  { label: 'الموارد البشرية', amount: 375000, percent: 15, color: 'bg-purple-500' },
                  { label: 'الاحتياطي', amount: 250000, percent: 10, color: 'bg-gray-400' },
                ].map((item, i) => (
                  <div key={i}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-gray-700">{item.label}</span>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-bold text-gray-900">{(item.amount / 1000).toFixed(0)}K</span>
                        <span className="text-xs text-gray-400">{item.percent}%</span>
                      </div>
                    </div>
                    <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
                      <div className={`h-full ${item.color} rounded-full`} style={{ width: `${item.percent}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      )}

      {activeTab === 'milestones' && (
        <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
          <h3 className="font-bold text-gray-900 mb-6">خارطة طريق الشركة</h3>
          <div className="relative">
            <div className="absolute right-4 top-0 bottom-0 w-0.5 bg-gray-200" />
            <div className="space-y-6">
              {milestones.map((m, i) => (
                <div key={i} className="flex gap-4 relative">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 z-10 ${
                    m.status === 'done' ? 'bg-green-500' :
                    m.status === 'in_progress' ? 'bg-dealix-emerald' :
                    'bg-gray-300'
                  }`}>
                    {m.status === 'done' ? <CheckCircle2 className="w-5 h-5 text-white" /> :
                     m.status === 'in_progress' ? <Activity className="w-4 h-4 text-white" /> :
                     <Calendar className="w-4 h-4 text-white" />}
                  </div>
                  <div className="flex-1 pb-6">
                    <div className="flex items-center gap-3 mb-1">
                      <span className="text-sm font-bold text-gray-500">{m.date}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                        m.status === 'done' ? 'bg-green-100 text-green-700' :
                        m.status === 'in_progress' ? 'bg-dealix-emerald/10 text-dealix-emerald' :
                        'bg-gray-100 text-gray-500'
                      }`}>
                        {m.status === 'done' ? 'مكتمل' : m.status === 'in_progress' ? 'قيد التنفيذ' : 'قادم'}
                      </span>
                    </div>
                    <p className={`text-base font-bold ${m.status === 'done' ? 'text-green-700 line-through' : 'text-gray-900'}`}>
                      {m.title}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
