import { useState } from 'react';
import {
  CheckCircle2, XCircle, Clock,
  AlertTriangle, User, Calendar
} from 'lucide-react';

const approvals = [
  { id: 1, title: 'عرض تجاري - شركة العقارات الكبرى', requester: 'أحمد', amount: 85000, type: 'عرض تجاري', priority: 'high', status: 'pending', date: '2025-06-14' },
  { id: 2, title: 'خصم 20% للعميل المؤسسي', requester: 'محمد', amount: 0, type: 'خصم', priority: 'medium', status: 'pending', date: '2025-06-13' },
  { id: 3, title: 'تجديد اشتراك سنوي مع خصم', requester: 'خالد', amount: 45000, type: 'تجديد', priority: 'low', status: 'approved', date: '2025-06-12' },
  { id: 4, title: 'إضافة مستخدمين للمنصة', requester: 'سعد', amount: 0, type: 'وصول', priority: 'medium', status: 'pending', date: '2025-06-13' },
  { id: 5, title: 'تعديل بنود العقد القياسي', requester: 'أحمد', amount: 0, type: 'عقد', priority: 'high', status: 'rejected', date: '2025-06-11' },
];

export default function ApprovalsPage() {
  const [filter, setFilter] = useState('pending');
  const pendingCount = approvals.filter(a => a.status === 'pending').length;

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">مركز الموافقات</h1>
          <p className="text-sm text-gray-500 mt-1">الطلبات التي تنتظر موافقتك</p>
        </div>
        {pendingCount > 0 && (
          <span className="px-3 py-1.5 bg-red-100 text-red-700 text-sm font-bold rounded-full flex items-center gap-1.5">
            <AlertTriangle className="w-4 h-4" />
            {pendingCount} طلب معلق
          </span>
        )}
      </div>

      <div className="flex items-center gap-2">
        {[
          { key: 'all', label: 'الكل', count: approvals.length },
          { key: 'pending', label: 'معلق', count: approvals.filter(a => a.status === 'pending').length },
          { key: 'approved', label: 'معتمد', count: approvals.filter(a => a.status === 'approved').length },
          { key: 'rejected', label: 'مرفوض', count: approvals.filter(a => a.status === 'rejected').length },
        ].map((f) => (
          <button key={f.key} onClick={() => setFilter(f.key)} className={`px-4 py-2 text-sm font-bold rounded-lg transition-all flex items-center gap-2 ${
            filter === f.key ? 'bg-dealix-charcoal text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}>
            {f.label}
            <span className={`text-xs px-1.5 py-0.5 rounded-full ${filter === f.key ? 'bg-white/20' : 'bg-gray-200'}`}>{f.count}</span>
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-card border border-gray-100 divide-y divide-gray-100">
        {approvals.filter(a => filter === 'all' || a.status === filter).map((item) => (
          <div key={item.id} className="p-6 hover:bg-gray-50 transition-colors">
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                  item.status === 'pending' ? 'bg-amber-100' :
                  item.status === 'approved' ? 'bg-green-100' :
                  'bg-red-100'
                }`}>
                  {item.status === 'pending' ? <Clock className="w-5 h-5 text-amber-600" /> :
                   item.status === 'approved' ? <CheckCircle2 className="w-5 h-5 text-green-600" /> :
                   <XCircle className="w-5 h-5 text-red-600" />}
                </div>
                <div>
                  <h4 className="font-bold text-gray-900">{item.title}</h4>
                  <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                    <span className="flex items-center gap-1"><User className="w-3.5 h-3.5" /> {item.requester}</span>
                    <span className="flex items-center gap-1"><Calendar className="w-3.5 h-3.5" /> {item.date}</span>
                    <span className="px-2 py-0.5 bg-gray-100 rounded-full text-xs">{item.type}</span>
                    {item.amount > 0 && <span className="font-bold text-dealix-emerald">{item.amount.toLocaleString()} ريال</span>}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  item.priority === 'high' ? 'bg-red-100 text-red-700' :
                  item.priority === 'medium' ? 'bg-amber-100 text-amber-700' :
                  'bg-green-100 text-green-700'
                }`}>
                  {item.priority === 'high' ? 'عالي' : item.priority === 'medium' ? 'متوسط' : 'منخفض'}
                </span>
                {item.status === 'pending' && (
                  <div className="flex items-center gap-1">
                    <button className="p-2 bg-green-100 text-green-600 rounded-lg hover:bg-green-200 transition-colors">
                      <CheckCircle2 className="w-4 h-4" />
                    </button>
                    <button className="p-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors">
                      <XCircle className="w-4 h-4" />
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
