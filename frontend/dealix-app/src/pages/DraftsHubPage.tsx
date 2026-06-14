import { useState } from 'react';
import {
  FileText, Copy, Check, Download, Mail, MessageSquare,
  FileCheck, FileSpreadsheet
} from 'lucide-react';

type DraftCategory = 'proposals' | 'contracts' | 'emails' | 'whatsapp' | 'reports';

interface DraftTemplate {
  id: number;
  name: string;
  category: DraftCategory;
  description: string;
  content: string;
  variables: string[];
}

const draftTemplates: DraftTemplate[] = [
  {
    id: 1,
    name: 'عرض تجاري - بايلوت',
    category: 'proposals',
    description: 'عرض بايلوت 7 أيام مع ضمان',
    variables: ['{{company}}', '{{contact}}', '{{sector}}', '{{price}}'],
    content: `عــــــرض تجــــــاري
══════════════════════════════════

إلى: {{company}}
الموضوع: عرض بايلوت Dealix - نظام إدارة الإيرادات بالذكاء الاصطناعي

الأخ {{contact}}،

يسعدنا أن نقدم لكم عرض البايلوت الحصري:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
المميزات المتضمنة:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ تشخيص شامل لأعمال {{company}} (30 نقطة)
✓ 7 أيام تجربة كاملة للمنصة
✓ مدير حساب مخصص
✓ تقرير أسبوعي مفصل
✓ تحليلات الذكاء الاصطناعي
✓ دعم فني مباشر

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
الاستثمار: {{price}} ريال
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ضمان استرداد 100% خلال 14 يوم

نتطلع للتعاون معكم.

Dealix
نظام تشغيل الإيرادات بالذكاء الاصطناعي
hello@dealix.me | dealix.me`
  },
  {
    id: 2,
    name: 'عرض تجاري - مؤسسي',
    category: 'proposals',
    description: 'عرض الاشتراك المؤسسي الشهري',
    variables: ['{{company}}', '{{contact}}', '{{users}}'],
    content: `عــــــرض اشتراك مؤسسي
══════════════════════════════════

إلى: {{company}}

الأخ {{contact}}،

نقدم لكم خطة "غرفة القيادة" المؤسسية:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
المميزات:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ منصة Dealix كاملة
✓ {{users}} مستخدم
✓ API كامل مع 172 نقطة
✓ تحليلات متقدمة في الوقت الفعلي
✓ تقارير مخصصة
✓ دعم شهري مستمر
✓ تحديثات مجانية
✓ امتثال PDPL وZATCA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
الاستثمار: 4,900 - 9,900 ريال/شهر
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ خصم 10% للسداد السنوي
✓ SLA: 99.5% uptime

للتفعيل: hello@dealix.me`
  },
  {
    id: 3,
    name: 'عقد خدمات - Dealix',
    category: 'contracts',
    description: 'عقد خدمات قياسي (قابل للتخصيص)',
    variables: ['{{company}}', '{{date}}', '{{price}}', '{{duration}}'],
    content: `عقد تقديم خدمات Dealix
══════════════════════════════════

الطرف الأول: Dealix لتقنية المعلومات
الطرف الثاني: {{company}}

تاريخ: {{date}}

المادة 1: الغرض
تقديم Dealix خدمات نظام إدارة الإيرادات بالذكاء الاصطناعي.

المادة 2: المدة
{{duration}} شهر، قابل للتجديد تلقائياً.

المادة 3: الاستثمار
{{price}} ريال/شهر، يُدفع مقدماً.

المادة 4: الامتثال
• حماية البيانات ح PDPL
• فوترة إلكترونية ZATCA
• تشفير البيانات end-to-end

المادة 5: الضمان
• ضمان استرداد 14 يوم
• SLA 99.5% uptime
• دعم فني خلال ساعات العمل

التوقيع: _______________     التوقيع: _______________
Dealix                              {{company}}`
  },
  {
    id: 4,
    name: 'بريد متابعة - بعد البايلوت',
    category: 'emails',
    description: 'بريد متابعة بعد انتهاء البايلوت',
    variables: ['{{company}}', '{{contact}}', '{{results}}'],
    content: `الموضوع: نتائج البايلوت - {{company}} + Dealix

الأخ {{contact}}،

شكراً لمنحنا الفرصة لخدمتكم خلال الأسبوع الماضي.

نتائج البايلوت:
{{results}}

هل ترغب في الانتقال للاشتراك الكامل؟
نقدم خصم 20% للعملاء الذين ينتقلون خلال 48 ساعة.

مع خالص التقدير،
Dealix Team`
  },
  {
    id: 5,
    name: 'WhatsApp - تعريفي',
    category: 'whatsapp',
    description: 'رسالة WhatsApp أولى',
    variables: ['{{contact}}', '{{company}}'],
    content: `السلام عليكم أخ {{contact}} 👋

أنا من Dealix - أول منصة سعودية 🇸🇦 لإدارة الإيرادات بالذكاء الاصطناعي.

نساعد شركات {{company}} على:
📈 زيادة المبيعات 35%
⏱️ تقليل وقت المتابعة 60%
🔒 الامتثال لـ PDPL

هل يمكننا 15 دقيقة هذا الأسبوع؟ 😊

شكراً،
Dealix`
  },
  {
    id: 6,
    name: 'WhatsApp - متابعة',
    category: 'whatsapp',
    description: 'رسالة متابعة بعد يومين',
    variables: ['{{contact}}'],
    content: `السلام عليكم أخ {{contact}} 🙏

أردت المتابعة على رسالتي السابقة.

لقد ساعدنا شركات مشابهة على تحقيق نتائج رائعة 💪

هل تفضل مكالمة سريعة 10 دقائق؟
أو يمكنني أرسل لك تقرير تشخيص مجاني أولاً 📋

شكراً لوقتك 🌟`
  },
  {
    id: 7,
    name: 'تقرير يومي - المؤسس',
    category: 'reports',
    description: 'تقرير ملخص يومي تلقائي',
    variables: ['{{date}}', '{{revenue}}', '{{deals}}', '{{calls}}', '{{new_leads}}'],
    content: `📊 تقرير يومي Dealix - {{date}}
══════════════════════════════════

📈 المبيعات:
   إيرادات اليوم: {{revenue}} ريال
   الصفقات المغلقة: {{deals}}

📞 المكالمات:
   مكالمات: {{calls}}
   عملاء جدد: {{new_leads}}

🎯 الاستهداف اليومي:
   □ مكالمة 1 - شركة العقارات الكبرى
   □ مكالمة 2 - المستشفى الوطني
   □ إرسال عرض تجاري - STC Solutions

⚡ تنبيهات:
   • 3 طلبات موافقة معلقة
   • معدل uptime: 99.7%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dealix Founder OS - dealix.me`
  },
  {
    id: 8,
    name: 'تقرير أسبوعي - المؤسس',
    category: 'reports',
    description: 'تقرير أسبوعي شامل',
    variables: ['{{week}}', '{{total_revenue}}', '{{new_customers}}', '{{pipeline}}'],
    content: `📊 التقرير الأسبوعي - الأسبوع {{week}}
══════════════════════════════════

💰 الإيرادات: {{total_revenue}} ريال
👥 عملاء جدد: {{new_customers}}
🎯 خط الأنابيب: {{pipeline}} ريال

📈 أداء القطاعات:
   العقارات: ████████░░ 80%
   الصحة:    ██████░░░░ 60%
   التجارة:  ███████░░░ 70%
   التقنية:  ██████░░░░ 55%

🏆 أبرز الإنجازات:
   • إغلاق صفقة شركة العقارات الكبرى
   • بايلوت جديد مع المستشفى الوطني

📋 أهداف الأسبوع القادم:
   • 10 مكالمات جديدة
   • 3 اجتماعات face-to-face
   • إطلاق حملة LinkedIn

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dealix Founder OS`
  },
];

