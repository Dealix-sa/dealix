import { useState } from 'react';
import {
  Crosshair, Target, Phone, Mail, MessageSquare, Send,
  CheckCircle2, Clock, AlertCircle, Building2, MapPin,
  TrendingUp, Star, ChevronRight, Copy, Check, RefreshCw
} from 'lucide-react';
import { Switch } from '@/components/ui/switch';

const dailyTargets = [
  { id: 1, company: 'مجموعة بن لادن السعودية', sector: 'عقارات', size: '5000+', location: 'جدة', contact: 'م. عبدالله بن لادن', role: 'مدير تطوير الأعمال', priority: 'high', status: 'new', phone: '+966 12 555 0000', email: 'abdullah@binladin.com', linkedIn: 'linkedin.com/in/abdullah-binladin' },
  { id: 2, company: 'مستشفى الملك فيصل التخصصي', sector: 'صحة', size: '2000+', location: 'الرياض', contact: 'د. فهد المحمد', role: 'مدير تقنية المعلومات', priority: 'high', status: 'new', phone: '+966 11 464 7272', email: 'f.almohammed@kfshrc.edu.sa', linkedIn: 'linkedin.com/in/dr-fahad' },
  { id: 3, company: 'شركة جرير للتسويق', sector: 'تجارة', size: '3000+', location: 'الرياض', contact: 'م. خالد الجرير', role: 'الرئيس التنفيذي', priority: 'medium', status: 'contacted', phone: '+966 11 215 8000', email: 'ceo@jarir.com', linkedIn: 'linkedin.com/in/khaled-jarir' },
  { id: 4, company: 'STC Solutions', sector: 'تقنية', size: '5000+', location: 'الرياض', contact: 'م. ناصر الدوسري', role: 'نائب الرئيس للرقمية', priority: 'high', status: 'new', phone: '+966 11 452 3000', email: 'n.dossary@stc.com.sa', linkedIn: 'linkedin.com/in/nasser-dossary' },
  { id: 5, company: 'مصنع ينبع الصناعي', sector: 'صناعة', size: '800+', location: 'ينبع', contact: 'م. سعد الحربي', role: 'مدير العمليات', priority: 'medium', status: 'new', phone: '+966 14 396 2000', email: 's.alharbi@yanbufactory.com', linkedIn: 'linkedin.com/in/saad-alharbi' },
];

const callScripts = {
  'عقارات': [
    'السلام عليكم، أنا [اسمك] من Dealix. نقدم نظام ذكاء اصطناعي لإدارة المبيعات العقارية. هل لديكم تحدي في تتبع العملاء المحتملين؟',
    'نحن نساعد شركات عقارية مثل [شركة منافسة] على زيادة مبيعاتها 35% عبر أتمتة المتابعة. هل يهمك أن نعمل تشخيص مجاني؟',
  ],
  'صحة': [
    'السلام عليكم، أنا [اسمك] من Dealix. نحن نساعد المستشفيات على تحسين تجربة المرضى والامتثال لـ PDPL. هل تواجهون تحديات في إدارة بيانات المرضى؟',
    'نظامنا مُعتمد من عدة مستشفيات سعودية ويساعد على تقليل وقت الانتظار 40%. هل ترغبون في بايلوت مجاني لمدة 7 أيام؟',
  ],
  'تجارة': [
    'السلام عليكم، أنا [اسمك] من Dealix. نقدم حلول ذكاء اصطناعي لتحليل سلوك العملاء وزيادة المبيعات. هل تستخدمون نظام CRM حالياً؟',
    'شركات التجزئة التي تستخدم Dealix حققت زيادة 28% في معدل التحويل. هل يمكننا جدولة 15 دقيقة لتقديم التشخيص؟',
  ],
  'تقنية': [
    'السلام عليكم، أنا [اسمك] من Dealix. نحن SaaS سعودي لإدارة الإيرادات بالذكاء الاصطناعي. نبحث عن شركات تقنية لشراكات استراتيجية.',
    'نظامنا يتكامل مع 172 نقطة API ويوفر تحليلات متقدمة. هل لديكم اهتمام في شراكة تقنية؟',
  ],
  'صناعة': [
    'السلام عليكم، أنا [اسمك] من Dealix. نساعد المصانع على أتمتة عمليات المبيعات وتحسين الكفاءة. هل تواجهون تحديات في إدارة العملاء B2B؟',
    'Dealix يقلل وقت المتابعة 60% ويزيد مبيعات B2B الصناعية. هل ترغبون في تشخيص مجاني؟',
  ],
};

