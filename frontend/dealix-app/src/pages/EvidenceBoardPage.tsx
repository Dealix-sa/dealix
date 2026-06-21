import { useState } from 'react';
import {
  FileCheck, CheckCircle2, Clock, TrendingUp,
  Award, Download, Filter
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const evidenceItems = [
  { id: 1, title: 'زيادة مبيعات الوحدات 35%', category: 'عقارات', metric: '+35%', status: 'verified', date: '2025-06-01', impact: 'high' },
  { id: 2, title: 'تقليل وقت المتابعة 60%', category: 'كفاءة', metric: '-60%', status: 'verified', date: '2025-05-28', impact: 'high' },
  { id: 3, title: 'PDPL compliance 100%', category: 'امتثال', metric: '100%', status: 'verified', date: '2025-05-20', impact: 'critical' },
  { id: 4, title: 'رفع معدل التحويل إلى 23.5%', category: 'مبيعات', metric: '23.5%', status: 'pending', date: '2025-06-10', impact: 'high' },
  { id: 5, title: 'تقليل تكلفة الاستحواذ 40%', category: 'تسويق', metric: '-40%', status: 'verified', date: '2025-05-15', impact: 'medium' },
  { id: 6, title: 'زيادة رضا العملاء 92%', category: 'خدمة', metric: '92%', status: 'verified', date: '2025-06-05', impact: 'high' },
];

const impactChart = [
  { month: 'يناير', revenue: 18000, efficiency: 45 },
  { month: 'فبراير', revenue: 25000, efficiency: 55 },
  { month: 'مارس', revenue: 32000, efficiency: 65 },
  { month: 'أبريل', revenue: 38000, efficiency: 72 },
  { month: 'مايو', revenue: 42000, efficiency: 78 },
  { month: 'يونيو', revenue: 50000, efficiency: 85 },
];

export default function EvidenceBoardPage() {
  const [filter, setFilter] = useState('all');
  const verified = evidenceItems.filter(e => e.status === 'verified').length;
  const highImpact = evidenceItems.filter(e => e.impact === 'high' || e.impact === 'critical').length;

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">لوحة الأدلة</h1>
          <p className="text-sm text-gray-500 mt-1">إثباتات وأرقام توثق فعالية Dealix</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white rounded-lg hover:bg-dealix-forest transition-colors">
          <Download className="w-4 h-4" />
          <span className="text-sm font-bold">تصدير التقرير</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><FileCheck className="w-5 h-5 text-dealix-emerald" /><span className="text-sm text-gray-500">إجمالي الأدلة</span></div>
          <p className="text-3xl font-bold text-gray-900">{evidenceItems.length}</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><CheckCircle2 className="w-5 h-5 text-green-500" /><span className="text-sm text-gray-500">موثقة</span></div>
          <p className="text-3xl font-bold text-gray-900">{verified}</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><TrendingUp className="w-5 h-5 text-dealix-gold" /><span className="text-sm text-gray-500">تأثير عالي</span></div>
          <p className="text-3xl font-bold text-gray-900">{highImpact}</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Award className="w-5 h-5 text-purple-500" /><span className="text-sm text-gray-500">شهادات</span></div>
          <p className="text-3xl font-bold text-gray-900">3</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center gap-3">
            <Filter className="w-4 h-4 text-gray-400" />
            {['all', 'عقارات', 'مبيعات', 'امتثال', 'كفاءة'].map((f) => (
              <button key={f} onClick={() => setFilter(f)} className={`px-3 py-1 text-xs font-bold rounded-full transition-all ${
                filter === f ? 'bg-dealix-emerald text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}>{f === 'all' ? 'الكل' : f}</button>
            ))}
          </div>
          <div className="space-y-3">
            {evidenceItems.filter(e => filter === 'all' || e.category === filter).map((item) => (
              <div key={item.id} className="bg-white rounded-xl p-5 shadow-card border border-gray-100 hover:border-dealix-emerald/30 transition-all">
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-4">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                      item.status === 'verified' ? 'bg-green-100' : 'bg-amber-100'
                    }`}>
                      {item.status === 'verified' ? <CheckCircle2 className="w-5 h-5 text-green-600" /> : <Clock className="w-5 h-5 text-amber-600" />}
                    </div>
                    <div>
                      <h4 className="font-bold text-gray-900">{item.title}</h4>
                      <div className="flex items-center gap-3 mt-1">
                        <span className="text-xs px-2 py-0.5 bg-gray-100 rounded-full text-gray-600">{item.category}</span>
                        <span className="text-xs text-gray-400">{item.date}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-left">
                    <span className="text-2xl font-bold text-dealix-emerald">{item.metric}</span>
                    <span className={`block text-xs mt-1 ${item.impact === 'critical' ? 'text-red-500' : item.impact === 'high' ? 'text-dealix-gold' : 'text-gray-500'}`}>
                      تأثير {item.impact === 'critical' ? 'حرج' : item.impact === 'high' ? 'عالي' : 'متوسط'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4">تطور الأداء</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={impactChart}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{fontSize: 11}} />
              <YAxis tick={{fontSize: 11}} />
              <Tooltip />
              <Bar dataKey="revenue" fill="#1B5E3B" name="الإيرادات" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
