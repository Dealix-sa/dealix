export type LeadInput = {
  company: string;
  email?: string;
  phone?: string;
  pain: string;
  sector?: string;
};

export function validateLeadInput(input: LeadInput): string[] {
  const errors: string[] = [];
  if (!input.company || input.company.length < 2) errors.push("company_required");
  if (!input.email && !input.phone) errors.push("contact_required");
  if (input.email && !/^\S+@\S+\.\S+$/.test(input.email)) errors.push("invalid_email");
  if (!input.pain || input.pain.length < 10) errors.push("pain_required");
  return errors;
}
