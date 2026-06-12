"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function ProjectsPage() {
  const params = useParams();
  const tenant = params.tenant as string;
  const [projects, setProjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/v1/erp/projects`, { headers: { "x-tenant-id": tenant } })
      .then((r) => r.json())
      .then((d) => { setProjects(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [tenant]);

  if (loading) return <div className="p-8 text-center">جاري التحميل...</div>;

  return (
    <div className="min-h-screen bg-slate-50 p-8" dir="rtl">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-slate-900">المشاريع</h1>
          <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700">
            + مشروع جديد
          </button>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((p: any) => (
            <div key={p.id} className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-bold text-slate-900">{p.name}</h3>
                <span className={`text-xs px-2 py-1 rounded ${
                  p.status === "active" ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-600"
                }`}>
                  {p.status}
                </span>
              </div>
              <p className="text-sm text-slate-500 mb-3">الأولوية: {p.priority}</p>
              <a href={`/${tenant}/projects/${p.id}`} className="text-emerald-600 text-sm hover:underline">
                عرض المهام →
              </a>
            </div>
          ))}
          {projects.length === 0 && (
            <div className="col-span-full text-center text-slate-400 py-12">
              لا توجد مشاريع بعد
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
