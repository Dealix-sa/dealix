import { NextResponse } from "next/server";
import { commandCenterPayload } from "@/lib/strategic-command-center";

export function GET() {
  return NextResponse.json(commandCenterPayload);
}
