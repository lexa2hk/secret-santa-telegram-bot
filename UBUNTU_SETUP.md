# Ubuntu Server Setup Guide

Complete guide to deploy the Secret Santa Telegram Bot on Ubuntu Server.

## Prerequisites

- Ubuntu Server 20.04 or newer
- SSH access to your server
- Root or sudo privileges
- Your Telegram Bot Token from [@BotFather](https://t.me/botfather)

## Step 1: Connect to Your Server

```bash
ssh username@your-server-ip
```

## Step 2: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 3: Install Docker

### Install Docker Engine

```bash
# Remove old versions (if any)
sudo apt remove docker docker-engine docker.io containerd runc

# Install dependencies
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker --version
```

### Add Your User to Docker Group (Optional)

This allows running Docker without `sudo`:

```bash
sudo usermod -aG docker $USER

# Log out and back in for changes to take effect
exit
# SSH back in
ssh username@your-server-ip

# Verify you can run docker without sudo
docker ps
```

## Step 4: Install Git

```bash
sudo apt install -y git
```

## Step 5: Clone the Bot Repository

```bash
# Create directory for the bot
mkdir -p ~/apps
cd ~/apps

# Clone the repository
git clone <your-repository-url> secret-santa-bot
cd secret-santa-bot

# Or if you uploaded files manually via SCP
# Skip this step and upload your files to ~/apps/secret-santa-bot
```

## Step 6: Configure the Bot

### Create Environment File

```bash
# Copy example file
cp .env.example .env

# Edit with nano or vim
nano .env
```

### Add Your Configuration

```bash
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_from_botfather

# PostgreSQL Database Configuration
POSTGRES_USER=secretsanta
POSTGRES_PASSWORD=your_strong_password_here
POSTGRES_DB=secretsanta
```

**To generate a strong password:**

```bash
openssl rand -base64 32
```

**Save and exit:**
- Press `Ctrl + X`
- Press `Y` to confirm
- Press `Enter` to save

### Secure the Environment File

```bash
chmod 600 .env
```

## Step 7: Start the Bot

```bash
# Start services in detached mode
docker compose up -d

# Or if using older docker-compose command:
# docker-compose up -d
```

**Expected output:**
```
[+] Running 3/3
 ✔ Network secret-santa-network      Created
 ✔ Container secret-santa-db         Started
 ✔ Container secret-santa-bot        Started
```

## Step 8: Verify Everything is Running

### Check Container Status

```bash
docker compose ps
```

You should see:
```
NAME                 STATUS              PORTS
secret-santa-bot     Up X minutes
secret-santa-db      Up X minutes (healthy)
```

### Check Logs

```bash
# View all logs
docker compose logs

# Follow bot logs in real-time
docker compose logs -f bot

# Follow database logs
docker compose logs -f db

# Press Ctrl+C to stop following logs
```

### Test the Bot

1. Open Telegram
2. Search for your bot
3. Send `/start` command
4. You should receive a welcome message in Russian (default language)

## Step 9: Set Up Automatic Restart (Optional but Recommended)

The containers are already configured with `restart: unless-stopped`, but let's ensure Docker starts on boot:

```bash
sudo systemctl enable docker
```

## Step 10: Set Up Automated Backups (Recommended)

### Create Backup Script

```bash
# Create backups directory
mkdir -p ~/backups

# Create backup script
nano ~/backup-bot.sh
```

**Add this content:**

```bash
#!/bin/bash
BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/secretsanta_$DATE.sql"

cd ~/apps/secret-santa-bot

# Create backup
docker compose exec -T db pg_dump -U secretsanta secretsanta > "$BACKUP_FILE"

# Compress backup
gzip "$BACKUP_FILE"

# Keep only last 30 days
find "$BACKUP_DIR" -name "secretsanta_*.sql.gz" -mtime +30 -delete

echo "Backup created: ${BACKUP_FILE}.gz"
```

**Make it executable:**

```bash
chmod +x ~/backup-bot.sh
```

**Test the backup:**

```bash
~/backup-bot.sh
ls -lh ~/backups/
```

### Schedule Daily Backups

```bash
# Open crontab
crontab -e

# Add this line (daily backup at 2 AM)
0 2 * * * /home/your-username/backup-bot.sh >> /home/your-username/backup.log 2>&1
```

## Common Operations

### View Logs

```bash
cd ~/apps/secret-santa-bot

# Real-time logs
docker compose logs -f

# Last 100 lines
docker compose logs --tail=100

# Bot logs only
docker compose logs -f bot
```

### Restart Bot

```bash
cd ~/apps/secret-santa-bot
docker compose restart
```

### Stop Bot

```bash
cd ~/apps/secret-santa-bot
docker compose down
```

### Start Bot

```bash
cd ~/apps/secret-santa-bot
docker compose up -d
```

### Update Bot

```bash
cd ~/apps/secret-santa-bot

# Pull latest changes
git pull

# Rebuild and restart
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Check Resource Usage

```bash
# Container stats
docker stats

# Disk usage
df -h

# Memory usage
free -h
```

## Backup and Restore

### Manual Backup

```bash
cd ~/apps/secret-santa-bot
docker compose exec db pg_dump -U secretsanta secretsanta > backup_$(date +%Y%m%d).sql
gzip backup_*.sql
```

### Restore from Backup

```bash
cd ~/apps/secret-santa-bot

# Decompress if needed
gunzip backup_20231221.sql.gz

# Restore
docker compose exec -T db psql -U secretsanta secretsanta < backup_20231221.sql
```

### Download Backup to Your Computer

```bash
# From your local computer
scp username@your-server-ip:~/backups/secretsanta_20231221.sql.gz ./
```

## Security Recommendations

### 1. Set Up Firewall

```bash
# Install UFW (usually pre-installed)
sudo apt install -y ufw

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 2. Keep System Updated

```bash
# Run weekly
sudo apt update
sudo apt upgrade -y
```

### 3. Monitor Logs Regularly

```bash
# Check for errors
docker compose logs --tail=100 | grep -i error
```

### 4. Strong Passwords

- Use strong passwords in `.env`
- Never commit `.env` to version control
- Keep `.env` permissions at 600

## Troubleshooting

### Bot Not Starting

```bash
# Check logs
docker compose logs bot

# Common issues:
# 1. Wrong BOT_TOKEN - check .env
# 2. Database not ready - wait 30 seconds and check again
# 3. Port already in use - check what's using the port
```

### Database Connection Errors

```bash
# Check if database is running
docker compose ps db

# Should show "healthy" status
# If not, check database logs
docker compose logs db

# Restart database
docker compose restart db
```

### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean Docker system
docker system prune -a

# Remove old backups
rm ~/backups/old_backup.sql.gz
```

### Can't Connect via SSH

```bash
# From local machine, check if server is reachable
ping your-server-ip

# Check if SSH is running (from server console)
sudo systemctl status ssh

# Restart SSH
sudo systemctl restart ssh
```

## Monitoring (Advanced)

### Set Up Log Rotation

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/docker-compose

# Add:
/home/your-username/apps/secret-santa-bot/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

### Monitor System Resources

```bash
# Install htop for better monitoring
sudo apt install -y htop

# Run htop
htop
```

## Quick Reference Commands

```bash
# Navigate to bot directory
cd ~/apps/secret-santa-bot

# Start bot
docker compose up -d

# Stop bot
docker compose down

# View logs
docker compose logs -f

# Restart bot
docker compose restart

# Check status
docker compose ps

# Backup database
docker compose exec db pg_dump -U secretsanta secretsanta > backup.sql

# Update bot
git pull && docker compose up -d --build
```

## Getting Help

If you encounter issues:

1. Check logs: `docker compose logs -f`
2. Verify `.env` file has correct values
3. Ensure Docker is running: `docker ps`
4. Check disk space: `df -h`
5. Review this guide and DEPLOYMENT.md

## Next Steps

After successful deployment:

1. ✅ Test the bot in a Telegram group
2. ✅ Set up automated backups
3. ✅ Configure firewall
4. ✅ Monitor logs regularly
5. ✅ Keep system updated

Your Secret Santa bot is now running in production! 🎉
