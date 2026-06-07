import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({ ok: true, tenants: [] })
}

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}))
  if (!body?.name) return NextResponse.json({ ok: false, error: 'name_required' }, { status: 400 })
  return NextResponse.json({ ok: true, tenant: { id: `tenant_${Date.now()}`, name: body.name, plan: body.plan || 'starter' } })
}
