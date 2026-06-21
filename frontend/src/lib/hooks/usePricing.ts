"use client";

import { useEffect, useState } from "react";

export interface PlanFeature {
  text: string;
  textAr: string;
  included: boolean;
}

export interface PlanData {
  id: string;
  name: string;
  nameAr: string;
  description: string;
  descriptionAr: string;
  monthlyPrice: number;
  yearlyPrice: number;
  features: PlanFeature[];
  highlighted: boolean;
  cta: string;
  ctaAr: string;
}

/**
 * Subscription plans. Returns an empty list until the pricing API endpoint is
 * wired; the UI renders its empty state in the meantime.
 */
export function usePlans() {
  const [data, setData] = useState<PlanData[] | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setData([]);
    setIsLoading(false);
  }, []);

  return { data, isLoading };
}
