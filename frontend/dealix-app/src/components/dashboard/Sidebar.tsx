import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard, Crosshair, Swords, FileCheck, ShieldCheck,
  Megaphone, TrendingUp, Target, BarChart3, LineChart,
  Settings, ChevronLeft, ChevronRight, Crown, Zap,
  FileText, FileSpreadsheet, Users, Calendar, FolderKanban,
  DollarSign, Bell
} from 'lucide-react';

interface Props {
  isOpen: boolean;
  setIsOpen: (v: boolean) => void;
}

const navGroups = [
  {
    label: 'القائمة الرئيسية',
    items: [
      { path: '/cockpit', label: 'كابينة المؤسس', icon: LayoutDashboard },
      { path: '/command-room', label: 'غرفة القيادة', icon: Crosshair },
      { path: '/war-room', label: 'غرفة الحرب', icon: Swords },
    ],
  },
  {
    label: 'العمليات',
    items: [
      { path: '/crm', label: 'إدارة العملاء (CRM)', icon: Users },
      { path: '/calendar', label: 'التقويم التنفيذي', icon: Calendar },
      { path: '/projects', label: 'المشاريع والمهام', icon: FolderKanban },
      { path: '/targeting', label: 'الاستهداف اليومي', icon: Crosshair },
      { path: '/drafts', label: 'مركز المسودات', icon: FileText },
      { path: '/reports', label: 'التقارير المؤتمتة', icon: FileSpreadsheet },
      { path: '/evidence', label: 'لوحة الأدلة', icon: FileCheck },
      { path: '/approvals', label: 'مركز الموافقات', icon: ShieldCheck },
      { path: '/marketing', label: 'عمليات التسويق', icon: Megaphone },
      { path: '/sales', label: 'عمليات المبيعات', icon: TrendingUp },
    ],
  },
  {
    label: 'التخطيط والتحليل',
    items: [
      { path: '/strategy', label: 'الاستراتيجية والأهداف', icon: Target },
      { path: '/financial', label: 'التحكم المالي', icon: BarChart3 },
      { path: '/investor', label: 'علاقات المستثمرين', icon: DollarSign },
      { path: '/analytics', label: 'التحليلات والتقارير', icon: LineChart },
    ],
  },
  {
    label: 'النظام',
    items: [
      { path: '/notifications', label: 'الإشعارات', icon: Bell },
      { path: '/settings', label: 'الإعدادات', icon: Settings },
    ],
  },
];

export default function Sidebar({ isOpen, setIsOpen }: Props) {
  const location = useLocation();

  return (
    <aside
      className={`fixed right-0 top-0 h-full bg-dealix-charcoal text-white z-40 transition-all duration-300 flex flex-col ${
        isOpen ? 'w-64' : 'w-16'
      }`}
      style={{ direction: 'rtl' }}
    >
      {/* Logo */}
      <div className={`flex items-center gap-3 h-16 px-4 border-b border-white/10 ${!isOpen && 'justify-center px-2'}`}>
        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-dealix-emerald to-dealix-forest flex items-center justify-center shrink-0">
          <Crown className="w-5 h-5 text-dealix-gold" />
        </div>
        {isOpen && (
          <div className="overflow-hidden">
            <h1 className="font-bold text-lg tracking-wide">Dealix</h1>
            <p className="text-[10px] text-white/40 -mt-1">Founder OS</p>
          </div>
        )}
      </div>

      {/* Toggle */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="absolute -left-3 top-20 w-6 h-6 bg-dealix-gold rounded-full flex items-center justify-center text-dealix-charcoal hover:scale-110 transition-transform z-50"
      >
        {isOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
      </button>

      {/* Nav */}
      <nav className="flex-1 overflow-y-auto py-4 scrollbar-thin px-2 space-y-6">
        {navGroups.map((group, gi) => (
          <div key={gi}>
            {isOpen && (
              <p className="px-3 mb-2 text-[10px] font-bold text-white/30 uppercase tracking-widest">
                {group.label}
              </p>
            )}
            <div className="space-y-1">
              {group.items.map((item) => {
                const isActive = location.pathname === item.path;
                const Icon = item.icon;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group ${
                      isActive
                        ? 'bg-dealix-emerald/20 text-dealix-gold border-r-2 border-dealix-gold'
                        : 'text-white/60 hover:text-white hover:bg-white/5'
                    } ${!isOpen && 'justify-center px-2'}`}
                    title={!isOpen ? item.label : undefined}
                  >
                    <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-dealix-gold' : ''}`} />
                    {isOpen && <span className="text-sm font-medium truncate">{item.label}</span>}
                    {isActive && isOpen && <Zap className="w-3 h-3 mr-auto text-dealix-gold animate-pulse" />}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      {/* Bottom status */}
      {isOpen && (
        <div className="p-3 border-t border-white/10">
          <div className="bg-white/5 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
              <span className="text-xs text-white/60">النظام يعمل</span>
            </div>
            <p className="text-[10px] text-white/30">Dealix Founder OS v1.0</p>
          </div>
        </div>
      )}
    </aside>
  );
}