const emailTemplates = [
  { id: 1, name: 'تقديم أولي', subject: 'Dealix - نظام الذكاء الاصطناعي لإدارة إيرادات {{company}}', body: 'السيد {{contact}}،\n\nأتشرف بالتعريف بـ Dealix - أول منصة سعودية لإدارة الإيرادات بالذكاء الاصطناعي.\n\nنحن نساعد شركات {{sector}} مثل {{company}} على:\n• زيادة المبيعات 35%\n• تقليل وقت المتابعة 60%\n• الامتثال الكامل لـ PDPL\n\nهل يمكننا جدولة 15 دقيقة لتقديم التشخيص المجاني؟\n\nمع خالص التقدير،\n{{sender}}\nمؤسس Dealix\n{{phone}}' },
  { id: 2, name: 'متابعة', subject: 'متابعة - {{company}} + Dealix', body: 'السيد {{contact}}،\n\nأتمنى أن تكون بخير. أردت المتابعة على رسالتي السابقة حول Dealix.\n\nلقد ساعدنا شركة مشابهة في قطاع {{sector}} على تحقيق نتائج مبهرة خلال 30 يوم فقط.\n\nهل لديكم 10 دقائق هذا الأسبوع لمكالمة تعريفية؟\n\n{{sender}}' },
  { id: 3, name: 'عرض بايلوت', subject: 'عرض بايلوت حصري - {{company}}', body: 'السيد {{contact}}،\n\نحن نقدم لـ {{company}} عرض بايلوت حصري:\n\n• 7 أيام تجربة كاملة\n• تشخيص مفصل لأعمالكم\n• تقرير توصيات مخصص\n• ضمان استرداد 100%\n\nالاستثمار: 2,500 ريال فقط\n\nهل تقبلون التحدي؟\n\n{{sender}}' },
];

