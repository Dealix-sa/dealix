# API Key and Webhook Policy

- API keys تكون scoped لكل tenant.
- كل webhook له signing secret.
- rotate keys عند أي شك.
- لا يظهر secret في frontend.
- سجل webhook failures بدون payload حساس.
