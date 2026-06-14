import {
  TrendingUp, Users, Eye, MousePointer,
  Mail, MessageSquare, Globe, ArrowUpRight, Plus
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const trafficData = [
  { date: '1 يونيو', visitors: 120, leads: 8 },
  { date: '5 يونيو', visitors: 180, leads: 12 },
  { date: '10 يونيو', visitors: 250, leads: 18 },
  { date: '14 يونيو', visitors: 320, leads: 25 },
];

const channelData = [
  { name: 'بحث عضوي', value: 40, color: '#1B5E3B' },
  { name: 'LinkedIn', value: 25, color: '#C9A94C' },
  { name: 'بريد إلكتروني', value: 20, color: '#0D2818' },
  { name: 'إحالات', value: 10, color: '#6B7280' },
  { name: 'أخرى', value: 5, color: '#E5E5E5' },
];

const campaigns = [
  { id: 1, name: 'حملة العقارات - الرياض', status: 'active', channel: 'LinkedIn', leads: 45, ctr: '3.2%', budget: 5000 },
  { id: 2, name: 'بريد القطاع الصحي', status: 'active', channel: 'Email', leads: 32, ctr: '5.8%', budget: 2000 },
  { id: 3, name: 'محتوى التقنية B2B', status: 'paused', channel: 'Organic', leads: 18, ctr: '2.1%', budget: 0 },
  { id: 4, name: 'حملة تجديد الاشتراكات', status: 'active', channel: 'Email', leads: 28, ctr: '8.4%', budget: 1500 },
];

export default function MarketingOpsPage() {
  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">عمليات التسويق</h1>
          <p className="text-sm text-gray-500 mt-1">إدارة الحملات والقيادة والنمو</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white rounded-lg hover:bg-dealix-forest transition-colors">
          <Plus className="w-4 h-4" />
          <span className="text-sm font-bold">حملة جديدة</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Users className="w-5 h-5 text-blue-500" /><span className="text-sm text-gray-500">زوار</span></div>
          <p className="text-2xl font-bold text-gray-900">3,240</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +24% هذا الشهر</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Eye className="w-5 h-5 text-purple-500" /><span className="text-sm text-gray-500">معدل الاستجابة</span></div>
          <p className="text-2xl font-bold text-gray-900">4.8%</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +1.2%</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><MousePointer className="w-5 h-5 text-dealix-gold" /><span className="text-sm text-gray-500">عملاء محتملين</span></div>
          <p className="text-2xl font-bold text-gray-900">186</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +18%</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><TrendingUp className="w-5 h-5 text-green-500" /><span className="text-sm text-gray-500">CAC</span></div>
          <p className="text-2xl font-bold text-gray-900">2,500</p>
          <p className="text-xs text-gray-500 mt-1">ريال / عميل</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4">حركة المرور والعملاء</h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={trafficData}>
              <defs><linearGradient id="mktGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#1B5E3B" stopOpacity={0.3}/><stop offset="95%" stopColor="#1B5E3B" stopOpacity={0}/></linearGradient></defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" tick={{fontSize: 12}} />
              <YAxis tick={{fontSize: 12}} />
              <Tooltip />
              <Area type="monotone" dataKey="visitors" stroke="#1B5E3B" fill="url(#mktGrad)" name="الزوار" />
              <Area type="monotone" dataKey="leads" stroke="#C9A94C" fill="none" name="العملاء" strokeWidth={2} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4">مصادر الحركة</h3>
          <ResponsiveContainer width="100%" height={180}>
            <PieChart><Pie data={channelData} cx="50%" cy="50%" innerRadius={40} outerRadius={70} dataKey="value">
              {channelData.map((e, i) => <Cell key={i} fill={e.color} />)}
            </Pie></PieChart>
          </ResponsiveContainer>
          <div className="space-y-1 mt-2">
            {channelData.map((c, i) => (
              <div key={i} className="flex items-center justify-between text-sm"><span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full" style={{backgroundColor: c.color}} />{c.name}</span><span className="font-bold">{c.value}%</span></div>
            ))}
          </div>
        </div>
      </div>

      {/* Campaigns */}
      <div className="bg-white rounded-xl shadow-card border border-gray-100">
        <div className="p-6 border-b border-gray-100"><h3 className="font-bold text-gray-900">الحملات النشطة</h3></div>
        <div className="divide-y divide-gray-100">
          {campaigns.map((camp) => (
            <div key={camp.id} className="p-6 flex items-center justify-between hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-4">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${camp.channel === 'LinkedIn' ? 'bg-blue-100' : camp.channel === 'Email' ? 'bg-amber-100' : 'bg-green-100'}`}>
                  {camp.channel === 'LinkedIn' ? <Globe className="w-5 h-5 text-blue-600" /> : camp.channel === 'Email' ? <Mail className="w-5 h-5 text-amber-600" /> : <MessageSquare className="w-5 h-5 text-green-600" />}
                </div>
                <div>
                  <h4 className="font-bold text-gray-900">{camp.name}</h4>
                  <div className="flex items-center gap-3 mt-1 text-sm text-gray-500">
                    <span>{camp.channel}</span>
                    <span>{camp.leads} عميل محتمل</span>
                    <span>CTR: {camp.ctr}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm font-bold text-gray-700">{camp.budget > 0 ? `${camp.budget.toLocaleString()} ريال` : 'مجاني'}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${camp.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
                  {camp.status === 'active' ? 'نشط' : 'متوقف'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
