"use client";

import {
  Bar,
  BarChart,
  Cell,
  LabelList,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import type { BarItem, RoiCol } from "./types";

const GOLD = "#C9A96E";
const EMERALD = "#10b981";
const MUTED = "#94a3b8";
const DANGER = "#ef4444";

interface BeforeAfterChartProps {
  items: BarItem[];
  lang: "ar" | "en";
}

export function BeforeAfterChart({ items, lang }: BeforeAfterChartProps) {
  const beforeLabel = lang === "ar" ? "قبل" : "Before";
  const afterLabel = lang === "ar" ? "بعد" : "After";
  const data = items.map((it) => ({
    name: it.label,
    before: Math.max(2, it.beforePct),
    after: Math.max(2, it.afterPct),
    beforeText: it.before,
    afterText: it.after,
  }));
  const height = data.length * 96 + 24;

  return (
    <div dir="ltr" className="w-full rounded-2xl border border-border bg-card/60 p-4">
      <div className="mb-2 flex items-center gap-5 px-2">
        <span className="flex items-center gap-2 text-xs font-semibold text-muted-foreground">
          <span className="h-3 w-3 rounded-sm" style={{ background: MUTED }} />
          {beforeLabel}
        </span>
        <span className="flex items-center gap-2 text-xs font-semibold text-muted-foreground">
          <span className="h-3 w-3 rounded-sm" style={{ background: EMERALD }} />
          {afterLabel}
        </span>
      </div>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart
          layout="vertical"
          data={data}
          margin={{ top: 8, right: 88, bottom: 8, left: 8 }}
          barGap={4}
        >
          <XAxis type="number" domain={[0, 118]} hide />
          <YAxis
            type="category"
            dataKey="name"
            width={150}
            tickLine={false}
            axisLine={false}
            tick={{ fill: "currentColor", fontSize: 12 }}
            className="text-foreground"
          />
          <Bar dataKey="before" fill={MUTED} radius={[0, 6, 6, 0]} barSize={20}>
            <LabelList
              dataKey="beforeText"
              position="right"
              className="fill-muted-foreground"
              style={{ fontSize: 12, fontWeight: 700 }}
            />
          </Bar>
          <Bar dataKey="after" fill={EMERALD} radius={[0, 6, 6, 0]} barSize={20}>
            <LabelList
              dataKey="afterText"
              position="right"
              className="fill-foreground"
              style={{ fontSize: 12, fontWeight: 800 }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface RoiChartProps {
  cols: RoiCol[];
  unit: string;
}

export function RoiChart({ cols, unit }: RoiChartProps) {
  const data = cols.map((c) => ({
    name: c.label,
    value: Math.max(3, c.pct),
    text: c.value,
    tone: c.tone,
  }));

  return (
    <div dir="ltr" className="w-full rounded-2xl border border-border bg-card/60 p-4">
      <p className="mb-1 px-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        {unit}
      </p>
      <ResponsiveContainer width="100%" height={data.length * 86 + 24}>
        <BarChart
          layout="vertical"
          data={data}
          margin={{ top: 8, right: 96, bottom: 8, left: 8 }}
        >
          <XAxis type="number" domain={[0, 116]} hide />
          <YAxis
            type="category"
            dataKey="name"
            width={170}
            tickLine={false}
            axisLine={false}
            tick={{ fill: "currentColor", fontSize: 12 }}
            className="text-foreground"
          />
          <Bar dataKey="value" radius={[0, 8, 8, 0]} barSize={34}>
            {data.map((d, i) => (
              <Cell key={i} fill={d.tone === "danger" ? DANGER : EMERALD} />
            ))}
            <LabelList
              dataKey="text"
              position="right"
              className="fill-foreground"
              style={{ fontSize: 15, fontWeight: 800 }}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export const PITCH_CHART_COLORS = { GOLD, EMERALD, MUTED, DANGER };
