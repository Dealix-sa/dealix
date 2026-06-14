import { useState } from 'react';
import {
  User, Bell, Shield, CreditCard, Globe, Palette,
  Save, CheckCircle2
} from 'lucide-react';
import { Switch } from '@/components/ui/switch';

const settingsSections = [
  { id: 'profile', label: 'الملف الشخصي', icon: User },
  { id: 'notifications', label: 'الإشعارات', icon: Bell },
  { id: 'security', label: 'الأمان', icon: Shield },
  { id: 'billing', label: 'الفوترة', icon: CreditCard },
  { id: 'language', label: 'اللغة والمنطقة', icon: Globe },
  { id: 'appearance', label: 'المظهر', icon: Palette },
];

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('profile');
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      <div>
        <h1 className="text-2xl font-bold text-gray-900">الإعدادات</h1>
        <p className="text-sm text-gray-500 mt-1">إدارة حسابك وتفضيلات النظام</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
            {settingsSections.map((section) => {
              const Icon = section.icon;
              return (
                <button
                  key={section.id}
                  onClick={() => setActiveSection(section.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3.5 text-right transition-all ${
                    activeSection === section.id
                      ? 'bg-dealix-emerald/10 text-dealix-emerald border-r-2 border-dealix-emerald'
                      : 'text-gray-600 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="text-sm font-medium">{section.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Content */}
        <div className="lg:col-span-3 space-y-6">
          {/* Profile */}
          {activeSection === 'profile' && (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-6">الملف الشخصي</h3>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">الاسم</label>
                    <input type="text" defaultValue="المؤسس" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-dealix-emerald/30 outline-none" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">البريد الإلكتروني</label>
                    <input type="email" defaultValue="founder@dealix.me" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-dealix-emerald/30 outline-none" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">المنصب</label>
                  <input type="text" defaultValue="CEO & Founder" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-dealix-emerald/30 outline-none" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">نبذة</label>
                  <textarea rows={3} defaultValue="مؤسس Dealix - نظام تشغيل الإيرادات بالذكاء الاصطناعي" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-dealix-emerald/30 outline-none resize-none" />
                </div>
              </div>
            </div>
          )}

          {/* Notifications */}
          {activeSection === 'notifications' && (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-6">الإشعارات</h3>
              <div className="space-y-4">
                {[
                  { label: 'إشعارات الصفقات الجديدة', desc: 'إشعار عند تسجيل صفقة جديدة', checked: true },
                  { label: 'تنبيهات النظام', desc: 'تنبيهات الأداء والأخطاء', checked: true },
                  { label: 'تقارير يومية', desc: 'تلخيص يومي عبر البريد', checked: false },
                  { label: 'إشعارات التسويق', desc: 'أداء الحملات والعملاء المحتملين', checked: true },
                  { label: 'تنبيهات الأمان', desc: 'محاولات دخول مشبوهة', checked: true },
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between py-3 border-b border-gray-50 last:border-0">
                    <div>
                      <p className="font-medium text-gray-800">{item.label}</p>
                      <p className="text-xs text-gray-500">{item.desc}</p>
                    </div>
                    <Switch defaultChecked={item.checked} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Security */}
          {activeSection === 'security' && (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-6">الأمان</h3>
              <div className="space-y-4">
                <div className="p-4 bg-green-50 border border-green-100 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle2 className="w-5 h-5 text-green-600" />
                    <span className="font-bold text-green-800">التحقق بخطوتين مفعل</span>
                  </div>
                  <p className="text-sm text-green-700">يتم إرسال رمز التحقق إلى هاتفك عند كل تسجيل دخول</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">كلمة المرور الحالية</label>
                    <input type="password" placeholder="••••••••" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">كلمة المرور الجديدة</label>
                    <input type="password" placeholder="••••••••" className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" />
                  </div>
                </div>
                <div className="p-4 bg-gray-50 rounded-lg">
                  <p className="text-sm font-medium text-gray-700">آخر تسجيل دخول</p>
                  <p className="text-xs text-gray-500 mt-1">14 يونيو 2025 - الرياض، السعودية - Chrome on MacOS</p>
                </div>
              </div>
            </div>
          )}

          {/* Billing */}
          {activeSection === 'billing' && (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-6">الفوترة</h3>
              <div className="p-4 bg-gradient-to-r from-dealix-emerald/10 to-dealix-gold/10 rounded-lg mb-4">
                <p className="text-sm text-gray-600">الخطة الحالية</p>
                <p className="text-2xl font-bold text-dealix-emerald">غرفة القيادة</p>
                <p className="text-sm text-gray-500">4,900 ريال / شهر • تجديد: 1 يوليو 2025</p>
              </div>
              <div className="space-y-3">
                {[
                  { item: 'اشتراك يونيو 2025', amount: '4,900', status: 'مدفوع' },
                  { item: 'اشتراك مايو 2025', amount: '4,900', status: 'مدفوع' },
                  { item: 'اشتراك أبريل 2025', amount: '4,900', status: 'مدفوع' },
                ].map((bill, i) => (
                  <div key={i} className="flex items-center justify-between py-3 border-b border-gray-50">
                    <span className="text-sm text-gray-700">{bill.item}</span>
                    <div className="flex items-center gap-4">
                      <span className="font-bold text-gray-900">{bill.amount} ريال</span>
                      <span className="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full">{bill.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Language */}
          {activeSection === 'language' && (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-6">اللغة والمنطقة</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">اللغة</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" defaultValue="ar">
                    <option value="ar">العربية</option>
                    <option value="en">English</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">المنطقة الزمنية</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" defaultValue="riyadh">
                    <option value="riyadh">الرياض (GMT+3)</option>
                    <option value="dubai">دبي (GMT+4)</option>
                    <option value="london">لندن (GMT+1)</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">العملة</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm" defaultValue="sar">
                    <option value="sar">ريال سعودي (SAR)</option>
                    <option value="usd">دولار أمريكي (USD)</option>
                    <option value="aed">درهم إماراتي (AED)</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Appearance */}
          {activeSection === 'appearance' && (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-6">
              <h3 className="font-bold text-gray-900 mb-6">المظهر</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between py-3">
                  <div>
                    <p className="font-medium text-gray-800">الوضع الداكن</p>
                    <p className="text-xs text-gray-500">تفعيل المظهر الداكن للوحة التحكم</p>
                  </div>
                  <Switch />
                </div>
                <div className="flex items-center justify-between py-3">
                  <div>
                    <p className="font-medium text-gray-800">شريط جانبي مدمج</p>
                    <p className="text-xs text-gray-500">تقليص الشريط الجانبي بشكل افتراضي</p>
                  </div>
                  <Switch defaultChecked={false} />
                </div>
                <div className="flex items-center justify-between py-3">
                  <div>
                    <p className="font-medium text-gray-800">الرسوم المتحركة</p>
                    <p className="text-xs text-gray-500">تفعيل الحركات والانتقالات</p>
                  </div>
                  <Switch defaultChecked={true} />
                </div>
              </div>
            </div>
          )}

          {/* Save Button */}
          <div className="flex items-center justify-end gap-3">
            {saved && (
              <span className="flex items-center gap-1 text-sm text-green-600">
                <CheckCircle2 className="w-4 h-4" /> تم الحفظ بنجاح
              </span>
            )}
            <button onClick={handleSave} className="flex items-center gap-2 px-6 py-2.5 bg-dealix-emerald text-white rounded-lg hover:bg-dealix-forest transition-colors font-bold">
              <Save className="w-4 h-4" />
              حفظ التغييرات
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
