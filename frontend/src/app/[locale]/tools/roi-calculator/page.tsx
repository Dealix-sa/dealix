'use client';
import { useState } from 'react';
export default function ROICalculator(){
  const [leads,setLeads]=useState(100); const [value,setValue]=useState(1500); const [lift,setLift]=useState(10);
  const recovered=Math.round(leads*value*(lift/100));
  return <main dir="rtl" className="min-h-screen bg-[#070b12] text-white px-6 py-16"><section className="mx-auto max-w-3xl space-y-6">
    <p className="text-cyan-300">Dealix Tool</p><h1 className="text-4xl font-bold">حاسبة فرص الإيراد الضائعة</h1>
    <p className="text-slate-300">تقدير تقريبي وليس ضمانًا للنتائج.</p>
    <input className="w-full rounded-xl p-3 text-black" type="number" value={leads} onChange={e=>setLeads(Number(e.target.value))}/>
    <input className="w-full rounded-xl p-3 text-black" type="number" value={value} onChange={e=>setValue(Number(e.target.value))}/>
    <input className="w-full rounded-xl p-3 text-black" type="number" value={lift} onChange={e=>setLift(Number(e.target.value))}/>
    <div className="rounded-3xl border border-white/10 bg-white/5 p-6"><p>قيمة تقديرية</p><p className="text-4xl font-bold text-cyan-300">{recovered.toLocaleString()} ريال / شهر</p></div>
  </section></main>
}
