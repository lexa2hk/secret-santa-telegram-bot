# Production Deployment Guide

This guide provides detailed instructions for deploying the Secret Santa Telegram Bot in a production environment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Docker Deployment](#docker-deployment)
- [Database Management](#database-management)
- [Monitoring](#monitoring)
- [Backup and Recovery](#backup-and-recovery)
- [Security Considerations](#security-considerations)
- [Scaling](#scaling)

## Prerequisites

### System Requirements

- **Server**: Linux server (Ubuntu 20.04+ or similar)
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Memory**: Minimum 512MB RAM (1GB+ recommended)
- **Storage**: 5GB+ available disk space

### Required Accounts

- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Server with SSH access
- Domain name (optional, for easier access)

## Environment Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd secret-santa-telegram-bot
```

### 2. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with production values:

```bash
# Telegram Bot Token (Required)
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# PostgreSQL Configuration
POSTGRES_USER=secretsanta
POSTGRES_PASSWORD=<generate-strong-password>
POSTGRES_DB=secretsanta
```

**Security Best Practices:**

1. Generate a strong password (20+ characters):
```bash
openssl rand -base64 32
```

2. Protect the `.env` file:
```bash
chmod 600 .env
```

3. Never commit `.env` to version control

## Docker Deployment

### Initial Deployment

1. **Build and start the services:**

```bash
docker-compose up -d
```

2. **Verify services are running:**

```bash
docker-compose ps
```

You should see:
- `secret-santa-bot` - running
- `secret-santa-db` - running (healthy)

3. **Check logs for errors:**

```bash
# All services
docker-compose logs -f

# Bot only
docker-compose logs -f bot

# Database only
docker-compose logs -f db
```

### Updates and Maintenance

**Update to latest version:**

```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Restart services:**

```bash
docker-compose restart
```

**Stop services:**

```bash
docker-compose down
```

## Database Management

### Accessing the Database

**PostgreSQL shell:**

```bash
docker-compose exec db psql -U secretsanta secretsanta
```

**Run SQL queries:**

```bash
docker-compose exec db psql -U secretsanta secretsanta -c "SELECT * FROM groups;"
```

### Database Schema

The bot automatically creates these tables:

- **groups**: Stores Secret Santa group information
- **participants**: Stores participant information and assignments

### Database Migrations

Currently, the bot uses automatic schema initialization. For future schema changes:

1. Create backup (see Backup section)
2. Update database.py
3. Restart bot to apply changes

## Monitoring

### Log Monitoring

**Real-time logs:**

```bash
docker-compose logs -f bot
```

**Recent logs:**

```bash
docker-compose logs --tail=100 bot
```

**Save logs to file:**

```bash
docker-compose logs bot > bot.log
```

### Resource Monitoring

**Container resource usage:**

```bash
docker stats
```

**Disk usage:**

```bash
docker system df
```

**Database size:**

```bash
docker-compose exec db psql -U secretsanta secretsanta -c "SELECT pg_size_pretty(pg_database_size('secretsanta'));"
```

### Health Checks

The PostgreSQL container includes automatic health checks:

```bash
docker-compose ps
```

Look for `(healthy)` status next to the database.

## Backup and Recovery

### Automated Backups

**Create a backup script** (`backup.sh`):

```bash
#!/bin/bash
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/secretsanta_$DATE.sql"

mkdir -p $BACKUP_DIR
docker-compose exec -T db pg_dump -U secretsanta secretsanta > $BACKUP_FILE

# Keep only last 30 days
find $BACKUP_DIR -name "secretsanta_*.sql" -mtime +30 -delete

echo "Backup created: $BACKUP_FILE"
```

**Make executable and schedule:**

```bash
chmod +x backup.sh

# Add to crontab (daily at 2 AM)
crontab -e
# Add line:
0 2 * * * /path/to/backup.sh
```

### Manual Backup

**Create backup:**

```bash
docker-compose exec db pg_dump -U secretsanta secretsanta > backup_$(date +%Y%m%d).sql
```

**Compress backup:**

```bash
gzip backup_*.sql
```

### Restore from Backup

**Restore database:**

```bash
docker-compose exec -T db psql -U secretsanta secretsanta < backup.sql
```

**Restore from compressed backup:**

```bash
gunzip -c backup.sql.gz | docker-compose exec -T db psql -U secretsanta secretsanta
```

## Security Considerations

### Network Security

1. **Firewall**: Only allow necessary ports
```bash
# Allow SSH
ufw allow 22/tcp

# Deny PostgreSQL from external access (only internal Docker network)
ufw deny 5432/tcp

ufw enable
```

2. **Docker network**: Database is isolated in `secret-santa-network`

### Application Security

1. **Non-root user**: Bot runs as `botuser` (UID 1000)
2. **Environment variables**: Sensitive data stored in `.env`
3. **Connection pooling**: Limits database connections

### Regular Maintenance

1. **Update dependencies:**
```bash
uv sync --upgrade
```

2. **Update Docker images:**
```bash
docker-compose pull
docker-compose up -d
```

3. **Review logs** for suspicious activity

## Scaling

### Vertical Scaling

**Increase resources in docker-compose.yml:**

```yaml
services:
  bot:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M

  db:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
```

### Connection Pool Tuning

Edit `bot/database.py`:

```python
self.pool = ConnectionPool(
    self.db_url,
    min_size=5,      # Increase for high traffic
    max_size=20,     # Increase for high traffic
    timeout=30,
    max_idle=300,
    max_lifetime=3600,
)
```

### Horizontal Scaling

For very high traffic:

1. Use external PostgreSQL (AWS RDS, Google Cloud SQL, etc.)
2. Run multiple bot instances with load balancer
3. Configure shared database connection

## Troubleshooting

### Bot not starting

```bash
# Check logs
docker-compose logs bot

# Common issues:
# 1. Invalid BOT_TOKEN
# 2. Database not ready (wait 10-20 seconds)
# 3. Port conflicts
```

### Database connection errors

```bash
# Check database health
docker-compose ps db

# Restart database
docker-compose restart db

# Check connectivity
docker-compose exec bot ping db
```

### Out of memory

```bash
# Check memory usage
free -h

# Increase swap space or upgrade server
# Reduce connection pool size
```

## Support

For issues and questions:
- Check logs: `docker-compose logs -f`
- Review troubleshooting section in README.md
- Open an issue on GitHub

## Quick Reference

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Backup database
docker-compose exec db pg_dump -U secretsanta secretsanta > backup.sql

# Restore database
docker-compose exec -T db psql -U secretsanta secretsanta < backup.sql

# Access database
docker-compose exec db psql -U secretsanta secretsanta

# Check status
docker-compose ps
```
