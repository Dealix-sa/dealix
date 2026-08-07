"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function InventoryPage() {
  const params = useParams();
  const tenant = params.tenant as string;
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Would fetch from /api/v1/erp/inventory/items
    setLoading(false);
  }, [tenant]);

  return (
    <div className="min-h-screen bg-slate-50 p-8" dir="rtl">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-slate-900">المخزون والمشتريات</h1>
          <div className="flex gap-3">
            <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">
              + منتج جديد
            </button>
            <button className="bg-slate-200 text-slate-700 px-4 py-2 rounded-lg hover:bg-slate-300">
              + أمر شراء
            </button>
          </div>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-6">
          <p className="text-slate-400 text-center py-12">
            {loading ? "جاري التحميل..." : "قريباً — إدارة المخزون والموردين وأوامر الشراء"}
          </p>
        </div>
      </div>
    </div>
  );
}
