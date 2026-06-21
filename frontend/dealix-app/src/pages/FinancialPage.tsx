import {
  DollarSign, TrendingUp, Wallet,
  Receipt, ArrowUpRight, ArrowDownRight, Calendar
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const revenueTrend = [
  { month: 'يناير', income: 35000, expenses: 28000 },
  { month: 'فبراير', income: 42000, expenses: 30000 },
  { month: 'مارس', income: 48000, expenses: 32000 },
  { month: 'أبريل', income: 55000, expenses: 34000 },
  { month: 'مايو', income: 62000, expenses: 36000 },
  { month: 'يونيو', income: 78000, expenses: 38000 },
];

const transactions = [
  { id: 1, desc: 'اشتراك شركة العقارات', type: 'income', amount: 4900, date: '2025-06-14', status: 'completed' },
  { id: 2, desc: 'اشتراك المستشفى الوطني', type: 'income', amount: 9900, date: '2025-06-13', status: 'completed' },
  { id: 3, desc: 'بايلوت شركة التقنية', type: 'income', amount: 5000, date: '2025-06-12', status: 'completed' },
  { id: 4, desc: 'رواتب الفريق', type: 'expense', amount: 25000, date: '2025-06-01', status: 'completed' },
  { id: 5, desc: 'استضافة السحابة', type: 'expense', amount: 3500, date: '2025-06-01', status: 'completed' },
  { id: 6, desc: 'تسويق LinkedIn', type: 'expense', amount: 5000, date: '2025-06-05', status: 'completed' },
];

export default function FinancialPage() {
  const totalIncome = transactions.filter(t => t.type === 'income').reduce((s, t) => s + t.amount, 0);
  const totalExpenses = transactions.filter(t => t.type === 'expense').reduce((s, t) => s + t.amount, 0);
  const netIncome = totalIncome - totalExpenses;
  const margin = Math.round((netIncome / totalIncome) * 100);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">لوحة التحكم المالية</h1>
          <p className="text-sm text-gray-500 mt-1">الإيرادات والمصروفات والتدفق النقدي</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <Calendar className="w-4 h-4" />
          <span>يونيو 2025</span>
        </div>
      </div>

      {/* Financial KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><DollarSign className="w-5 h-5 text-green-500" /><span className="text-sm text-gray-500">الإيرادات</span></div>
          <p className="text-2xl font-bold text-gray-900">{totalIncome.toLocaleString()}</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +18%</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Receipt className="w-5 h-5 text-red-500" /><span className="text-sm text-gray-500">المصروفات</span></div>
          <p className="text-2xl font-bold text-gray-900">{totalExpenses.toLocaleString()}</p>
          <p className="text-xs text-red-500 flex items-center gap-1 mt-1"><ArrowDownRight className="w-3 h-3" /> -5%</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><Wallet className="w-5 h-5 text-dealix-emerald" /><span className="text-sm text-gray-500">صافي الربح</span></div>
          <p className="text-2xl font-bold text-gray-900">{netIncome.toLocaleString()}</p>
          <p className="text-xs text-gray-400 mt-1">ريال سعودي</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2"><TrendingUp className="w-5 h-5 text-dealix-gold" /><span className="text-sm text-gray-500">هامش الربح</span></div>
          <p className="text-2xl font-bold text-gray-900">{margin}%</p>
          <p className="text-xs text-green-600 flex items-center gap-1 mt-1"><ArrowUpRight className="w-3 h-3" /> +3%</p>
        </div>
      </div>

      {/* Revenue vs Expenses Chart */}
      <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
        <h3 className="font-bold text-gray-900 mb-4">الإيرادات vs المصروفات</h3>
        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={revenueTrend}>
            <defs>
              <linearGradient id="incGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#1B5E3B" stopOpacity={0.3}/><stop offset="95%" stopColor="#1B5E3B" stopOpacity={0}/></linearGradient>
              <linearGradient id="expGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#EF4444" stopOpacity={0.2}/><stop offset="95%" stopColor="#EF4444" stopOpacity={0}/></linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="month" tick={{fontSize: 12}} />
            <YAxis tick={{fontSize: 12}} />
            <Tooltip />
            <Area type="monotone" dataKey="income" stroke="#1B5E3B" fill="url(#incGrad)" name="الإيرادات" strokeWidth={2} />
            <Area type="monotone" dataKey="expenses" stroke="#EF4444" fill="url(#expGrad)" name="المصروفات" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Transactions */}
      <div className="bg-white rounded-xl shadow-card border border-gray-100">
        <div className="p-6 border-b border-gray-100"><h3 className="font-bold text-gray-900">المعاملات الأخيرة</h3></div>
        <div className="divide-y divide-gray-100">
          {transactions.map((t) => (
            <div key={t.id} className="p-4 flex items-center justify-between hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-3">
                <div className={`w-9 h-9 rounded-lg flex items-center justify-center ${t.type === 'income' ? 'bg-green-100' : 'bg-red-100'}`}>
                  {t.type === 'income' ? <ArrowUpRight className="w-4 h-4 text-green-600" /> : <ArrowDownRight className="w-4 h-4 text-red-600" />}
                </div>
                <div>
                  <p className="font-medium text-gray-800">{t.desc}</p>
                  <p className="text-xs text-gray-400">{t.date}</p>
                </div>
              </div>
              <span className={`font-bold ${t.type === 'income' ? 'text-green-600' : 'text-red-500'}`}>
                {t.type === 'income' ? '+' : '-'}{t.amount.toLocaleString()} ريال
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
