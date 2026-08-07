import { NextResponse } from "next/server";
import { hubspotCommercialPayload } from "@/lib/hubspot-commercial-os";

export function GET() {
  return NextResponse.json({
    ...hubspotCommercialPayload,
    safety: {
      crmWritesRequireOwnerApproval: true,
      externalCommunicationEnabled: false,
      communicationMode: "draft_only",
      campaignsWritable: false,
    },
  });
}
