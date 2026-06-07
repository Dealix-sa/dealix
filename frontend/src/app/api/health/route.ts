export async function GET() {
  return Response.json({
    service: 'dealix',
    status: 'ok',
    checks: ['api', 'routing'],
    timestamp: new Date().toISOString(),
  });
}
