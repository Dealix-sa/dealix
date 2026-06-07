export type DealixRole = 'owner' | 'admin' | 'member' | 'viewer';

export type DealixSession = {
  userId: string;
  tenantId: string;
  workspaceId?: string;
  role: DealixRole;
};

export function assertTenantSession(session?: Partial<DealixSession>): DealixSession {
  if (!session?.userId || !session?.tenantId || !session?.role) {
    throw new Error('Unauthorized: missing tenant session');
  }
  return session as DealixSession;
}

export function canWrite(role: DealixRole): boolean {
  return role === 'owner' || role === 'admin' || role === 'member';
}
