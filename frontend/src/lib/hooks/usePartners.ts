"use client";

import { useEffect, useState } from "react";

export interface PartnerData {
  id: string;
  company: string;
  status: string;
  tier: string;
  totalCommission: number;
  totalReferrals: number;
}

export interface PartnerCommission {
  id: string;
  amount: number;
  status: string;
  earnedAt: string;
}

export interface RegisterPartnerInput {
  [key: string]: unknown;
}

/**
 * Partner directory. Returns an empty list until the partner API endpoint is
 * wired; the UI renders its empty state in the meantime.
 */
export function usePartners() {
  const [data, setData] = useState<PartnerData[] | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setData([]);
    setIsLoading(false);
  }, []);

  return { data, isLoading };
}

/** Commissions for a partner (or all partners when partnerId is null). */
export function usePartnerCommissions(partnerId: string | null) {
  const [data, setData] = useState<PartnerCommission[] | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setData([]);
    setIsLoading(false);
  }, [partnerId]);

  return { data, isLoading };
}

/** Partner self-registration mutation. */
export function useRegisterPartner() {
  const [isPending, setIsPending] = useState(false);

  const mutateAsync = async (input: RegisterPartnerInput) => {
    setIsPending(true);
    try {
      // Integrate with the partner API once the endpoint is available.
      return input;
    } finally {
      setIsPending(false);
    }
  };

  return { mutateAsync, isPending };
}
