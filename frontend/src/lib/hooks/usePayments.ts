"use client";

import { useEffect, useState } from "react";

export interface InvoiceItem {
  description: string;
}

export interface InvoiceData {
  id: string;
  number: string;
  amount: number;
  status: string;
  issuedAt: string;
  dueDate: string;
  items: InvoiceItem[];
}

export interface InvoiceList {
  data: InvoiceData[];
}

export interface SubscriptionData {
  status: string;
  planName: string;
  amount: number;
  interval: string;
  cancelAtPeriodEnd: boolean;
}

/**
 * Invoice history. Returns an empty list until the payments API endpoint is
 * wired; the UI renders its empty state in the meantime.
 */
export function useInvoices(_params?: { limit?: number }) {
  const [data, setData] = useState<InvoiceList | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setData({ data: [] });
    setIsLoading(false);
  }, []);

  return { data, isLoading };
}

/** Current subscription. Returns undefined until the billing API is wired. */
export function useSubscription() {
  const [data, setData] = useState<SubscriptionData | undefined>(undefined);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setData(undefined);
    setIsLoading(false);
  }, []);

  return { data, isLoading };
}

export function useUpdateSubscription() {
  const [isPending, setIsPending] = useState(false);
  const mutateAsync = async (input: Record<string, unknown>) => {
    setIsPending(true);
    try {
      return input;
    } finally {
      setIsPending(false);
    }
  };
  return { mutateAsync, isPending };
}

export function useCancelSubscription() {
  const [isPending, setIsPending] = useState(false);
  const mutateAsync = async (input: { cancelAtPeriodEnd: boolean }) => {
    setIsPending(true);
    try {
      return input;
    } finally {
      setIsPending(false);
    }
  };
  return { mutateAsync, isPending };
}
