import { useState } from 'react';
import {
  Radio, Activity, Users, Globe, TrendingUp, AlertCircle,
  CheckCircle2, Zap, Shield, Server
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const liveData = [
  { time: '08:00', users: 12, requests: 180 },
  { time: '09:00', users: 25, requests: 420 },
  { time: '10:00', users: 38, requests: 680 },
  { time: '11:00', users: 45, requests: 850 },
  { time: '12:00', users: 52, requests: 920 },
  { time: '13:00', users: 48, requests: 780 },
];

const alerts = [
  { id: 1, level: 'warning', message: 'استخدام CPU مرتفع على خادم API', time: 'منذ 5 دقائق' },
  { id: 2, level: 'success', message: 'تم نسخ قاعدة البيانات احتياطياً', time: 'منذ 15 دقيقة' },
  { id: 3, level: 'info', message: 'عميل جديد سجل في المنصة', time: 'منذ 30 دقيقة' },
  { id: 4, level: 'warning', message: '3 طلبات API فشلت', time: 'منذ ساعة' },
];

const modules = [
  { name: 'API Gateway', status: 'online', uptime: '99.9%', latency: '45ms', icon: Server },
  { name: 'Auth Service', status: 'online', uptime: '99.8%', latency: '23ms', icon: Shield },
  { name: 'Payments', status: 'online', uptime: '99.9%', latency: '67ms', icon: Zap },
  { name: 'AI Engine', status: 'online', uptime: '99.5%', latency: '120ms', icon: Activity },
  { name: 'CRM Sync', status: 'warning', uptime: '98.2%', latency: '234ms', icon: Users },
  { name: 'Notifications', status: 'online', uptime: '99.9%', latency: '12ms', icon: Radio },
];

export default function CommandRoomPage() {
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h');

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">غرفة القيادة</h1>
          <p className="text-sm text-gray-500 mt-1">مراقبة النظام والعمليات اللحظية</p>
        </div>
        <div className="flex items-center gap-2">
          {['1h', '24h', '7d', '30d'].map((range) => (
            <button
              key={range}
              onClick={() => setSelectedTimeRange(range)}
              className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all ${
                selectedTimeRange === range
                  ? 'bg-dealix-emerald text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
              <CheckCircle2 className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">5/6</p>
              <p className="text-xs text-gray-500">الخدمات تعمل</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
              <Users className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">48</p>
              <p className="text-xs text-gray-500">مستخدم نشط الآن</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-dealix-gold/10 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-dealix-gold" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">920</p>
              <p className="text-xs text-gray-500">طلب API/ساعة</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
              <Globe className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">99.7%</p>
              <p className="text-xs text-gray-500">معدل uptime</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Live Traffic Chart */}
        <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4">حركة المرور اللحظية</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={liveData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="time" tick={{fontSize: 12}} />
              <YAxis tick={{fontSize: 12}} />
              <Tooltip />
              <Line type="monotone" dataKey="users" stroke="#1B5E3B" strokeWidth={2} name="المستخدمين" />
              <Line type="monotone" dataKey="requests" stroke="#C9A94C" strokeWidth={2} name="الطلبات" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Alerts */}
        <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-dealix-gold" />
            التنبيهات
          </h3>
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div key={alert.id} className={`flex items-start gap-3 p-3 rounded-lg ${
                alert.level === 'warning' ? 'bg-amber-50 border border-amber-100' :
                alert.level === 'success' ? 'bg-green-50 border border-green-100' :
                'bg-blue-50 border border-blue-100'
              }`}>
                <div className={`w-2 h-2 rounded-full mt-1.5 ${
                  alert.level === 'warning' ? 'bg-amber-500' :
                  alert.level === 'success' ? 'bg-green-500' :
                  'bg-blue-500'
                }`} />
                <div className="flex-1">
                  <p className="text-sm text-gray-800">{alert.message}</p>
                  <p className="text-xs text-gray-400 mt-1">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Services Status */}
      <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
        <h3 className="font-bold text-gray-900 mb-4">حالة الخدمات</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {modules.map((mod, i) => {
            const Icon = mod.icon;
            return (
              <div key={i} className="flex items-center gap-4 p-4 rounded-lg border border-gray-100 hover:border-dealix-emerald/30 transition-all">
                <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                  mod.status === 'online' ? 'bg-green-50' : 'bg-amber-50'
                }`}>
                  <Icon className={`w-5 h-5 ${mod.status === 'online' ? 'text-green-600' : 'text-amber-600'}`} />
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <p className="font-medium text-gray-800">{mod.name}</p>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      mod.status === 'online' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      {mod.status === 'online' ? 'يعمل' : 'تنبيه'}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                    <span>Uptime: {mod.uptime}</span>
                    <span>Latency: {mod.latency}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
