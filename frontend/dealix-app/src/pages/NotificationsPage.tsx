import { useState } from 'react';
import {
  Bell, CheckCircle2, AlertTriangle, AlertCircle, Info,
  Clock, Filter, CheckCheck, Trash2, Zap,
  TrendingUp, Users, DollarSign, X
} from 'lucide-react';

type NotifType = 'success' | 'warning' | 'error' | 'info';
type NotifCategory = 'all' | 'sales' | 'system' | 'team' | 'finance';

interface Notification {
  id: number;
  title: string;
  message: string;
  type: NotifType;
  category: NotifCategory;
  time: string;
  read: boolean;
}

const notifications: Notification[] = [
  { id: 1, title: 'صفقة جديدة مغلقة!', message: 'تم إغلاق صفقة شركة العقارات الكبرى بقيمة 45,000 ريال', type: 'success', category: 'sales', time: 'منذ 5 دقائق', read: false },
  { id: 2, title: 'تنبيه: Runway منخفض', message: 'Runway الحالي 13 شهراً. يُنصح بالتخطيط للجولة القادمة', type: 'warning', category: 'finance', time: 'منذ 15 دقيقة', read: false },
  { id: 3, title: 'فشل في مزامنة البيانات', message: 'تعذر الاتصال بخادم CRM الخارجي. جارٍ إعادة المحاولة', type: 'error', category: 'system', time: 'منذ 30 دقيقة', read: false },
  { id: 4, title: 'عميل جديد مسجل', message: 'مستشفى الرياض الوطني سجل في المنصة', type: 'info', category: 'sales', time: 'منذ ساعة', read: true },
  { id: 5, title: 'مهمة متأخرة', message: 'تحليل بيانات Q2 متأخر بـ 2 يوم', type: 'warning', category: 'team', time: 'منذ ساعتين', read: false },
  { id: 6, title: 'إنجاز: هدف الشهر', message: 'تم تحقيق هدف المبيعات الشهري بنسبة 105%', type: 'success', category: 'sales', time: 'منذ 3 ساعات', read: true },
  { id: 7, title: 'تحديث النظام', message: 'تم تحديث Dealix إلى الإصدار 2.4.1 بنجاح', type: 'info', category: 'system', time: 'منذ 5 ساعات', read: true },
  { id: 8, title: 'انضمام عضو جديد', message: 'انضم ناصر العتيبي لفريق المبيعات', type: 'info', category: 'team', time: 'منذ 6 ساعات', read: true },
  { id: 9, title: 'تجاوز الحد', message: 'استهلاك API تجاوز 85% من الحد اليومي', type: 'warning', category: 'system', time: 'منذ 8 ساعات', read: false },
  { id: 10, title: 'دفعة مستلمة', message: 'تم استلام دفعة 120,000 ريال من شركة STC', type: 'success', category: 'finance', time: 'أمس', read: true },
];

