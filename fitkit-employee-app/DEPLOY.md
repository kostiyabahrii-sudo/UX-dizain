# Deploying the Fitkit workspace

The whole app is one Docker image (`Dockerfile` in this folder): the Go API serves the built React front-end, so one web service plus one PostgreSQL database is all you need. It listens on `$PORT` (set by the platform) or `:8080`.

## Environment variables

| Variable | Required | What |
| --- | --- | --- |
| `DATABASE_URL` | yes | PostgreSQL connection string (from the platform's database) |
| `BOOTSTRAP_ADMIN_EMAIL`, `BOOTSTRAP_ADMIN_PASSWORD` | first deploy | Creates the first sign-in (shift lead) **only while the database has no employees**. Password 10+ characters. Can be removed after the first start. |
| `BOOTSTRAP_ADMIN_NAME` | no | Display name of that account (default “Адміністратор”) |
| `CLIENT_APP_WEBHOOK_SECRET`, `TRACKER_WEBHOOK_SECRET` | for webhooks | Long random strings; `/webhooks/*` answer 503 until set |
| `SECURE_COOKIE` | recommended | `true` on HTTPS (the app also detects HTTPS behind the platform's proxy) |
| `JOBS_INTERVAL` | no | Background jobs period, default `1m` |
| `ALLOW_SEED` | never in production | `seed` wipes the database; it refuses to run without `ALLOW_SEED=true` |

Migrations run automatically on every start.

## Option A — Render (config in the repo)

`render.yaml` in the repository root describes the web service and the database.

1. Sign in at render.com with GitHub and give Render access to this repository.
2. **New → Blueprint**, choose the repository and the branch with this code.
3. Fill in `BOOTSTRAP_ADMIN_EMAIL`, `BOOTSTRAP_ADMIN_PASSWORD`, `BOOTSTRAP_ADMIN_NAME` when asked. Webhook secrets are generated.
4. Apply. When the deploy is green, open the `…onrender.com` address and sign in with the bootstrap account.

The plans in `render.yaml` are examples; check current pricing before applying.

## Option B — Railway

1. Sign in at railway.com with GitHub. **New Project → Deploy from GitHub repo**, pick this repository and branch.
2. In the service settings set **Root Directory** to `fitkit-employee-app` (Railway then builds the `Dockerfile`).
3. **+ New → Database → PostgreSQL** in the same project.
4. Service **Variables**: `DATABASE_URL=${{Postgres.DATABASE_URL}}`, `SECURE_COOKIE=true`, the two webhook secrets, and the `BOOTSTRAP_ADMIN_*` values.
5. **Settings → Networking → Generate Domain**, open it and sign in.

## After the first deploy

- Add employees: sign in as the bootstrap lead; until an admin screen exists, run `api create-employee -name … -email … -role buyer|lead|warehouse|support -password …` in the platform's shell (Render: Shell tab; Railway: `railway run` / service shell).
- Give the Fitkit client app the webhook URL `https://<your-domain>/webhooks/client-app/…` and `CLIENT_APP_WEBHOOK_SECRET`.
- One instance only for now: live updates and the sign-in throttle are in memory.
- Nova Poshta, tracking aggregator, refunds and client notices are still fakes that only log (see `api/README.md`).
