// Next.js conversion-funnel smoke — apps/web.
// Covers the canonical offer ladder page, the /contact LeadForm, and the
// /api/leads capture route. All submitted data is clearly [TEST]-labeled.

const { test, expect } = require("@playwright/test");

test("home renders with a visible H1", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("h1").first()).toBeVisible();
});

test("/ar/offers renders the 6-rung canonical ladder", async ({ page }) => {
  await page.goto("/ar/offers");
  await expect(page.getByText("عروض Dealix").first()).toBeVisible();
  const cards = page.locator("main .grid").first().locator("> div");
  await expect(cards).toHaveCount(6);
  await expect(page.getByText("7,500–25,000 ريال").first()).toBeVisible();
});

test("/ar/pricing shows the same canonical ladder", async ({ page }) => {
  await page.goto("/ar/pricing");
  const cards = page.locator("main .grid").first().locator("> article");
  await expect(cards).toHaveCount(6);
});

test("/contact LeadForm submits and confirms receipt", async ({ page }) => {
  await page.goto("/contact");
  await page.locator('input[placeholder="شركتك"]').fill("[TEST] Playwright Co");
  await page.locator('input[placeholder="عيادات، عقار، لوجستيات..."]').fill("clinics");
  await page.locator('input[type="email"]').fill("pw-test@example.com");
  const respPromise = page.waitForResponse((r) => r.url().includes("/api/leads"));
  await page.getByRole("button", { name: /أرسل الطلب/ }).click();
  const resp = await respPromise;
  expect([200, 202]).toContain(resp.status()); // 200 forwarded / 202 graceful fallback
  await expect(page.getByText("استلمنا طلبك")).toBeVisible();
});

test("POST /api/leads accepts a valid lead", async ({ request }) => {
  const res = await request.post("/api/leads", {
    data: { company: "[TEST] API Co", sector: "logistics", email: "api-test@example.com" },
  });
  expect([200, 202]).toContain(res.status());
  expect((await res.json()).accepted).toBe(true);
});

test("POST /api/leads rejects missing fields", async ({ request }) => {
  const res = await request.post("/api/leads", { data: { company: "[TEST] only" } });
  expect(res.status()).toBe(400);
});
