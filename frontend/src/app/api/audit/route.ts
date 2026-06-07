import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}))
  if (!body?.action) return NextResponse.json({ ok: false, error: 'action_required' }, { status: 400 })
  return NextResponse.json({ ok: true, audit_event: { id: `audit_${Date.now()}`, ...body } })
}