const categories: { key: DraftCategory; label: string; icon: typeof FileText }[] = [
  { key: 'proposals', label: 'العروض التجارية', icon: FileText },
  { key: 'contracts', label: 'العقود', icon: FileCheck },
  { key: 'emails', label: 'الرسائل البريدية', icon: Mail },
  { key: 'whatsapp', label: 'WhatsApp', icon: MessageSquare },
  { key: 'reports', label: 'التقارير', icon: FileSpreadsheet },
];

export default function DraftsHubPage() {
  const [activeCategory, setActiveCategory] = useState<DraftCategory>('proposals');
  const [selectedDraft, setSelectedDraft] = useState<DraftTemplate | null>(null);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const copyToClipboard = (text: string, id: number) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    });
  };

  const downloadText = (filename: string, text: string) => {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const filteredDrafts = draftTemplates.filter(d => d.category === activeCategory);

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">مركز المسودات</h1>
          <p className="text-sm text-gray-500 mt-1">قوالب جاهزة - انسخ وعدل وأرسل</p>
        </div>
        <span className="px-3 py-1.5 bg-dealix-gold/10 text-dealix-gold text-sm font-bold rounded-full">
          {draftTemplates.length} قالب جاهز
        </span>
      </div>

      {/* Category Tabs */}
      <div className="grid grid-cols-5 gap-2">
        {categories.map((cat) => {
          const Icon = cat.icon;
          const count = draftTemplates.filter(d => d.category === cat.key).length;
          return (
            <button
              key={cat.key}
              onClick={() => { setActiveCategory(cat.key); setSelectedDraft(null); }}
              className={`flex items-center justify-center gap-2 py-3 rounded-xl text-sm font-bold transition-all ${
                activeCategory === cat.key
                  ? 'bg-dealix-emerald text-white shadow-glow-emerald'
                  : 'bg-white text-gray-600 border border-gray-200 hover:border-dealix-gold/30'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span className="hidden sm:inline">{cat.label}</span>
              <span className={`text-xs px-1.5 py-0.5 rounded-full ${
                activeCategory === cat.key ? 'bg-white/20' : 'bg-gray-100'
              }`}>{count}</span>
            </button>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Drafts List */}
        <div className="lg:col-span-1 space-y-2">
          {filteredDrafts.map((draft) => (
            <button
              key={draft.id}
              onClick={() => setSelectedDraft(draft)}
              className={`w-full text-right p-4 rounded-xl border transition-all ${
                selectedDraft?.id === draft.id
                  ? 'border-dealix-emerald bg-dealix-emerald/5'
                  : 'border-gray-100 bg-white hover:border-dealix-gold/30'
              }`}
            >
              <h4 className="font-bold text-gray-900 text-sm">{draft.name}</h4>
              <p className="text-xs text-gray-500 mt-1">{draft.description}</p>
              <div className="flex gap-1 mt-2 flex-wrap">
                {draft.variables.slice(0, 3).map((v, i) => (
                  <span key={i} className="text-[10px] px-1.5 py-0.5 bg-gray-100 rounded text-gray-500">{v}</span>
                ))}
              </div>
            </button>
          ))}
        </div>

        {/* Preview */}
        <div className="lg:col-span-2">
          {selectedDraft ? (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
              <div className="flex items-center justify-between p-4 border-b border-gray-100 bg-gray-50">
                <div>
                  <h3 className="font-bold text-gray-900">{selectedDraft.name}</h3>
                  <p className="text-xs text-gray-500">{selectedDraft.description}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => copyToClipboard(selectedDraft.content, selectedDraft.id)}
                    className="flex items-center gap-1 px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-sm hover:bg-gray-50"
                  >
                    {copiedId === selectedDraft.id ? <Check className="w-3.5 h-3.5 text-green-500" /> : <Copy className="w-3.5 h-3.5" />}
                    {copiedId === selectedDraft.id ? 'تم' : 'نسخ'}
                  </button>
                  <button
                    onClick={() => downloadText(`${selectedDraft.name}.txt`, selectedDraft.content)}
                    className="flex items-center gap-1 px-3 py-1.5 bg-dealix-emerald text-white rounded-lg text-sm hover:bg-dealix-forest"
                  >
                    <Download className="w-3.5 h-3.5" /> تصدير
                  </button>
                </div>
              </div>
              <div className="p-6">
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 font-mono text-sm leading-relaxed whitespace-pre-wrap">
                  {selectedDraft.content}
                </div>
                <div className="mt-4">
                  <p className="text-xs text-gray-500 mb-2">المتغيرات:</p>
                  <div className="flex gap-2 flex-wrap">
                    {selectedDraft.variables.map((v, i) => (
                      <span key={i} className="text-xs px-2 py-1 bg-dealix-gold/10 text-dealix-gold rounded font-bold">{v}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-12 text-center">
              <FileText className="w-16 h-16 text-gray-200 mx-auto mb-4" />
              <p className="text-gray-400">اختر قالباً لعرض المعاينة والتصدير</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
