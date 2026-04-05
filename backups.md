# Database Backup and Restore Guide

## Table of Contents
1. [Creating a Backup from Production](#creating-a-backup-from-production)
2. [Downloading the Backup](#downloading-the-backup)
3. [Restoring in Linux Bash](#restoring-in-linux-bash)
4. [Restoring in PowerShell (Windows)](#restoring-in-powershell-windows)
5. [Troubleshooting](#troubleshooting)

---

## Creating a Backup from Production

### Step 1: SSH into the Production Server

```bash
ssh user@your-server.com
```

### Step 2: Create the Database Backup

Create a timestamped backup file:

```bash
docker exec frisbeer-db pg_dump -U postgres postgres > backup_$(date +%Y-%m-%d_%H%M%S).sql
```

This creates a file like `backup_2026-04-05_121706.sql`

### Step 3: Verify the Backup

Check that the backup file was created:

```bash
ls -lh backup_*.sql
```

You should see something like:
```
-rw-r--r-- 1 user user 5.2M Apr 5 12:17 backup_2026-04-05_121706.sql
```

---

## Downloading the Backup

### Option A: Using SCP (Recommended)

**From Linux/Mac:**
```bash
scp user@your-server.com:~/backup_2026-04-05_121706.sql ./backup.sql
```

**From PowerShell (Windows):**
```powershell
scp user@your-server.com:~/backup_2026-04-05_121706.sql C:\Users\Joonas\backup.sql
```

### Option B: Using SSH Pipe (One Command)

**From Linux/Mac:**
```bash
ssh user@your-server.com "cat ~/backup_2026-04-05_121706.sql" > backup.sql
```

**From PowerShell (Windows):**
```powershell
ssh user@your-server.com "cat ~/backup_2026-04-05_121706.sql" | Out-File -Encoding UTF8 backup.sql
```

### Option C: Direct Stream and Restore (No Download Needed)

**From Linux/Mac:**
```bash
ssh user@your-server.com "cat ~/backup_2026-04-05_121706.sql" | docker exec -i frisbeer-db psql -U postgres postgres
```

**From PowerShell (Windows):**
```powershell
ssh user@your-server.com "cat ~/backup_2026-04-05_121706.sql" | docker exec -i frisbeer-db psql -U postgres postgres
```

---

## Restoring in Linux Bash

### Prerequisites
- Docker is running
- PostgreSQL container is running: `docker ps | grep frisbeer-db`

### Step 1: Clear Existing Data (Optional but Recommended)

If you want to completely replace the local database:

```bash
docker exec frisbeer-db psql -U postgres postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### Step 2: Restore from Backup File

```bash
cat backup_2026-04-05_121706.sql | docker exec -i frisbeer-db psql -U postgres postgres
```

Or directly from the remote server (no download needed):

```bash
ssh user@your-server.com "cat ~/backup_2026-04-05_121706.sql" | docker exec -i frisbeer-db psql -U postgres postgres
```

### Step 3: Verify the Restore

```bash
docker exec frisbeer-db psql -U postgres postgres -c "SELECT COUNT(*) FROM frisbeer_player;"
```

You should see a number representing the player count from production.

### Step 4: Create Missing Role (if needed)

If you see an error about role "frisbeer" not existing:

```bash
docker exec frisbeer-db psql -U postgres -c "CREATE ROLE frisbeer;"
```

---

## Restoring in PowerShell (Windows)

### Prerequisites
- Docker Desktop is running
- PostgreSQL container is running: `docker ps | grep frisbeer-db`
- SSH is available: `ssh -V`

### Step 1: Clear Existing Data (Optional but Recommended)

If you want to completely replace the local database:

```powershell
docker exec frisbeer-db psql -U postgres postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### Step 2: Restore from Local Backup File

**Download the backup first, then:**

```powershell
Get-Content .\backup_2026-04-05_121706.sql | docker exec -i frisbeer-db psql -U postgres postgres
```

Or using the `cat` alias:

```powershell
cat .\backup_2026-04-05_121706.sql | docker exec -i frisbeer-db psql -U postgres postgres
```

### Step 3: Restore Directly from Remote Server (No Download)

Stream the backup directly from production:

```powershell
ssh user@your-server.com "cat ~/backup_2026-04-05_121706.sql" | docker exec -i frisbeer-db psql -U postgres postgres
```

### Step 4: Verify the Restore

```powershell
docker exec frisbeer-db psql -U postgres postgres -c "SELECT COUNT(*) FROM frisbeer_player;"
```

You should see a number representing the player count from production.

### Step 5: Create Missing Role (if needed)

If you see an error about role "frisbeer" not existing:

```powershell
docker exec frisbeer-db psql -U postgres -c "CREATE ROLE frisbeer;"
```

---

## Troubleshooting

### Error: "relation already exists" or "multiple primary keys"

**Cause:** Local database already has tables from a previous backup.

**Solution:** Clear the schema before restoring:

**Bash:**
```bash
docker exec frisbeer-db psql -U postgres postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

**PowerShell:**
```powershell
docker exec frisbeer-db psql -U postgres postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

### Error: "role \"frisbeer\" does not exist"

**Cause:** The backup references a role that doesn't exist in your local database.

**Solution:** Create the role:

```bash
docker exec frisbeer-db psql -U postgres -c "CREATE ROLE frisbeer;"
```

### Error: "Get-Content: command not found" (PowerShell on Linux)

**Cause:** You're using bash on Linux, not PowerShell.

**Solution:** Use bash syntax instead:

```bash
cat backup_2026-04-05_121706.sql | docker exec -i frisbeer-db psql -U postgres postgres
```

### Error: "docker exec -i not supported" 

**Cause:** Docker daemon not responding or container not running.

**Solution:** Check container status:

```bash
docker ps | grep frisbeer-db
```

If not running:

```bash
docker-compose up -d
```

### SSH Connection Refused

**Cause:** SSH credentials or server address incorrect.

**Solution:** 
1. Verify server is reachable: `ping your-server.com`
2. Verify SSH is enabled on the server
3. Check credentials: `ssh -v user@your-server.com`

### Backup File is Very Large / Taking Too Long

**Solution:** Compress the backup:

**Creating compressed backup (on server):**
```bash
docker exec frisbeer-db pg_dump -U postgres postgres | gzip > backup_$(date +%Y-%m-%d_%H%M%S).sql.gz
```

**Restoring compressed backup:**

**Bash:**
```bash
gunzip -c backup_2026-04-05_121706.sql.gz | docker exec -i frisbeer-db psql -U postgres postgres
```

**PowerShell:**
```powershell
Get-Content backup_2026-04-05_121706.sql.gz | Out-String | docker exec -i frisbeer-db psql -U postgres postgres
```

---

## Quick Reference Commands

### Bash

```bash
# Create backup
docker exec frisbeer-db pg_dump -U postgres postgres > backup_$(date +%Y-%m-%d_%H%M%S).sql

# Download from server
scp user@your-server.com:~/backup_*.sql ./

# Clear local database
docker exec frisbeer-db psql -U postgres postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restore backup
cat backup_2026-04-05_121706.sql | docker exec -i frisbeer-db psql -U postgres postgres

# Verify restore
docker exec frisbeer-db psql -U postgres postgres -c "SELECT COUNT(*) FROM frisbeer_player;"
```

### PowerShell

```powershell
# Download from server
scp user@your-server.com:~/backup_*.sql ./

# Clear local database
docker exec frisbeer-db psql -U postgres postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restore backup
cat .\backup_2026-04-05_121706.sql | docker exec -i frisbeer-db psql -U postgres postgres

# Verify restore
docker exec frisbeer-db psql -U postgres postgres -c "SELECT COUNT(*) FROM frisbeer_player;"
```

---

## Connection Details (for Reference)

From [docker-compose.yml](docker/docker-compose.yml):

- **Container:** frisbeer-db
- **Image:** postgres:11
- **Database:** postgres
- **User:** postgres
- **Password:** See `docker/docker-compose.yml` (POSTGRES_PASSWORD variable)
- **Port:** 5432
- **Volume:** pg-data
