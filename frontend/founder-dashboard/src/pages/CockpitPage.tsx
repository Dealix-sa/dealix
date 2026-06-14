import { useEffect, useState } from 'react';
import {
  TrendingUp, Users, DollarSign, Target, Zap, Clock,
  BarChart3, ArrowUpRight, ArrowDownRight, Activity,
  CheckCircle2, AlertTriangle, CircleDollarSign,
  Globe, MessageSquare, FileText, Star
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell
} from 'recharts';

const revenueData = [
  { name: 'يناير', revenue: 12000, target: 15000 },
  { name: 'فبراير', revenue: 18000, target: 20000 },
  { name: 'مارس', revenue: 25000, target: 25000 },
  { name: 'أبريل', revenue: 32000, target: 30000 },
  { name: 'مايو', revenue: 38000, target: 35000 },
  { name: 'يونيو', revenue: 45000, target: 40000 },
];

const pieData = [
  { name: 'اشتراكات', value: 45, color: '#1B5E3B' },
  { name: 'بايلوت', value: 25, color: '#C9A94C' },
  { name: 'مؤسسي', value: 20, color: '#0D2818' },
  { name: 'خدمات', value: 10, color: '#6B7280' },
];

const tasks = [
  { id: 1, title: 'مراجعة عرض العقارات الجديد', status: 'urgent', time: '30 دقيقة', icon: FileText },
  { id: 2, title: 'اتصال مع عميل محتمل - شركة الصحة', status: 'normal', time: '1 ساعة', icon: MessageSquare },
  { id: 3, title: 'تحديث خطة الـ GTM للربع القادم', status: 'normal', time: '2 ساعة', icon: Target },
  { id: 4, title: 'مراجعة تقرير التحليلات الأسبوعي', status: 'done', time: 'تم', icon: CheckCircle2 },
  { id: 5, title: 'موافقة على عقد المؤسسي الجديد', status: 'urgent', time: '45 دقيقة', icon: Star },
];

const kpis = [
  { label: 'الإيرادات الشهرية', value: '45,000', change: '+18.5%', up: true, icon: DollarSign, color: 'from-emerald-500 to-emerald-700' },
  { label: 'العملاء النشطون', value: '128', change: '+12.3%', up: true, icon: Users, color: 'from-amber-500 to-amber-700' },
  { label: 'معدل التحويل', value: '23.5%', change: '+4.2%', up: true, icon: TrendingUp, color: 'from-blue-500 to-blue-700' },
  { label: 'متوسط قيمة الطلب', value: '4,900', change: '-2.1%', up: false, icon: CircleDollarSign, color: 'from-purple-500 to-purple-700' },
];

