# 🐳 The $5/mo Lean Solopreneur VPS Stack

Run your entire One-Person Company back-office on a single **2 vCPU / 4 GB RAM VPS** (e.g., Hetzner CPX21 or DigitalOcean Droplet) for **$5–$8/month**, replacing over **$300+/month** in SaaS subscriptions.

## Included Services

| Service | Port | Replaces | Purpose |
| :--- | :---: | :--- | :--- |
| **[n8n](https://github.com/n8n-io/n8n)** | `5678` | Zapier / Make ($69/mo) | Workflow automation & AI agent orchestration |
| **[Umami](https://github.com/umami-software/umami)** | `3001` | Plausible / GA4 ($19/mo) | Privacy-first web & conversion analytics |
| **[Listmonk](https://github.com/knadh/listmonk)** | `9000` | Mailchimp / ConvertKit ($59/mo) | High-speed newsletter & email campaigns (pair with AWS SES) |
| **[Uptime Kuma](https://github.com/louislam/uptime-kuma)** | `3002` | BetterStack / Pingdom ($29/mo) | Uptime monitoring, Telegram alerts & public status page |
| **[WAHA](https://github.com/devlikeapro/waha)** | `3003` | Wati / Twilio WA ($49/mo) | Self-hosted WhatsApp HTTP REST API & MCP server |
| **PostgreSQL 16 + Redis 7** | Internal | Managed DBs ($30/mo) | Shared database & cache backbone for all services |

## Quick Start

```bash
cp .env.example .env
# Edit .env with strong secrets, then launch:
docker compose up -d
```

> **Pro Tip:** Deploy this `docker-compose.yml` directly inside **[Coolify](https://github.com/coollabsio/coolify)** or **[Dokploy](https://github.com/Dokploy/dokploy)** to get automatic HTTPS/SSL certificates and custom subdomains (`n8n.yourdomain.com`, `stats.yourdomain.com`, `status.yourdomain.com`) in one click.
