# StockWatch 

A microservices-based inventory management system with real-time low-stock email alerts. Built as a hands-on learning project demonstrating modern DevOps practices including containerization, service orchestration, CI/CD pipelines, and integration testing.

---

## 🎯 What It Does

StockWatch monitors product inventory and sends automated email alerts when stock levels drop below configurable thresholds. Users can:

- Add, update, and delete products through a clean web dashboard
- Set per-product stock thresholds
- View real-time status indicators (healthy, low, critical)
- Trigger manual stock checks on demand
- Configure the email recipient for alerts
- See a history of sent alerts

## 🏗️ Architecture

StockWatch is composed of **three microservices** plus a PostgreSQL database, orchestrated with Docker Compose:


### Services

| Service | Stack | Port | Responsibility |
|---------|-------|------|----------------|
| **Frontend** | Node.js + Express + Vanilla JS | 8000 | Serves the dashboard UI |
| **Inventory** | Node.js + Express + pg | 3000 | Product CRUD, threshold evaluation, alert triggering |
| **Notification** | Python + Flask + smtplib | 3002 | Sends emails via SMTP |
| **PostgreSQL** | Postgres 16 

### Design Principles

- **Single responsibility** — each service does one thing well
- **Data ownership** — only the Inventory service talks to the database
- **HTTP communication** — services interact over REST APIs, language-agnostic
- **Environment-driven configuration** — 12-factor app principles throughout
- **Fail-fast validation** — services crash on startup if required config is missing

---



---

##  Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/install/) v2
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) (for sending alerts)

### 1. Clone and Configure

```bash
git clone <your-repo-url>
cd stockwatch
cp .env.example .env
```

Edit `.env` with your settings (see [Environment Variables](#-environment-variables) below).

### 2. Start the Stack

```bash
docker compose up --build
```

First-time build takes ~2 minutes. Subsequent starts are cached and fast.

### 3. Open the Dashboard

Navigate to **http://localhost:8000** in your browser. You should see the StockWatch dashboard with a green "SERVICES ONLINE" indicator.

### 4. Try It Out

1. Add a product: name `USB-C Cable`, quantity `3`, threshold `5`
2. The product appears with an orange/red progress bar (low stock)
3. Check your inbox — you should receive a low-stock alert email!

---

## ⚙️ Environment Variables

Create a `.env` file at the project root with the following:

```bash
# ─── PostgreSQL ────────────────────────────────────────
POSTGRES_USER=stockwatch
POSTGRES_PASSWORD=change-me-in-production
POSTGRES_DB=stockwatch
DATABASE_URL=postgresql://stockwatch:change-me-in-production@postgres:5432/stockwatch

# ─── Frontend ──────────────────────────────────────────
FRONTEND_PORT=8000
FRONTEND_HOST=0.0.0.0
API=http://localhost:3000

# ─── Inventory Service ─────────────────────────────────
INVENTORY_PORT=3000
INVENTORY_HOST=0.0.0.0
CORS_ORIGIN=*
ALERT_RECIPIENT=admin@example.com

# ─── Notification Service ──────────────────────────────
NOTIFICATION_PORT=3002
NOTIFICATION_HOST=0.0.0.0

# SMTP (Gmail example — use an App Password, not your regular password)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM=your-email@gmail.com


```

> ⚠️ **Gmail setup**: Enable 2FA on your Google account, then generate an App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords). Use this 16-character code as `SMTP_PASSWORD` — not your regular password.







## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/main.yml`) that:

1. **Builds and pushes** three Docker images in parallel to Docker Hub
2. **Runs integration tests** against the pushed images using `docker-compose.ci.yaml`
3. **Dumps container logs** on failure for easy debugging
4. **Always cleans up** containers, even if tests fail

### Trigger a Build

The workflow is triggered manually with a version tag:

1. Go to **Actions** tab in GitHub
2. Select **"Build, Push & Integration Test"**
3. Click **"Run workflow"**
4. Enter a version (e.g., `v1.0.0` or `latest`)

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASS` | Docker Hub password or access token |

### Published Images

After a successful build, images are available at:

- `<DOCKER_USERNAME>/devops2-frontend:<version>`
- `<DOCKER_USERNAME>/devops2-backend:<version>`
- `<DOCKER_USERNAME>/devops2-notifications:<version>`

---

## Development

### Running a Single Service Locally

Useful for active development without rebuilding Docker images:

```bash
# Notification service
cd notification-service
pip install -r requirements.txt
python app.py

# Inventory service
cd inventory-service
npm install
node index.js

# Frontend
cd frontend
npm install
node server.js
```

Remember to set the required environment variables in your shell (`export PORT=3000` etc.).

### Viewing Logs

```bash
# All services, live tail
docker compose logs -f

# Just one service
docker compose logs -f notification

# Last 50 lines
docker compose logs --tail=50 inventory

# Errors only
docker compose logs inventory | grep -i error
```

### Database Access

Connect directly to Postgres for inspection using external database from neon:



### Rebuilding After Code Changes

```bash
# Rebuild one service
docker compose up --build -d frontend

# Force fresh build (no cache)
docker compose build --no-cache inventory
docker compose up -d inventory
```

---

##  Troubleshooting

### Frontend shows "INVENTORY SERVICE OFFLINE"

The browser can't reach the inventory service. Check:

1. Is inventory running? `docker compose ps`
2. Does `curl http://localhost:3000/health` work from your terminal?
3. Check DevTools → Console for CORS errors
4. Verify `CORS_ORIGIN=*` in `.env`

### Port already in use

```
Error: bind: address already in use
```

Something else is holding the port. Either stop it or change the port in `.env`:

```bash
lsof -i :8000               # find what's using the port
# kill it, or change FRONTEND_PORT in .env
```

### Notification service crash-loops

Usually missing SMTP credentials. Check logs:

```bash
docker compose logs notification
```

If you see ` SMTP_USER and SMTP_PASSWORD env vars are required`, fill them in `.env` and restart.

### Email not arriving

1. Check notification logs for auth errors
2. Verify you're using a **Gmail App Password** (16 chars), not your regular password
3. Test the endpoint directly:
   ```bash
   curl -X POST http://localhost:3002/notify \
     -H 'Content-Type: application/json' \
     -d '{"to":"you@example.com","subject":"Test","message":"Hi"}'
   ```
4. Check spam folder





##  Possible Next Steps

Things that would evolve this further toward a production system:

- Replace HTTP with a message queue (RabbitMQ, Kafka) so notification failures don't block inventory
- Add an API Gateway (Nginx, Kong) as a single entry point

- Add Prometheus metrics + Grafana dashboards
- Deploy to Kubernetes with Helm charts
- Add distributed tracing (Jaeger, OpenTelemetry)

---

## License

MIT — do whatever you want with this code.

---

## Acknowledgments
This project is under continous devopment
Built as a DevOps learning exercise by [Mohamed](https://github.com/mkmahmoud)