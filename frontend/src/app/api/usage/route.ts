import { NextResponse } from 'next/server'

const allowedEvents = new Set(['lead_created','agent_run','offer_created','proof_item_added','report_generated'])

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}))
  if (!body?.tenant_id) return NextResponse.json({ ok: false, error: 'tenant_id_required' }, { status: 400 })
  if (!allowedEvents.has(body?.event_type)) return NextResponse.json({ ok: false, error: 'invalid_event_type' }, { status: 400 })
  return NextResponse.json({ ok: true, usage_event: { id: `usage_${Date.now()}`, ...body } })
}
