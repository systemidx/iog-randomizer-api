# Illusion of Gaia Randomizer API

API service for generating Illusion of Gaia randomizer seeds, patches, and permalinks.

---

## Quick Start (Debian 13 LXC / Native Linux)

### 1. Requirements
* Python 3.10+ (Debian 13 comes with Python 3.12/3.13)
* `python3-venv` and `python3-pip`

### 2. Running Locally / Server Startup
```bash
# Copy example configuration file
cp variables.conf.example variables.conf

# Start API service
./start.sh
```

---

## Environment Variables Configuration

The application uses `python-decouple` to configure application options and database connectivity via `variables.conf` or environment variables:

| Variable | Type | Default | Required? | Description |
| :--- | :--- | :--- | :--- | :--- |
| `DEBUG` | Boolean | `False` | Optional | Enable Flask debug mode (`True` / `False`). |
| `DB_ENABLED` | Boolean | `False` | Optional | Enable MongoDB persistence for permalinks. |
| `DB_USERNAME` | String | - | If `DB_ENABLED=True` | MongoDB authentication username. |
| `DB_PASSWORD` | String | - | If `DB_ENABLED=True` | MongoDB authentication password. |
| `DB_AUTHDB` | String | - | If `DB_ENABLED=True` | MongoDB authentication database (e.g. `admin`). |
| `DB_HOST` | String | - | If `DB_ENABLED=True` | MongoDB host IP or hostname (`192.168.6.20`). |
| `DB_PORT` | Integer | - | If `DB_ENABLED=True` | MongoDB server port (`27017`). |
| `DB_DATABASE_ID` | String | - | If `DB_ENABLED=True` | MongoDB target database name (`iog_randomizer`). |
| `DB_COLLECTION_ID` | String | - | If `DB_ENABLED=True` | MongoDB collection name (`dev_permalinks` or `prod_permalinks`). |

---

## Server Deployment

Detailed step-by-step setup guides for fresh **Debian 13 LXC containers** and **Jenkins CI/CD** pipeline configuration are provided in **[DEPLOYMENT.md](DEPLOYMENT.md)**.

* **Dev Server (LXC)**: `192.168.6.31` (Deploys `develop` branch)
* **Prod Server (LXC)**: `192.168.6.32` (Deploys `master` branch)