const typeConfig = {
  success: { icon: CheckCircle2, color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-100' },
  warning: { icon: AlertTriangle, color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-100' },
  error: { icon: AlertCircle, color: 'text-red-600', bg: 'bg-red-50', border: 'border-red-100' },
  info: { icon: Info, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-100' },
};

const categoryFilters: { key: NotifCategory; label: string; count: number }[] = [
  { key: 'all', label: 'الكل', count: 10 },
  { key: 'sales', label: 'مبيعات', count: 3 },
  { key: 'system', label: 'نظام', count: 3 },
  { key: 'team', label: 'فريق', count: 2 },
  { key: 'finance', label: 'مالية', count: 2 },
];

export default function NotificationsPage() {
  const [notifs, setNotifs] = useState(notifications);
  const [activeFilter, setActiveFilter] = useState<NotifCategory>('all');
  const [showUnreadOnly, setShowUnreadOnly] = useState(false);

  const filtered = notifs.filter(n => {
    const matchesCategory = activeFilter === 'all' || n.category === activeFilter;
    const matchesUnread = !showUnreadOnly || !n.read;
    return matchesCategory && matchesUnread;
  });

  const unreadCount = notifs.filter(n => !n.read).length;

  const markAllRead = () => setNotifs(prev => prev.map(n => ({ ...n, read: true })));
  const markRead = (id: number) => setNotifs(prev => prev.map(n => n.id === id ? { ...n, read: true } : n));
  const clearAll = () => setNotifs([]);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Bell className="w-6 h-6 text-gray-900" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
                {unreadCount}
              </span>
            )}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">مركز الإشعارات</h1>
            <p className="text-sm text-gray-500 mt-1">جميع التنبيهات والإشعارات الحية</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={markAllRead} className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg text-sm hover:bg-gray-50">
            <CheckCheck className="w-4 h-4" /> تعليم الكل مقروء
          </button>
          <button onClick={clearAll} className="flex items-center gap-2 px-3 py-2 border border-red-200 text-red-600 rounded-lg text-sm hover:bg-red-50">
            <Trash2 className="w-4 h-4" /> مسح الكل
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Filters */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-4">
            <div className="flex items-center gap-2 mb-3">
              <Filter className="w-4 h-4 text-gray-500" />
              <span className="font-bold text-gray-900 text-sm">التصفية</span>
            </div>
            <div className="space-y-1">
              {categoryFilters.map((cat) => (
                <button
                  key={cat.key}
                  onClick={() => setActiveFilter(cat.key)}
                  className={`w-full flex items-center justify-between px-3 py-2 rounded-lg text-sm transition-colors ${
                    activeFilter === cat.key ? 'bg-dealix-emerald/10 text-dealix-emerald font-bold' : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <span>{cat.label}</span>
                  <span className={`text-xs px-1.5 py-0.5 rounded-full ${
                    activeFilter === cat.key ? 'bg-dealix-emerald text-white' : 'bg-gray-100 text-gray-500'
                  }`}>{cat.count}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={showUnreadOnly}
                onChange={(e) => setShowUnreadOnly(e.target.checked)}
                className="w-4 h-4 accent-dealix-emerald"
              />
              <span className="text-sm text-gray-700">غير المقروء فقط</span>
            </label>
          </div>

          {/* Quick Stats */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-4">
            <h4 className="font-bold text-gray-900 text-sm mb-3">ملخص سريع</h4>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Zap className="w-4 h-4 text-dealix-emerald" />
                  <span className="text-xs text-gray-600">غير مقروء</span>
                </div>
                <span className="font-bold text-gray-900 text-sm">{unreadCount}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-green-500" />
                  <span className="text-xs text-gray-600">مبيعات</span>
                </div>
                <span className="font-bold text-gray-900 text-sm">{notifs.filter(n => n.category === 'sales').length}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-amber-500" />
                  <span className="text-xs text-gray-600">مالية</span>
                </div>
                <span className="font-bold text-gray-900 text-sm">{notifs.filter(n => n.category === 'finance').length}</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-blue-500" />
                  <span className="text-xs text-gray-600">فريق</span>
                </div>
                <span className="font-bold text-gray-900 text-sm">{notifs.filter(n => n.category === 'team').length}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Notifications List */}
        <div className="lg:col-span-3">
          <div className="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
              <h3 className="font-bold text-gray-900">الإشعارات</h3>
              <span className="text-xs text-gray-400">{filtered.length} إشعار</span>
            </div>
            <div className="divide-y divide-gray-50">
              {filtered.length === 0 ? (
                <div className="p-12 text-center">
                  <Bell className="w-12 h-12 text-gray-200 mx-auto mb-3" />
                  <p className="text-gray-400">لا توجد إشعارات</p>
                </div>
              ) : (
                filtered.map((notif) => {
                  const config = typeConfig[notif.type];
                  const Icon = config.icon;
                  return (
                    <div
                      key={notif.id}
                      className={`px-5 py-4 flex items-start gap-4 hover:bg-gray-50 transition-colors cursor-pointer ${
                        !notif.read ? 'bg-dealix-emerald/[0.02]' : ''
                      }`}
                      onClick={() => markRead(notif.id)}
                    >
                      <div className={`w-10 h-10 rounded-lg ${config.bg} flex items-center justify-center shrink-0`}>
                        <Icon className={`w-5 h-5 ${config.color}`} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <p className={`text-sm ${!notif.read ? 'font-bold text-gray-900' : 'text-gray-700'}`}>
                            {notif.title}
                          </p>
                          {!notif.read && <span className="w-2 h-2 rounded-full bg-dealix-emerald" />}
                        </div>
                        <p className="text-sm text-gray-500">{notif.message}</p>
                        <div className="flex items-center gap-3 mt-2">
                          <span className="text-xs text-gray-400 flex items-center gap-1">
                            <Clock className="w-3 h-3" /> {notif.time}
                          </span>
                          <span className={`text-[10px] px-1.5 py-0.5 rounded-full font-bold ${
                            notif.category === 'sales' ? 'bg-blue-100 text-blue-600' :
                            notif.category === 'finance' ? 'bg-amber-100 text-amber-600' :
                            notif.category === 'system' ? 'bg-gray-100 text-gray-600' :
                            'bg-purple-100 text-purple-600'
                          }`}>
                            {notif.category === 'sales' ? 'مبيعات' :
                             notif.category === 'finance' ? 'مالية' :
                             notif.category === 'system' ? 'نظام' : 'فريق'}
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setNotifs(prev => prev.filter(n => n.id !== notif.id));
                        }}
                        className="p-1 hover:bg-gray-200 rounded transition-colors"
                      >
                        <X className="w-4 h-4 text-gray-400" />
                      </button>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
