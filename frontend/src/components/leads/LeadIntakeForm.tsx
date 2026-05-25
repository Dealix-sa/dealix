"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { api } from "@/lib/api";
import { toast } from "sonner";

export function LeadIntakeForm() {
  const t = useTranslations("leadIntake");
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const fd = new FormData(e.currentTarget);
    setLoading(true);
    try {
      await api.submitLead({
        company: String(fd.get("company") || ""),
        name: String(fd.get("name") || ""),
        email: String(fd.get("email") || ""),
        phone: String(fd.get("phone") || ""),
        sector: String(fd.get("sector") || "technology"),
        region: "Saudi Arabia",
        budget: 50000,
        message: String(fd.get("message") || ""),
      });
      toast.success(t("success"));
      e.currentTarget.reset();
    } catch {
      toast.error(t("error"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="mt-8 space-y-4 max-w-md">
      <h2 className="text-lg font-semibold">{t("title")}</h2>
      <div className="space-y-1.5">
        <Label htmlFor="company">{t("company")}</Label>
        <Input id="company" name="company" required />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="name">{t("name")}</Label>
        <Input id="name" name="name" required />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="email">{t("email")}</Label>
        <Input id="email" name="email" type="email" required dir="ltr" />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="phone">{t("phone")}</Label>
        <Input id="phone" name="phone" required dir="ltr" />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="sector">{t("sector")}</Label>
        <Input id="sector" name="sector" defaultValue="technology" />
      </div>
      <div className="space-y-1.5">
        <Label htmlFor="message">{t("message")}</Label>
        <Input id="message" name="message" />
      </div>
      <Button type="submit" disabled={loading}>
        {t("submit")}
      </Button>
    </form>
  );
}
