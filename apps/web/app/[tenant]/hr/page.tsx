"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function HRPage() {
  const params = useParams();
  const tenant = params.tenant as string;
  const [employees, setEmployees] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/v1/erp/hr/employees`, { headers: { "x-tenant-id": tenant } })
      .then((r) => r.json())
      .then((d) => { setEmployees(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [tenant]);

  if (loading) return <div className="p-8 text-center">جاري التحميل...</div>;

  return (
    <div className="min-h-screen bg-slate-50 p-8" dir="rtl">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-slate-900">الموارد البشرية</h1>
          <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">
            + موظف جديد
          </button>
        </div>
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="text-right p-4 text-slate-500">الاسم</th>
                <th className="text-right p-4 text-slate-500">القسم</th>
                <th className="text-right p-4 text-slate-500">المنصب</th>
                <th className="text-right p-4 text-slate-500">الحالة</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((e: any) => (
                <tr key={e.id} className="border-t border-slate-100">
                  <td className="p-4 font-medium">{e.full_name}</td>
                  <td className="p-4 text-slate-600">{e.department || "—"}</td>
                  <td className="p-4 text-slate-600">{e.job_title || "—"}</td>
                  <td className="p-4">
                    <span className="text-xs px-2 py-1 rounded bg-emerald-100 text-emerald-700">
                      {e.status}
                    </span>
                  </td>
                </tr>
              ))}
              {employees.length === 0 && (
                <tr><td colSpan={4} className="p-8 text-center text-slate-400">لا يوجد موظفين</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