export default function CockpitPage() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">كابينة المؤسس</h1>
          <p className="text-sm text-gray-500 mt-1">نظرة شاملة على أداء الشركة - {new Date().toLocaleDateString('ar-SA')}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
            مباشر
          </span>
          <span className="px-3 py-1 bg-dealix-gold/10 text-dealix-gold text-xs font-bold rounded-full">
            90 دقيقة يومية
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, i) => {
          const Icon = kpi.icon;
          return (
            <div
              key={i}
              className="bg-white rounded-xl p-5 shadow-card hover:shadow-card-hover transition-all border border-gray-100"
              style={{ animationDelay: `${i * 100}ms` }}
            >
              <div className="flex items-start justify-between mb-3">
                <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${kpi.color} flex items-center justify-center`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <span className={`flex items-center gap-0.5 text-xs font-bold ${kpi.up ? 'text-green-600' : 'text-red-500'}`}>
                  {kpi.up ? <ArrowUpRight className="w-3 h-3" /> : <ArrowDownRight className="w-3 h-3" />}
                  {kpi.change}
                </span>
              </div>
              <p className="text-2xl font-bold text-gray-900">{kpi.value} <span className="text-xs text-gray-400 font-normal">ريال</span></p>
              <p className="text-xs text-gray-500 mt-1">{kpi.label}</p>
            </div>
          );
        })}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue Chart */}
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-bold text-gray-900">أداء الإيرادات</h3>
              <p className="text-xs text-gray-500">الإيرادات مقابل الأهداف (آخر 6 أشهر)</p>
            </div>
            <div className="flex items-center gap-4 text-xs">
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-dealix-emerald" /> الإيرادات</span>
              <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-full bg-dealix-gold" /> الهدف</span>
            </div>
          </div>
          {mounted && (
            <ResponsiveContainer width="100%" height={280}>
              <AreaChart data={revenueData}>
                <defs>
                  <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#1B5E3B" stopOpacity={0.3}/><stop offset="95%" stopColor="#1B5E3B" stopOpacity={0}/></linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="name" tick={{fontSize: 12}} />
                <YAxis tick={{fontSize: 12}} />
                <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)'}} />
                <Area type="monotone" dataKey="revenue" stroke="#1B5E3B" fill="url(#revGrad)" strokeWidth={2} />
                <Area type="monotone" dataKey="target" stroke="#C9A94C" fill="none" strokeWidth={2} strokeDasharray="5 5" />
              </AreaChart>
            </ResponsiveContainer>
          )}
        </div>

        {/* Revenue Distribution */}
        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-1">توزيع الإيرادات</h3>
          <p className="text-xs text-gray-500 mb-6">حسب نوع الخدمة</p>
          {mounted && (
            <ResponsiveContainer width="100%" height={200}>
              <PieChart>
                <Pie data={pieData} cx="50%" cy="50%" innerRadius={50} outerRadius={80} dataKey="value">
                  {pieData.map((entry, index) => <Cell key={index} fill={entry.color} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}
          <div className="space-y-2 mt-4">
            {pieData.map((item, i) => (
              <div key={i} className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2"><span className="w-2.5 h-2.5 rounded-full" style={{backgroundColor: item.color}} /> {item.name}</span>
                <span className="font-bold text-gray-700">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Row: Tasks + Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Tasks */}
        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-gray-900 flex items-center gap-2">
              <Clock className="w-5 h-5 text-dealix-gold" />
              مهام اليوم (90 دقيقة)
            </h3>
            <span className="text-xs bg-dealix-emerald/10 text-dealix-emerald px-2 py-1 rounded-full font-bold">
              {tasks.filter(t => t.status === 'done').length}/{tasks.length} تم
            </span>
          </div>
          <div className="space-y-3">
            {tasks.map((task) => {
              const Icon = task.icon;
              return (
                <div key={task.id} className={`flex items-center gap-3 p-3 rounded-lg border transition-all ${
                  task.status === 'done' ? 'bg-green-50 border-green-100' :
                  task.status === 'urgent' ? 'bg-red-50 border-red-100' :
                  'bg-gray-50 border-gray-100 hover:border-dealix-gold/30'
                }`}>
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    task.status === 'done' ? 'bg-green-100' :
                    task.status === 'urgent' ? 'bg-red-100' :
                    'bg-dealix-gold/10'
                  }`}>
                    <Icon className={`w-4 h-4 ${
                      task.status === 'done' ? 'text-green-600' :
                      task.status === 'urgent' ? 'text-red-500' :
                      'text-dealix-gold'
                    }`} />
                  </div>
                  <div className="flex-1">
                    <p className={`text-sm font-medium ${task.status === 'done' ? 'line-through text-gray-400' : 'text-gray-800'}`}>
                      {task.title}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    {task.status === 'urgent' && <AlertTriangle className="w-4 h-4 text-red-500" />}
                    <span className="text-xs text-gray-400">{task.time}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-dealix-gold" />
            إجراءات سريعة
          </h3>
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: 'تشخيص جديد', icon: Activity, color: 'bg-dealix-emerald/10 text-dealix-emerald' },
              { label: 'عرض تجاري', icon: FileText, color: 'bg-dealix-gold/10 text-dealix-gold' },
              { label: 'مكالمة مبيعات', icon: MessageSquare, color: 'bg-blue-50 text-blue-600' },
              { label: 'تقرير تحليلي', icon: BarChart3, color: 'bg-purple-50 text-purple-600' },
              { label: 'هدف جديد', icon: Target, color: 'bg-orange-50 text-orange-600' },
              { label: 'إعدادات', icon: Globe, color: 'bg-gray-100 text-gray-600' },
            ].map((action, i) => {
              const Icon = action.icon;
              return (
                <button key={i} className="flex items-center gap-3 p-3 rounded-lg border border-gray-100 hover:border-dealix-emerald/30 hover:shadow-md transition-all text-right">
                  <div className={`w-10 h-10 rounded-lg ${action.color} flex items-center justify-center`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-sm font-medium text-gray-700">{action.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
