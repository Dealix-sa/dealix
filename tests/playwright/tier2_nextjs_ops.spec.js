// @ts-check
const { test, expect } = require("@playwright/test");

const BASE = process.env.PLAYWRIGHT_NEXT_BASE_URL || "http://localhost:3000";
const LOCALE = process.env.PLAYWRIGHT_LOCALE || "ar";

test.describe("Next.js ops shell (Tier-2)", () => {
  test("login page loads", async ({ page }) => {
    await page.goto(`${BASE}/${LOCALE}/login`);
    await expect(page.locator("input[type=email]")).toBeVisible();
  });

  test("operator route redirects to login when unauthenticated", async ({ page }) => {
    await page.goto(`${BASE}/${LOCALE}/operator`);
    await page.waitForURL(/\/login/, { timeout: 15000 });
    expect(page.url()).toContain("/login");
  });

  test("offer page shows lead intake form", async ({ page }) => {
    await page.goto(`${BASE}/${LOCALE}/offer/lead-intelligence-sprint`);
    await expect(page.getByRole("button", { name: /إرسال|Submit/i })).toBeVisible();
  });
});
