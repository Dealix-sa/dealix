import { useState, useEffect, useCallback } from 'react';
import {
  Radio, Activity, Users, Globe, TrendingUp, AlertCircle,
  CheckCircle2, Zap, Shield, Server, Play, RefreshCw, Mail
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

const modules = [
  { name: 'API Gateway', status: 'online', uptime: '99.9%', latency: '45ms', icon: Server },
  { name: 'Auth Service', status: 'online', uptime: '99.8%', latency: '23ms', icon: Shield },
  { name: 'Payments', status: 'online', uptime: '99.9%', latency: '67ms', icon: Zap },
  { name: 'AI Engine', status: 'online', uptime: '99.5%', latency: '120ms', icon: Activity },
  { name: 'CRM Sync', status: 'warning', uptime: '98.2%', latency: '234ms', icon: Users },
  { name: 'Notifications', status: 'online', uptime: '99.9%', latency: '12ms', icon: Radio },
];

const API_BASE = '/api/v1';

interface DashboardData {
  generated_at?: string;
  leads_waiting_24h_plus?: { count: number; items: unknown[] };
  friction_last_7d?: { total: number };
  renewals_due_next_7d?: { count: number };
  pending_approvals?: { count: number };
}

interface OutreachQueueData {
  count: number;
  items: { id: string; channel: string; status: string; message: string }[];
}

interface DailyTarget {
  account_id: string;
  company_name: string;
  sector: string;
  region: string;
  icp_score: number;
  tier: string;
  email: {
    subject: string;
    offer_matched: string;
    pain_points_used: string[];
  };
  draft_id: string;
}

interface DailyOpsStatus {
  ran: boolean;
  run_at?: string;
  dry_run?: boolean;
  top_targets_count?: number;
  drafts_created?: number;
  tier_counts?: { A: number; B: number; C: number };
}

interface DailyTargetsData {
  targets: DailyTarget[];
  tier_counts?: { A: number; B: number; C: number };
  run_at?: string;
}

const TIER_COLORS: Record<string, string> = {
  A: 'bg-green-100 text-green-800',
  B: 'bg-blue-100 text-blue-800',
  C: 'bg-amber-100 text-amber-800',
  DQ: 'bg-gray-100 text-gray-600',
};

async function apiFetch<T>(path: string, opts: RequestInit = {}): Promise<T | null> {
  try {
    const res = await fetch(`${API_BASE}${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...opts,
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

export default function CommandRoomPage() {
  const [selectedTimeRange, setSelectedTimeRange] = useState('24h');
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [outreachQueue, setOutreachQueue] = useState<OutreachQueueData | null>(null);
  const [dailyStatus, setDailyStatus] = useState<DailyOpsStatus | null>(null);
  const [dailyTargets, setDailyTargets] = useState<DailyTargetsData | null>(null);
  const [loadingDashboard, setLoadingDashboard] = useState(false);
  const [loadingTargets, setLoadingTargets] = useState(false);
  const [runningEngine, setRunningEngine] = useState(false);
  const [engineMessage, setEngineMessage] = useState('');

  const fetchDashboard = useCallback(async () => {
    setLoadingDashboard(true);
    const data = await apiFetch<DashboardData>('/founder/dashboard');
    setDashboard(data);
    setLoadingDashboard(false);
  }, []);

  const fetchOutreach = useCallback(async () => {
    const data = await apiFetch<OutreachQueueData>('/outreach/queue?limit=20');
    setOutreachQueue(data);
  }, []);

  const fetchDailyOps = useCallback(async () => {
    setLoadingTargets(true);
    const status = await apiFetch<DailyOpsStatus>('/daily-ops/status');
    const targets = await apiFetch<DailyTargetsData>('/daily-ops/targets');
    setDailyStatus(status);
    setDailyTargets(targets);
    setLoadingTargets(false);
  }, []);

  useEffect(() => {
    fetchDashboard();
    fetchOutreach();
    fetchDailyOps();
  }, [fetchDashboard, fetchOutreach, fetchDailyOps]);

  const runDailyEngine = async () => {
    setRunningEngine(true);
    setEngineMessage('جاري تشغيل محرك الاستهداف اليومي...');
    const result = await apiFetch<Record<string, unknown>>('/daily-ops/run', { method: 'POST' });
    if (result) {
      setEngineMessage('تم بنجاح. تحديث النتائج...');
      await fetchDailyOps();
      setEngineMessage('');
    } else {
      setEngineMessage('فشل التشغيل — تحقق من السجلات');
    }
    setRunningEngine(false);
  };

  const leadsWaiting = dashboard?.leads_waiting_24h_plus?.count ?? 0;
  const pendingApprovals = dashboard?.pending_approvals?.count ?? 0;
  const renewalsDue = dashboard?.renewals_due_next_7d?.count ?? 0;
  const outreachCount = outreachQueue?.count ?? 0;

  const targets = dailyTargets?.targets ?? [];
  const tierCounts = dailyTargets?.tier_counts ?? { A: 0, B: 0, C: 0 };

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">غرفة القيادة</h1>
          <p className="text-sm text-gray-500 mt-1">مراقبة النظام والعمليات اللحظية</p>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
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
          <button
            onClick={fetchDashboard}
            disabled={loadingDashboard}
            className="px-3 py-1.5 text-xs font-bold rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 flex items-center gap-1"
          >
            <RefreshCw className={`w-3 h-3 ${loadingDashboard ? 'animate-spin' : ''}`} />
            تحديث
          </button>
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
              <p className="text-2xl font-bold text-gray-900">{leadsWaiting}</p>
              <p className="text-xs text-gray-500">عملاء محتملون بانتظار 24h+</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-dealix-gold/10 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-dealix-gold" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{renewalsDue}</p>
              <p className="text-xs text-gray-500">تجديدات مستحقة هذا الأسبوع</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
              <Globe className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{pendingApprovals}</p>
              <p className="text-xs text-gray-500">موافقات معلقة</p>
            </div>
          </div>
        </div>
      </div>

      {/* Daily Targeting Engine Panel */}
      <div className="bg-white rounded-xl p-6 shadow-card border border-gray-100">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-gray-900 flex items-center gap-2">
              <Mail className="w-5 h-5 text-dealix-emerald" />
              محرك الاستهداف اليومي
            </h3>
            {dailyStatus?.ran && (
              <p className="text-xs text-gray-500 mt-1">
                آخر تشغيل: {dailyStatus.run_at ? new Date(dailyStatus.run_at).toLocaleString('ar-SA') : '—'}
                {dailyStatus.dry_run ? ' (وضع تجريبي)' : ' (مسودات Gmail)'}
              </p>
            )}
            {!dailyStatus?.ran && (
              <p className="text-xs text-amber-600 mt-1">لم يتم التشغيل اليوم بعد</p>
            )}
          </div>
          <div className="flex items-center gap-3">
            {dailyStatus?.ran && (
              <div className="flex gap-2 text-sm">
                <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-bold">
                  A: {tierCounts?.A ?? 0}
                </span>
                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-bold">
                  B: {tierCounts?.B ?? 0}
                </span>
              </div>
            )}
            <button
              onClick={runDailyEngine}
              disabled={runningEngine}
              className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white text-sm font-bold rounded-lg hover:bg-dealix-emerald/90 transition-all disabled:opacity-50"
            >
              <Play className={`w-4 h-4 ${runningEngine ? 'animate-pulse' : ''}`} />
              {runningEngine ? 'جاري التشغيل...' : 'تشغيل استهداف اليوم'}
            </button>
          </div>
        </div>

        {engineMessage && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-100 rounded-lg text-sm text-blue-800">
            {engineMessage}
          </div>
        )}

        {loadingTargets ? (
          <div className="py-8 text-center text-gray-400 text-sm">جاري التحميل...</div>
        ) : targets.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">#</th>
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">الشركة</th>
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">القطاع</th>
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">المنطقة</th>
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">النقاط</th>
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">الفئة</th>
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">العرض المناسب</th>
                  <th className="text-right pb-2 font-semibold text-gray-600 text-xs">المسودة</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {targets.map((t, i) => (
                  <tr key={t.account_id} className="hover:bg-gray-50 transition-colors">
                    <td className="py-3 text-gray-400 text-xs">{i + 1}</td>
                    <td className="py-3 font-medium text-gray-900">{t.company_name}</td>
                    <td className="py-3 text-gray-600">{t.sector}</td>
                    <td className="py-3 text-gray-600">{t.region}</td>
                    <td className="py-3 font-bold text-gray-900">{t.icp_score}/100</td>
                    <td className="py-3">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${TIER_COLORS[t.tier] ?? 'bg-gray-100 text-gray-600'}`}>
                        {t.tier}
                      </span>
                    </td>
                    <td className="py-3 text-xs text-gray-600 max-w-[200px] truncate">
                      {t.email?.offer_matched ?? '—'}
                    </td>
                    <td className="py-3 text-xs">
                      {t.draft_id && t.draft_id !== 'DRY_RUN' && !t.draft_id.startsWith('ERROR') ? (
                        <span className="text-green-600 font-medium">جاهزة</span>
                      ) : (
                        <span className="text-gray-400">تجريبي</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-6 text-center text-gray-400 text-sm">
            لا توجد نتائج — اضغط "تشغيل استهداف اليوم" لتحميل التارجتس
          </div>
        )}
      </div>

      {/* Outreach Queue Summary */}
      {outreachQueue && outreachCount > 0 && (
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <h3 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
            <Radio className="w-4 h-4 text-dealix-gold" />
            طابور التواصل ({outreachCount} رسالة)
          </h3>
          <div className="space-y-2">
            {outreachQueue.items.slice(0, 5).map((item) => (
              <div key={item.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg text-sm">
                <span className="text-gray-700 truncate max-w-[60%]">{item.message?.slice(0, 60)}...</span>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-gray-500">{item.channel}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                    item.status === 'approved' ? 'bg-green-100 text-green-700' :
                    item.status === 'queued' ? 'bg-amber-100 text-amber-700' :
                    'bg-gray-100 text-gray-600'
                  }`}>
                    {item.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

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
            {dashboard ? (
              <>
                {leadsWaiting > 0 && (
                  <div className="flex items-start gap-3 p-3 rounded-lg bg-amber-50 border border-amber-100">
                    <div className="w-2 h-2 rounded-full mt-1.5 bg-amber-500" />
                    <div className="flex-1">
                      <p className="text-sm text-gray-800">{leadsWaiting} عميل محتمل بانتظار أكثر من 24 ساعة</p>
                    </div>
                  </div>
                )}
                {pendingApprovals > 0 && (
                  <div className="flex items-start gap-3 p-3 rounded-lg bg-blue-50 border border-blue-100">
                    <div className="w-2 h-2 rounded-full mt-1.5 bg-blue-500" />
                    <div className="flex-1">
                      <p className="text-sm text-gray-800">{pendingApprovals} موافقة تحتاج مراجعة</p>
                    </div>
                  </div>
                )}
                {renewalsDue > 0 && (
                  <div className="flex items-start gap-3 p-3 rounded-lg bg-green-50 border border-green-100">
                    <div className="w-2 h-2 rounded-full mt-1.5 bg-green-500" />
                    <div className="flex-1">
                      <p className="text-sm text-gray-800">{renewalsDue} تجديد مستحق الأسبوع القادم</p>
                    </div>
                  </div>
                )}
                {leadsWaiting === 0 && pendingApprovals === 0 && renewalsDue === 0 && (
                  <div className="flex items-start gap-3 p-3 rounded-lg bg-green-50 border border-green-100">
                    <div className="w-2 h-2 rounded-full mt-1.5 bg-green-500" />
                    <div className="flex-1">
                      <p className="text-sm text-gray-800">لا توجد تنبيهات عاجلة الآن</p>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <p className="text-sm text-gray-400">
                {loadingDashboard ? 'جاري التحميل...' : 'البيانات غير متاحة حالياً'}
              </p>
            )}
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
