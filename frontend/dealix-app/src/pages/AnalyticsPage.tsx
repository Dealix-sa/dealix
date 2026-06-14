import { useState } from 'react';
import {
  Users, Activity, Globe,
  TrendingUp, ArrowUpRight, Download
} from 'lucide-react';
import {
  LineChart as ReLineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';

const monthlyUsers = [
  { month: 'يناير', users: 45, sessions: 320, bounce: 42 },
  { month: 'فبراير', users: 58, sessions: 410, bounce: 38 },
  { month: 'مارس', users: 72, sessions: 520, bounce: 35 },
  { month: 'أبريل', users: 85, sessions: 640, bounce: 32 },
  { month: 'مايو', users: 98, sessions: 780, bounce: 30 },
  { month: 'يونيو', users: 128, sessions: 950, bounce: 28 },
];

const deviceData = [
  { name: 'Desktop', value: 55, color: '#1B5E3B' },
  { name: 'Mobile', value: 35, color: '#C9A94C' },
  { name: 'Tablet', value: 10, color: '#6B7280' },
];

const topPages = [
  { page: '/diagnostic', views: 2450, avgTime: '3:20' },
  { page: '/pricing', views: 1820, avgTime: '2:45' },
  { page: '/features', views: 1560, avgTime: '4:10' },
  { page: '/signup', views: 980, avgTime: '1:30' },
  { page: '/contact', views: 740, avgTime: '2:00' },
];

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState('30d');

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">التحليلات والتقارير</h1>
          <p className="text-sm text-gray-500 mt-1">تحليل أداء المنصة وسلوك المستخدمين</p>
        </div>
        <div className="flex items-center gap-2">
          {['7d', '30d', '90d'].map((r) => (
            <button key={r} onClick={() => setTimeRange(r)} className={`px-3 py-1.5 text-xs font-bold rounded-lg ${
              timeRange === r ? 'bg-dealix-emerald text-white' : 'bg-gray-100 text-gray-600'
            }`}>{r === '7d' ? 'أسبوع' : r === '30d' ? 'شهر' : '3 أشهر'}</button>
          ))}
          <button className="flex items-center gap-1 px-3 py-1.5 text-xs font-bold text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200">
            <Download className="w-3 h-3" /> تصدير
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Users className="w-5 h-5 text-blue-500" /><span className="text-sm text-gray-500">مستخدمون نشطون</span></div>
          <p className="text-2xl font-bold text-gray-900">128</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +24%</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Activity className="w-5 h-5 text-green-500" /><span className="text-sm text-gray-500">الجلسات</span></div>
          <p className="text-2xl font-bold text-gray-900">950</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +18%</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><TrendingUp className="w-5 h-5 text-purple-500" /><span className="text-sm text-gray-500">معدل الارتداد</span></div>
          <p className="text-2xl font-bold text-gray-900">28%</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> -4% تحسن</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Globe className="w-5 h-5 text-dealix-gold" /><span className="text-sm text-gray-500">وقت الجلسة</span></div>
          <p className="text-2xl font-bold text-gray-900">4:32</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +12%</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4">المستخدمون والجلسات</h3>
          <ResponsiveContainer width="100%" height={250}>
            <ReLineChart data={monthlyUsers}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{fontSize: 12}} />
              <YAxis tick={{fontSize: 12}} />
              <Tooltip />
              <Line type="monotone" dataKey="users" stroke="#1B5E3B" strokeWidth={2} name="مستخدمون" />
              <Line type="monotone" dataKey="sessions" stroke="#C9A94C" strokeWidth={2} name="جلسات" />
            </ReLineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4">الأجهزة</h3>
          <ResponsiveContainer width="100%" height={150}>
            <PieChart><Pie data={deviceData} cx="50%" cy="50%" innerRadius={35} outerRadius={60} dataKey="value">
              {deviceData.map((e, i) => <Cell key={i} fill={e.color} />)}
            </Pie></PieChart>
          </ResponsiveContainer>
          <div className="space-y-1 mt-2">
            {deviceData.map((d, i) => (
              <div key={i} className="flex items-center justify-between text-sm"><span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full" style={{backgroundColor: d.color}} />{d.name}</span><span className="font-bold">{d.value}%</span></div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Pages */}
      <div className="bg-white rounded-xl shadow-card border border-gray-100">
        <div className="p-6 border-b border-gray-100"><h3 className="font-bold text-gray-900">أكثر الصفحات زيارة</h3></div>
        <div className="divide-y divide-gray-100">
          {topPages.map((page, i) => (
            <div key={i} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-3">
                <span className="text-sm text-gray-400 w-6">{i + 1}</span>
                <span className="font-medium text-gray-800">{page.page}</span>
              </div>
              <div className="flex items-center gap-8 text-sm">
                <span className="text-gray-500">{page.views.toLocaleString()} مشاهدة</span>
                <span className="text-gray-500">{page.avgTime} متوسط</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
