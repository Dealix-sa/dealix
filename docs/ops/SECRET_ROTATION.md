# Secret Rotation

## Scope
This note defines a minimum operational process for rotating sensitive keys and tokens.

## Keys To Review
- app credentials
- database credentials
- WhatsApp access token
- webhook verification token

## Minimum Procedure
1. create replacement secret
2. update deployment environment
3. verify application health
4. revoke old secret
5. document the rotation date and owner

## Rules
- never commit secrets to the repository
- never print secrets in logs
- rotate immediately after suspected exposure