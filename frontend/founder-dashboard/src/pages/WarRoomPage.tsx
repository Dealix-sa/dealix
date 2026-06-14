import { useState } from 'react';
import {
  Swords, Target, Flame,
  Trophy, ArrowUpRight,
  Star
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const weeklyData = [
  { day: 'السبت', leads: 12, deals: 3, revenue: 15000 },
  { day: 'الأحد', leads: 18, deals: 5, revenue: 25000 },
  { day: 'الإثنين', leads: 15, deals: 4, revenue: 20000 },
  { day: 'الثلاثاء', leads: 22, deals: 6, revenue: 35000 },
  { day: 'الأربعاء', leads: 20, deals: 7, revenue: 42000 },
  { day: 'الخميس', leads: 25, deals: 8, revenue: 50000 },
  { day: 'الجمعة', leads: 10, deals: 2, revenue: 10000 },
];

const battles = [
  { id: 1, name: 'عقد الشركة العقارية الكبرى', progress: 75, status: 'active', priority: 'high', value: 85000 },
  { id: 2, name: 'بايلوت مستشفى الرياض', progress: 40, status: 'active', priority: 'high', value: 12000 },
  { id: 3, name: 'اشتراك شركة التقنية', progress: 90, status: 'closing', priority: 'medium', value: 45000 },
  { id: 4, name: 'عرض قطاع التجزئة', progress: 20, status: 'active', priority: 'medium', value: 25000 },
  { id: 5, name: 'تجديد اشتراك العميل السنوي', progress: 100, status: 'won', priority: 'low', value: 58000 },
];

const leaderboard = [
  { name: 'أحمد', deals: 8, revenue: 180000, streak: 5 },
  { name: 'محمد', deals: 6, revenue: 145000, streak: 3 },
  { name: 'خالد', deals: 5, revenue: 120000, streak: 2 },
  { name: 'سعد', deals: 4, revenue: 95000, streak: 1 },
];

export default function WarRoomPage() {
  const [activeTab, setActiveTab] = useState('battles');

  const wonDeals = battles.filter(b => b.status === 'won').length;
  const activeDeals = battles.filter(b => b.status === 'active').length;
  const totalPipeline = battles.reduce((sum, b) => sum + b.value, 0);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
            <Swords className="w-5 h-5 text-red-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">غرفة الحرب</h1>
            <p className="text-sm text-gray-500">متابعة الصفقات والمنافسة - أسبوع {new Date().toLocaleDateString('ar-SA')}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {[
            { key: 'battles', label: 'المعارك' },
            { key: 'analytics', label: 'التحليلات' },
            { key: 'team', label: 'الفريق' },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-2 text-sm font-bold rounded-lg transition-all ${
                activeTab === tab.key ? 'bg-dealix-charcoal text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-dealix-charcoal to-dealix-forest rounded-xl p-5 text-white">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-5 h-5 text-dealix-gold" />
            <span className="text-sm text-white/60">خط الأنابيب</span>
          </div>
          <p className="text-3xl font-bold">{totalPipeline.toLocaleString()}</p>
          <p className="text-xs text-dealix-gold mt-1">ريال سعودي</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Flame className="w-5 h-5 text-orange-500" />
            <span className="text-sm text-gray-500">صفقات نشطة</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{activeDeals}</p>
          <p className="text-xs text-orange-500 mt-1">قيد المتابعة</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Trophy className="w-5 h-5 text-dealix-gold" />
            <span className="text-sm text-gray-500">صفقات مغلقة</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{wonDeals}</p>
          <p className="text-xs text-green-600 mt-1 flex items-center gap-1">
            <ArrowUpRight className="w-3 h-3" /> هذا الأسبوع
          </p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Star className="w-5 h-5 text-purple-500" />
            <span className="text-sm text-gray-500">معدل الفوز</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">68%</p>
          <p className="text-xs text-green-600 mt-1 flex items-center gap-1">
            <ArrowUpRight className="w-3 h-3" /> +5% عن الشهر الماضي
          </p>
        </div>
      </div>

      {activeTab === 'battles' && (
        <div className="space-y-6">
          {/* Battles List */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100">
            <div className="p-6 border-b border-gray-100">
              <h3 className="font-bold text-gray-900">معارك الأسبوع</h3>
            </div>
            <div className="divide-y divide-gray-100">
              {battles.map((battle) => (
                <div key={battle.id} className="p-6 hover:bg-gray-50 transition-colors">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${
                        battle.status === 'won' ? 'bg-green-500' :
                        battle.status === 'closing' ? 'bg-dealix-gold animate-pulse' :
                        'bg-blue-500'
                      }`} />
                      <h4 className="font-bold text-gray-900">{battle.name}</h4>
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        battle.priority === 'high' ? 'bg-red-100 text-red-700' :
                        battle.priority === 'medium' ? 'bg-amber-100 text-amber-700' :
                        'bg-green-100 text-green-700'
                      }`}>
                        {battle.priority === 'high' ? 'عالي' : battle.priority === 'medium' ? 'متوسط' : 'منخفض'}
                      </span>
                    </div>
                    <span className="text-lg font-bold text-dealix-emerald">{battle.value.toLocaleString()} ريال</span>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="flex-1">
                      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all ${
                            battle.status === 'won' ? 'bg-green-500' :
                            battle.status === 'closing' ? 'bg-dealix-gold' :
                            'bg-blue-500'
                          }`}
                          style={{ width: `${battle.progress}%` }}
                        />
                      </div>
                    </div>
                    <span className="text-sm text-gray-500 w-12">{battle.progress}%</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'analytics' && (
        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4">أداء الأسبوع</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="day" tick={{fontSize: 12}} />
              <YAxis tick={{fontSize: 12}} />
              <Tooltip />
              <Bar dataKey="leads" fill="#1B5E3B" name="عملاء محتملين" radius={[4, 4, 0, 0]} />
              <Bar dataKey="deals" fill="#C9A94C" name="صفقات" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {activeTab === 'team' && (
        <div className="bg-white rounded-xl shadow-card border border-gray-100">
          <div className="p-6 border-b border-gray-100">
            <h3 className="font-bold text-gray-900">لوحة المتصدرين</h3>
          </div>
          <div className="divide-y divide-gray-100">
            {leaderboard.map((member, i) => (
              <div key={i} className="p-6 flex items-center gap-6">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg ${
                  i === 0 ? 'bg-dealix-gold text-white' :
                  i === 1 ? 'bg-gray-300 text-gray-700' :
                  i === 2 ? 'bg-amber-700 text-white' :
                  'bg-gray-100 text-gray-500'
                }`}>
                  {i + 1}
                </div>
                <div className="flex-1">
                  <p className="font-bold text-gray-900">{member.name}</p>
                  <p className="text-sm text-gray-500">{member.deals} صفقات</p>
                </div>
                <div className="text-left">
                  <p className="font-bold text-dealix-emerald">{member.revenue.toLocaleString()} ريال</p>
                  <p className="text-xs text-gray-400">streak: {member.streak} أيام</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