export default function TargetingPage() {
  const [selectedTarget, setSelectedTarget] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<'targets' | 'scripts' | 'emails'>('targets');
  const [copiedId, setCopiedId] = useState<number | null>(null);
  const [callLog, setCallLog] = useState<Record<number, 'called' | 'answered' | 'meeting' | 'rejected'>>({});

  const copyToClipboard = (text: string, id: number) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    });
  };

  const logCall = (id: number, result: 'called' | 'answered' | 'meeting' | 'rejected') => {
    setCallLog(prev => ({ ...prev, [id]: result }));
  };

  const selected = dailyTargets.find(t => t.id === selectedTarget);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">الاستهداف اليومي</h1>
          <p className="text-sm text-gray-500 mt-1">{new Date().toLocaleDateString('ar-SA')} - {dailyTargets.filter(t => t.status === 'new').length} أهداف جديدة</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-3 py-1.5 bg-dealix-gold/10 text-dealix-gold text-sm font-bold rounded-full flex items-center gap-1">
            <Target className="w-4 h-4" /> 5 أهداف اليوم
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Target List */}
        <div className="lg:col-span-1 space-y-3">
          {dailyTargets.map((target) => {
            const logged = callLog[target.id];
            return (
              <button
                key={target.id}
                onClick={() => setSelectedTarget(target.id)}
                className={`w-full text-right p-4 rounded-xl border transition-all ${
                  selectedTarget === target.id
                    ? 'border-dealix-emerald bg-dealix-emerald/5'
                    : 'border-gray-100 bg-white hover:border-dealix-gold/30'
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${
                      target.priority === 'high' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'
                    }`}>{target.priority === 'high' ? 'عالي' : 'متوسط'}</span>
                    {logged && (
                      <span className={`text-xs px-2 py-0.5 rounded-full ${
                        logged === 'meeting' ? 'bg-green-100 text-green-700' :
                        logged === 'answered' ? 'bg-blue-100 text-blue-700' :
                        logged === 'called' ? 'bg-gray-100 text-gray-600' :
                        'bg-red-100 text-red-700'
                      }`}>
                        {logged === 'meeting' ? 'اجتماع' : logged === 'answered' ? 'رد' : logged === 'called' ? 'مكالمة' : 'رفض'}
                      </span>
                    )}
                  </div>
                  <Building2 className="w-5 h-5 text-gray-400" />
                </div>
                <h4 className="font-bold text-gray-900 mb-1">{target.company}</h4>
                <p className="text-xs text-gray-500 flex items-center gap-1"><MapPin className="w-3 h-3" /> {target.location} • {target.sector} • {target.size} موظف</p>
              </button>
            );
          })}
        </div>

        {/* Right: Detail Panel */}
        <div className="lg:col-span-2">
          {selected ? (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
              {/* Header */}
              <div className="p-6 border-b border-gray-100">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h2 className="text-xl font-bold text-gray-900">{selected.company}</h2>
                    <p className="text-sm text-gray-500 mt-1">{selected.contact} - {selected.role}</p>
                  </div>
                  <span className="px-3 py-1 bg-dealix-emerald/10 text-dealix-emerald text-sm font-bold rounded-full">{selected.sector}</span>
                </div>
                <div className="flex items-center gap-3 flex-wrap">
                  <a href={`tel:${selected.phone}`} className="flex items-center gap-2 px-4 py-2 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors text-sm font-bold">
                    <Phone className="w-4 h-4" /> اتصال
                  </a>
                  <a href={`mailto:${selected.email}`} className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors text-sm font-bold">
                    <Mail className="w-4 h-4" /> بريد
                  </a>
                  <button className="flex items-center gap-2 px-4 py-2 bg-gray-50 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors text-sm font-bold">
                    <MessageSquare className="w-4 h-4" /> WhatsApp
                  </button>
                </div>
              </div>

              {/* Tabs */}
              <div className="flex border-b border-gray-100">
                {[
                  { key: 'targets', label: 'المعلومات' },
                  { key: 'scripts', label: 'سكريبت المكالمة' },
                  { key: 'emails', label: 'قوالب البريد' },
                ].map((tab) => (
                  <button
                    key={tab.key}
                    onClick={() => setActiveTab(tab.key as any)}
                    className={`flex-1 py-3 text-sm font-bold transition-all ${
                      activeTab === tab.key ? 'text-dealix-emerald border-b-2 border-dealix-emerald' : 'text-gray-500'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Tab Content */}
              <div className="p-6">
                {activeTab === 'targets' && (
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="p-4 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">الهاتف</p><p className="font-medium">{selected.phone}</p></div>
                      <div className="p-4 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">البريد</p><p className="font-medium text-sm">{selected.email}</p></div>
                      <div className="p-4 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">الموقع</p><p className="font-medium">{selected.location}</p></div>
                      <div className="p-4 bg-gray-50 rounded-lg"><p className="text-xs text-gray-500">LinkedIn</p><p className="font-medium text-sm">{selected.linkedIn}</p></div>
                    </div>
                    <div>
                      <p className="text-sm font-bold text-gray-700 mb-3">تسجيل نتيجة المكالمة</p>
                      <div className="grid grid-cols-4 gap-2">
                        {[
                          { key: 'called', label: 'تم الاتصال', color: 'bg-gray-100 text-gray-700' },
                          { key: 'answered', label: 'رد', color: 'bg-blue-100 text-blue-700' },
                          { key: 'meeting', label: 'اجتماع', color: 'bg-green-100 text-green-700' },
                          { key: 'rejected', label: 'رفض', color: 'bg-red-100 text-red-700' },
                        ].map((btn) => (
                          <button
                            key={btn.key}
                            onClick={() => logCall(selected.id, btn.key as any)}
                            className={`py-2 rounded-lg text-xs font-bold transition-all ${btn.color} ${
                              callLog[selected.id] === btn.key ? 'ring-2 ring-offset-2 ring-dealix-gold' : ''
                            }`}
                          >
                            {btn.label}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {activeTab === 'scripts' && (
                  <div className="space-y-4">
                    <p className="text-sm text-gray-500">سكريبتات مكالمة جاهزة لقطاع {selected.sector}</p>
                    {(callScripts[selected.sector as keyof typeof callScripts] || callScripts['عقارات']).map((script, i) => {
                      const personalized = script
                        .replace('[اسمك]', 'المؤسس')
                        .replace('[شركة منافسة]', 'شركة الرياض العقارية');
                      return (
                        <div key={i} className="p-4 bg-gray-50 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-xs font-bold text-dealix-gold">سكريبت {i + 1}</span>
                            <button
                              onClick={() => copyToClipboard(personalized, i)}
                              className="flex items-center gap-1 text-xs text-gray-500 hover:text-dealix-emerald"
                            >
                              {copiedId === i ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                              {copiedId === i ? 'تم النسخ' : 'نسخ'}
                            </button>
                          </div>
                          <p className="text-sm text-gray-700 leading-relaxed">{personalized}</p>
                        </div>
                      );
                    })}
                  </div>
                )}

                {activeTab === 'emails' && (
                  <div className="space-y-4">
                    {emailTemplates.map((template) => {
                      const body = template.body
                        .replace(/\{\{company\}\}/g, selected.company)
                        .replace(/\{\{contact\}\}/g, selected.contact)
                        .replace(/\{\{sector\}\}/g, selected.sector)
                        .replace(/\{\{sender\}\}/g, 'المؤسس - Dealix')
                        .replace(/\{\{phone\}\}/g, '+966 50 000 0000');
                      return (
                        <div key={template.id} className="p-4 bg-gray-50 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <div>
                              <p className="text-sm font-bold text-gray-800">{template.name}</p>
                              <p className="text-xs text-gray-500">{template.subject.replace(/\{\{company\}\}/g, selected.company)}</p>
                            </div>
                            <button
                              onClick={() => copyToClipboard(body, template.id + 100)}
                              className="flex items-center gap-1 text-xs text-gray-500 hover:text-dealix-emerald"
                            >
                              {copiedId === template.id + 100 ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3" />}
                              {copiedId === template.id + 100 ? 'تم النسخ' : 'نسخ'}
                            </button>
                          </div>
                          <pre className="text-xs text-gray-600 whitespace-pre-wrap leading-relaxed">{body}</pre>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-12 text-center">
              <Target className="w-16 h-16 text-gray-200 mx-auto mb-4" />
              <p className="text-gray-400">اختر شركة من القائمة لعرض التفاصيل والسكريبتات</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
