# Client Workspace Template (canonical)

This directory is the **canonical** Delivery & Client Success workspace template,
referenced by the Delivery & Client Success Operating System v1.

When a new client is onboarded (after payment / PO / written approval), copy
this entire folder into the private operations workspace:

```
cp -r clients/_template <private_ops>/clients/<client_name>_private
```

Then fill the files in the order described by
`docs/delivery/DELIVERY_OPERATING_ROUTINE.md`.

Notes:
- Do **not** put client-specific data into this template directory.
- Do **not** commit private client folders to the public repository.
- The older `clients/_TEMPLATE/` (uppercase) directory is kept for legacy
  delivery flows; this `_template/` directory is the one the Delivery &
  Client Success OS expects.
