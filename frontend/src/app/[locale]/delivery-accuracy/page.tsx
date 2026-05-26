import React from 'react';

export default function DeliveryAccuracyPage() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-orange-500 selection:text-white" dir="rtl">
      {/* Header */}
      <header className="border-b border-white/10 bg-black/50 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-xl font-bold tracking-tight">Dealix<span className="text-orange-500">.</span></div>
        </div>
      </header>

      {/* Hero */}
      <section className="py-24 px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-orange-900/20 via-black to-black"></div>
        <div className="container mx-auto relative z-10 max-w-4xl text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 tracking-tight text-white">
            Delivery Accuracy Sprint <br/><span className="text-orange-500 text-3xl md:text-5xl">لقطاع اللوجستيات والمتاجر</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-400 mb-10 leading-relaxed max-w-3xl mx-auto">
            ابتداءً من يناير 2026، سترفض هيئة النقل أي شحنة بدون عنوان وطني. استعد الآن بمسار تدقيق ومعالجة لفشل التسليم خلال 7-14 يوم.
          </p>
          <button className="bg-white text-black px-8 py-4 rounded-full font-medium text-lg hover:bg-gray-100 transition-colors">
            اطلب التدقيق الآن
          </button>
        </div>
      </section>

      {/* Content */}
      <section className="py-20 px-6 border-t border-white/10 bg-zinc-950">
        <div className="container mx-auto max-w-4xl space-y-20">
          
          <div className="grid md:grid-cols-2 gap-12 items-start">
            <div>
              <h2 className="text-3xl font-bold mb-4 text-white">المشكلة</h2>
              <p className="text-gray-400 text-lg leading-relaxed">
                الشحنات المرتجعة (RTO) تكلف المتاجر وشركات الشحن مبالغ طائلة. مع قرار هيئة النقل العامة، سيصبح العنوان الوطني شرطاً أساسياً للتوصيل، مما يتطلب تصحيح آلي لبيانات العملاء.
              </p>
            </div>
            <div>
              <h2 className="text-3xl font-bold mb-4 text-white">لمن؟</h2>
              <ul className="space-y-3 text-gray-400 text-lg">
                <li className="flex items-center gap-3"><span className="w-2 h-2 rounded-full bg-orange-500"></span> شركات التوصيل والميل الأخير</li>
                <li className="flex items-center gap-3"><span className="w-2 h-2 rounded-full bg-orange-500"></span> المتاجر الإلكترونية الكبرى</li>
                <li className="flex items-center gap-3"><span className="w-2 h-2 rounded-full bg-orange-500"></span> مزودي خدمات الإيفاء (Fulfillment)</li>
              </ul>
            </div>
          </div>

          <div className="bg-black border border-white/10 rounded-3xl p-10">
            <h2 className="text-3xl font-bold mb-8 text-center text-white">المخرجات (Deliverables)</h2>
            <div className="grid md:grid-cols-2 gap-8">
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-orange-400">التدقيق والتقييم</h3>
                <ul className="space-y-2 text-gray-400">
                  <li>• Address Readiness Audit</li>
                  <li>• Failed Delivery Reason Map</li>
                  <li>• RTO Risk Report</li>
                </ul>
              </div>
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-orange-400">التنفيذ والتصحيح</h3>
                <ul className="space-y-2 text-gray-400">
                  <li>• National Address Collection Flow</li>
                  <li>• Customer Correction Script</li>
                  <li>• Proof Pack</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="text-center space-y-6">
            <h2 className="text-3xl font-bold text-white">السعر يبدأ من 5,000 ريال</h2>
            <p className="text-gray-400 text-lg">يختلف حسب حجم الشحنات وتعقيد الربط.</p>
            <button className="bg-orange-600 text-white px-8 py-4 rounded-full font-medium text-lg hover:bg-orange-500 transition-colors">
              تواصل لبدء التدقيق
            </button>
          </div>

        </div>
      </section>
    </div>
  );
}
