import { useState } from 'react';
import {
  Users, Phone, Mail, MessageSquare, Calendar,
  ArrowUpRight, DollarSign, Target, Star, Clock
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const pipelineData = [
  { stage: 'جديد', count: 45, value: 225000 },
  { stage: 'تواصل', count: 28, value: 168000 },
  { stage: 'عرض', count: 18, value: 126000 },
  { stage: 'تفاوض', count: 12, value: 96000 },
  { stage: 'إغلاق', count: 8, value: 72000 },
];

const deals = [
  { id: 1, company: 'شركة الرياض العقارية', contact: 'فهد العتيبي', value: 45000, stage: 'تفاوض', probability: 70, lastActivity: 'مكالمة أمس', icon: Phone },
  { id: 2, company: 'مستشفى الصحة الوطني', contact: 'د. سالم', value: 32000, stage: 'عرض', probability: 50, lastActivity: 'بريد ٢ يوم', icon: Mail },
  { id: 3, company: 'تقنية المستقبل', contact: 'عبدالله المحمد', value: 18000, stage: 'تواصل', probability: 30, lastActivity: 'WhatsApp اليوم', icon: MessageSquare },
  { id: 4, company: 'مجموعة التجارة السعودية', contact: 'سعد الخالد', value: 65000, stage: 'إغلاق', probability: 90, lastActivity: 'اجتماع أمس', icon: Calendar },
  { id: 5, company: 'فنادق الضيافة الفاخرة', contact: 'ناصر الدوسري', value: 28000, stage: 'عرض', probability: 45, lastActivity: 'مكالمة قبل ٣ أيام', icon: Phone },
];

const monthlyData = [
  { month: 'يناير', deals: 5, revenue: 45000 },
  { month: 'فبراير', deals: 7, revenue: 63000 },
  { month: 'مارس', deals: 8, revenue: 78000 },
  { month: 'أبريل', deals: 10, revenue: 95000 },
  { month: 'مايو', deals: 9, revenue: 88000 },
  { month: 'يونيو', deals: 12, revenue: 120000 },
];

export default function SalesOpsPage() {
  const [stageFilter, setStageFilter] = useState('all');
  const totalPipeline = pipelineData.reduce((s, p) => s + p.value, 0);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">عمليات المبيعات</h1>
          <p className="text-sm text-gray-500 mt-1">إدارة خط الأنابيب والصفقات</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white rounded-lg hover:bg-dealix-forest transition-colors">
          <Users className="w-4 h-4" />
          <span className="text-sm font-bold">عميل جديد</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><DollarSign className="w-5 h-5 text-dealix-emerald" /><span className="text-sm text-gray-500">خط الأنابيب</span></div>
          <p className="text-2xl font-bold text-gray-900">{totalPipeline.toLocaleString()}</p>
          <p className="text-xs text-gray-400 mt-1">ريال سعودي</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Target className="w-5 h-5 text-dealix-gold" /><span className="text-sm text-gray-500">الصفقات المفتوحة</span></div>
          <p className="text-2xl font-bold text-gray-900">24</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +3 هذا الأسبوع</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Star className="w-5 h-5 text-purple-500" /><span className="text-sm text-gray-500">معدل الفوز</span></div>
          <p className="text-2xl font-bold text-gray-900">68%</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +5%</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Clock className="w-5 h-5 text-blue-500" /><span className="text-sm text-gray-500">دورة المبيعات</span></div>
          <p className="text-2xl font-bold text-gray-900">14</p>
          <p className="text-xs text-gray-400 mt-1">يوم متوسط</p>
        </div>
      </div>

      {/* Pipeline Chart */}
      <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
        <h3 className="font-bold text-gray-900 mb-4">خط أنابيب المبيعات</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={pipelineData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis type="number" tick={{fontSize: 12}} />
            <YAxis dataKey="stage" type="category" tick={{fontSize: 12}} width={80} />
            <Tooltip formatter={(v: number) => v.toLocaleString()} />
            <Bar dataKey="value" fill="#1B5E3B" radius={[0, 4, 4, 0]} name="القيمة (ريال)" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Deals */}
      <div className="bg-white rounded-xl shadow-card border border-gray-100">
        <div className="p-6 border-b border-gray-100 flex items-center justify-between">
          <h3 className="font-bold text-gray-900">الصفقات</h3>
          <select
            value={stageFilter}
            onChange={(e) => setStageFilter(e.target.value)}
            className="text-sm border border-gray-200 rounded-lg px-3 py-1.5"
          >
            <option value="all">كل المراحل</option>
            <option value="جديد">جديد</option>
            <option value="تواصل">تواصل</option>
            <option value="عرض">عرض</option>
            <option value="تفاوض">تفاوض</option>
            <option value="إغلاق">إغلاق</option>
          </select>
        </div>
        <div className="divide-y divide-gray-100">
          {deals.filter(d => stageFilter === 'all' || d.stage === stageFilter).map((deal) => {
            const Icon = deal.icon;
            return (
              <div key={deal.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-lg bg-dealix-emerald/10 flex items-center justify-center">
                      <Icon className="w-5 h-5 text-dealix-emerald" />
                    </div>
                    <div>
                      <h4 className="font-bold text-gray-900">{deal.company}</h4>
                      <p className="text-sm text-gray-500">{deal.contact} • {deal.lastActivity}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-6">
                    <div className="text-left">
                      <p className="font-bold text-dealix-emerald">{deal.value.toLocaleString()} ريال</p>
                      <p className="text-xs text-gray-400">القيمة</p>
                    </div>
                    <div className="text-left">
                      <p className="font-bold text-gray-700">{deal.probability}%</p>
                      <p className="text-xs text-gray-400">احتمالية</p>
                    </div>
                    <span className="px-3 py-1 bg-dealix-gold/10 text-dealix-gold text-xs font-bold rounded-full">{deal.stage}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Monthly Performance */}
      <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
        <h3 className="font-bold text-gray-900 mb-4">أداء شهري</h3>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={monthlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="month" tick={{fontSize: 12}} />
            <YAxis tick={{fontSize: 12}} />
            <Tooltip />
            <Bar dataKey="deals" fill="#1B5E3B" name="الصفقات" radius={[4, 4, 0, 0]} />
            <Bar dataKey="revenue" fill="#C9A94C" name="الإيرادات" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
