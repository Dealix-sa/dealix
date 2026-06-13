import { test, expect } from '@playwright/test';

test('public home page loads', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Dealix|ديليكس|Revenue|AI/i);
});

test('health endpoint returns ok', async ({ request }) => {
  const res = await request.get('/api/health');
  expect(res.ok()).toBeTruthy();
  const body = await res.json();
  expect(body.status).toBe('ok');
});

test('diagnostic route is reachable', async ({ page }) => {
  await page.goto('/ar/diagnostic');
  await expect(page.locator('body')).toBeVisible();
});
