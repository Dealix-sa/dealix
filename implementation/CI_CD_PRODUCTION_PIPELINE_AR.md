# CI/CD Production Pipeline

## الهدف
بناء pipeline إنتاج لا يدفع كودًا خطيرًا ولا يخلط بين readiness وdeployment.

## Jobs المقترحة
1. Python scripts readiness.
2. Env contract check.
3. Secret/public exposure check.
4. DB migration manifest check.
5. TypeScript build check.
6. Playwright smoke tests.
7. Deployment smoke after deploy.

## صلاحيات GitHub Actions
الافتراضي:

```yaml
permissions:
  contents: read
```

أي deployment job يحتاج صلاحية مخصصة وبيئة GitHub Environment بموافقة بشرية.
