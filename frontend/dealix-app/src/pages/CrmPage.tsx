import { useState } from 'react';
import {
  Users, Phone, Mail, MessageSquare, Building2, MapPin,
  Star, TrendingUp, ChevronRight, Plus, Search, Filter,
  Target, Briefcase
} from 'lucide-react';

type PipelineStage = 'lead' | 'contacted' | 'meeting' | 'proposal' | 'negotiation' | 'closed';

interface Customer {
  id: number;
  name: string;
  company: string;
  sector: string;
  stage: PipelineStage;
  value: number;
  lastContact: string;
  nextAction: string;
  email: string;
  phone: string;
  rating: number;
  location: string;
  deals: number;
  avatar: string;
}

const pipelineStages: { key: PipelineStage; label: string; color: string }[] = [
  { key: 'lead', label: 'عميل محتمل', color: 'bg-gray-400' },
  { key: 'contacted', label: 'تم التواصل', color: 'bg-blue-400' },
  { key: 'meeting', label: 'اجتماع', color: 'bg-amber-400' },
  { key: 'proposal', label: 'عرض مقدم', color: 'bg-purple-400' },
  { key: 'negotiation', label: 'تفاوض', color: 'bg-orange-400' },
  { key: 'closed', label: 'مغلقة', color: 'bg-green-500' },
];

const customers: Customer[] = [
  { id: 1, name: 'أحمد الشمري', company: 'شركة الرياض العقارية', sector: 'عقارات', stage: 'proposal', value: 450000, lastContact: 'منذ ساعتين', nextAction: 'متابعة العرض', email: 'ahmed@riyadhat.com', phone: '+966 50 123 4567', rating: 5, location: 'الرياض', deals: 2, avatar: 'أ' },
  { id: 2, name: 'خالد العنزي', company: 'مستشفى الصحة الوطني', sector: 'صحة', stage: 'negotiation', value: 780000, lastContact: 'منذ 4 ساعات', nextAction: 'اجتماع نهائي', email: 'khalid@healthnat.com', phone: '+966 55 234 5678', rating: 4, location: 'جدة', deals: 1, avatar: 'خ' },
  { id: 3, name: 'فهد المطيري', company: 'STC Solutions', sector: 'تقنية', stage: 'meeting', value: 1200000, lastContact: 'أمس', nextAction: 'عرض تقني', email: 'fahad@stcsolutions.com', phone: '+966 54 345 6789', rating: 5, location: 'الرياض', deals: 3, avatar: 'ف' },
  { id: 4, name: 'عبدالله القحطاني', company: 'مصنع الوفاء', sector: 'صناعة', stage: 'contacted', value: 320000, lastContact: 'منذ يومين', nextAction: 'مكالمة متابعة', email: 'abdullah@wafa.com', phone: '+966 56 456 7890', rating: 3, location: 'الدمام', deals: 0, avatar: 'ع' },
  { id: 5, name: 'سعد الحربي', company: 'مجموعة التجارة السعودية', sector: 'تجارة', stage: 'closed', value: 950000, lastContact: 'اليوم', nextAction: 'تجديد العقد', email: 'saad@satrade.com', phone: '+966 57 567 8901', rating: 5, location: 'مكة', deals: 4, avatar: 'س' },
  { id: 6, name: 'محمد الدوسري', company: 'شركة البحر الأحمر', sector: 'عقارات', stage: 'lead', value: 650000, lastContact: 'منذ 3 أيام', nextAction: 'أول مكالمة', email: 'mohamed@redsea.com', phone: '+966 58 678 9012', rating: 4, location: 'جدة', deals: 1, avatar: 'م' },
  { id: 7, name: 'ناصر السبيعي', company: 'مستشفى الملك فهد', sector: 'صحة', stage: 'proposal', value: 890000, lastContact: 'منذ 5 ساعات', nextAction: 'إرسال العرض النهائي', email: 'nasser@kfmc.com', phone: '+966 59 789 0123', rating: 4, location: 'الرياض', deals: 2, avatar: 'ن' },
  { id: 8, name: 'بدر العتيبي', company: 'شركة نيوم التقنية', sector: 'تقنية', stage: 'negotiation', value: 2100000, lastContact: 'منذ ساعة', nextAction: 'توقيع العقد', email: 'bader@neomtech.com', phone: '+966 50 890 1234', rating: 5, location: 'نيوم', deals: 1, avatar: 'ب' },
];

