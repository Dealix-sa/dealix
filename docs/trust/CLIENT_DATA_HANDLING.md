# Client Data Handling

How Dealix receives, stores, uses, and returns client data.

## On receipt
- Client data only enters through a defined channel (signed agreement, encrypted upload, or explicit consent).
- Logged in `dealix-ops-private/trust/data_intake_log.csv` with the date, source, sensitivity, and retention class.

## In use
- Stored under `dealix-ops-private/clients/<client-slug>/`.
- Access restricted to the assigned engagement team.
- Never copied to a public repo, public sheet, or third-party share without the client's written approval.
- Never used to train a model.

## In transit
- Encrypted in transit.
- Email attachments avoided for sensitive data; use a controlled link instead.

## On engagement close
- Per the retention class, data is either retained for the agreed period or returned and deleted.
- Deletion is logged in `dealix-ops-private/trust/deletion_log.csv`.

## On client request
- Client may request a copy of all their data within five working days.
- Client may request full deletion within ten working days.

## Rule
Client data is held in trust. Treat it as the founder would want her own data handled.