const interactions = [
  { id: 1, customer: 'أحمد الشمري', action: 'مكالمة هاتفية', time: 'منذ ساعتين', note: 'ناقشنا العرض التفصيلي، العميل مهتم بالباقة الذهبية' },
  { id: 2, customer: 'خالد العنزي', action: 'اجتماع', time: 'منذ 4 ساعات', note: 'عرضنا الحلول المخصصة للقطاع الصحي' },
  { id: 3, customer: 'فهد المطيري', action: 'بريد إلكتروني', time: 'أمس', note: 'أرسلت العرض التقني مع التكلفة' },
  { id: 4, customer: 'بدر العتيبي', action: 'مكالمة هاتفية', time: 'منذ ساعة', note: 'العميل وافق على الشروط، في انتظار التوقيع' },
];

export default function CrmPage() {
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterSector, setFilterSector] = useState('all');

  const filteredCustomers = customers.filter(c => {
    const matchesSearch = c.name.includes(searchQuery) || c.company.includes(searchQuery);
    const matchesSector = filterSector === 'all' || c.sector === filterSector;
    return matchesSearch && matchesSector;
  });

  const totalPipeline = customers.reduce((sum, c) => sum + c.value, 0);
  const avgDeal = Math.round(totalPipeline / customers.length);
  const activeDeals = customers.filter(c => c.stage !== 'closed').length;

  return (
    <div className="space-y-6" style={{ direction: 'rtl' }}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">إدارة علاقات العملاء</h1>
          <p className="text-sm text-gray-500 mt-1">نظام CRM متكامل لتتبع العملاء والفرص</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-dealix-emerald text-white rounded-lg hover:bg-dealix-forest text-sm font-bold">
          <Plus className="w-4 h-4" /> عميل جديد
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gradient-to-br from-dealix-emerald to-dealix-forest rounded-xl p-5 text-white">
          <div className="flex items-center gap-2 mb-2">
            <Briefcase className="w-5 h-5 text-dealix-gold" />
            <span className="text-sm text-white/70">قيمة الأنابيب</span>
          </div>
          <p className="text-3xl font-bold">{totalPipeline.toLocaleString()} <span className="text-lg">ريال</span></p>
          <p className="text-xs text-white/60 mt-1">+23% عن الشهر الماضي</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Users className="w-5 h-5 text-blue-500" />
            <span className="text-sm text-gray-500">العملاء النشطون</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{activeDeals}</p>
          <p className="text-xs text-gray-400 mt-1">صفقة في الأنابيب</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <Target className="w-5 h-5 text-dealix-gold" />
            <span className="text-sm text-gray-500">متوسط الصفقة</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">{avgDeal.toLocaleString()}</p>
          <p className="text-xs text-gray-400 mt-1">ريال للصفقة الواحدة</p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-green-500" />
            <span className="text-sm text-gray-500">معدل الإغلاق</span>
          </div>
          <p className="text-3xl font-bold text-gray-900">68%</p>
          <p className="text-xs text-green-600 mt-1">+12% عن الربع السابق</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Pipeline & Customers List */}
        <div className="lg:col-span-2 space-y-6">
          {/* Search & Filter */}
          <div className="flex items-center gap-3">
            <div className="flex-1 relative">
              <Search className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="ابحث باسم العميل أو الشركة..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pr-10 pl-4 py-2.5 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-dealix-emerald"
              />
            </div>
            <select
              value={filterSector}
              onChange={(e) => setFilterSector(e.target.value)}
              className="border border-gray-200 rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:border-dealix-emerald"
            >
              <option value="all">كل القطاعات</option>
              <option value="عقارات">عقارات</option>
              <option value="صحة">صحة</option>
              <option value="تقنية">تقنية</option>
              <option value="تجارة">تجارة</option>
              <option value="صناعة">صناعة</option>
            </select>
            <button className="p-2.5 border border-gray-200 rounded-lg hover:bg-gray-50">
              <Filter className="w-4 h-4 text-gray-500" />
            </button>
          </div>

          {/* Pipeline Visual */}
          <div className="bg-white rounded-xl p-5 shadow-card border border-gray-100">
            <h3 className="font-bold text-gray-900 mb-4">خط الأنابيب</h3>
            <div className="flex gap-1">
              {pipelineStages.map((stage) => {
                const count = customers.filter(c => c.stage === stage.key).length;
                const value = customers.filter(c => c.stage === stage.key).reduce((s, c) => s + c.value, 0);
                return (
                  <div
                    key={stage.key}
                    className="flex-1 rounded-lg p-3 text-center cursor-pointer hover:opacity-80 transition-opacity"
                    onClick={() => setFilterSector('all')}
                  >
                    <div className={`w-full h-2 rounded-full ${stage.color} mb-2`} />
                    <p className="text-2xl font-bold text-gray-900">{count}</p>
                    <p className="text-xs text-gray-500 mt-1">{stage.label}</p>
                    <p className="text-[10px] text-gray-400">{(value / 1000).toFixed(0)}K</p>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Customers Table */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
            <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
              <h3 className="font-bold text-gray-900">قائمة العملاء</h3>
              <span className="text-xs text-gray-400">{filteredCustomers.length} عميل</span>
            </div>
            <div className="divide-y divide-gray-50">
              {filteredCustomers.map((customer) => (
                <div
                  key={customer.id}
                  className="px-5 py-4 flex items-center gap-4 hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => setSelectedCustomer(customer)}
                >
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-dealix-emerald to-dealix-forest flex items-center justify-center text-white font-bold text-sm shrink-0">
                    {customer.avatar}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="font-bold text-gray-900 text-sm">{customer.name}</p>
                      <div className="flex">
                        {Array.from({ length: customer.rating }).map((_, i) => (
                          <Star key={i} className="w-3 h-3 text-dealix-gold fill-dealix-gold" />
                        ))}
                      </div>
                    </div>
                    <p className="text-xs text-gray-500">{customer.company}</p>
                  </div>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-gray-100 text-gray-600">
                    {customer.sector}
                  </span>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                    customer.stage === 'closed' ? 'bg-green-100 text-green-700' :
                    customer.stage === 'negotiation' ? 'bg-orange-100 text-orange-700' :
                    customer.stage === 'proposal' ? 'bg-purple-100 text-purple-700' :
                    'bg-blue-100 text-blue-700'
                  }`}>
                    {pipelineStages.find(s => s.key === customer.stage)?.label}
                  </span>
                  <p className="text-sm font-bold text-gray-900 w-28 text-left">{customer.value.toLocaleString()} ر.س</p>
                  <ChevronRight className="w-4 h-4 text-gray-300" />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Panel: Customer Detail + Interactions */}
        <div className="space-y-6">
          {selectedCustomer ? (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-5">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-dealix-emerald to-dealix-forest flex items-center justify-center text-white font-bold text-xl">
                  {selectedCustomer.avatar}
                </div>
                <div>
                  <h3 className="font-bold text-gray-900">{selectedCustomer.name}</h3>
                  <p className="text-sm text-gray-500">{selectedCustomer.company}</p>
                </div>
              </div>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm">
                  <Mail className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-600">{selectedCustomer.email}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Phone className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-600">{selectedCustomer.phone}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <MapPin className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-600">{selectedCustomer.location}</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <Building2 className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-600">{selectedCustomer.sector}</span>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-gray-100">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-500">قيمة الصفقة</span>
                  <span className="font-bold text-gray-900">{selectedCustomer.value.toLocaleString()} ر.س</span>
                </div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-500">الصفقات السابقة</span>
                  <span className="font-bold text-gray-900">{selectedCustomer.deals}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-500">آخر تواصل</span>
                  <span className="font-bold text-gray-900">{selectedCustomer.lastContact}</span>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-gray-100">
                <p className="text-xs text-gray-500 mb-1">الخطوة التالية</p>
                <p className="text-sm font-bold text-dealix-emerald">{selectedCustomer.nextAction}</p>
              </div>
              <div className="flex gap-2 mt-4">
                <button className="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-dealix-emerald text-white rounded-lg text-sm font-bold">
                  <Phone className="w-4 h-4" /> اتصال
                </button>
                <button className="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-bold hover:bg-gray-200">
                  <Mail className="w-4 h-4" /> بريد
                </button>
                <button className="flex-1 flex items-center justify-center gap-1 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-bold hover:bg-gray-200">
                  <MessageSquare className="w-4 h-4" /> واتساب
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow-card border border-gray-100 p-8 text-center">
              <Users className="w-12 h-12 text-gray-200 mx-auto mb-3" />
              <p className="text-gray-400 text-sm">اختر عميلاً لعرض التفاصيل</p>
            </div>
          )}

          {/* Recent Interactions */}
          <div className="bg-white rounded-xl shadow-card border border-gray-100 p-5">
            <h3 className="font-bold text-gray-900 mb-4">آخر التفاعلات</h3>
            <div className="space-y-4">
              {interactions.map((interaction) => (
                <div key={interaction.id} className="flex gap-3">
                  <div className="w-8 h-8 rounded-full bg-dealix-emerald/10 flex items-center justify-center shrink-0 mt-0.5">
                    {interaction.action === 'مكالمة هاتفية' ? <Phone className="w-4 h-4 text-dealix-emerald" /> :
                     interaction.action === 'اجتماع' ? <Users className="w-4 h-4 text-dealix-emerald" /> :
                     <Mail className="w-4 h-4 text-dealix-emerald" />}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <p className="text-sm font-bold text-gray-900">{interaction.customer}</p>
                      <span className="text-[10px] text-gray-400">{interaction.time}</span>
                    </div>
                    <p className="text-xs text-dealix-emerald font-medium">{interaction.action}</p>
                    <p className="text-xs text-gray-500 mt-1">{interaction.note}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
