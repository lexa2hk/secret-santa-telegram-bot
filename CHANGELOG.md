# Changelog

## v2.0.0 - 2025-11-21

### Breaking Changes
- 🔄 Migrated from SQLite to PostgreSQL for production readiness
- 🔐 Database connection now requires `DATABASE_URL` environment variable

### Added
- 🚀 Production-ready deployment with Docker Compose
- 🗄️ PostgreSQL database with connection pooling (2-10 connections)
- 🔒 Multi-stage Docker build for smaller, more secure images
- 👤 Non-root user in Docker container for enhanced security
- 🏥 Database health checks in Docker Compose
- 🌐 Isolated Docker network for database security
- 📊 Comprehensive logging throughout database layer
- 🔧 Database backup and restore documentation
- 📚 Production deployment guide (DEPLOYMENT.md)
- 🐧 Complete Ubuntu Server setup guide (UBUNTU_SETUP.md)
- 📖 Quick-start commands in README

### Changed
- ⚡ Improved performance with connection pooling
- 🔄 Updated all database queries to use PostgreSQL syntax
- 📦 Replaced `AUTOINCREMENT` with `SERIAL` for auto-incrementing IDs
- 🔀 Changed from `?` to `%s` parameter placeholders
- 🛡️ Enhanced error handling with proper exception logging

### Technical
- Python 3.13 (updated from 3.14 requirement)
- psycopg 3.2+ with binary package
- PostgreSQL 16 Alpine in Docker
- Connection pool: min 2, max 10, timeout 30s
- Foreign key constraints with CASCADE delete

## v1.0.0 - 2025-11-21

### Added
- 🎅 Complete Secret Santa bot implementation
- 🌍 Multi-language support (English & Russian)
- 💬 Anonymous messaging between participants and their Secret Santa
- 📅 Event date and price configuration
- 🎲 Random Secret Santa assignment algorithm
- 📬 Private DM notifications
- 🎁 /myassignment command to check assignments anytime
- 📖 Comprehensive /help command
- ✨ Beautiful emoji-enhanced messages
- 🏗️ Organized project structure with separate handler modules

### Features
- Admin-only commands (setup, assign, configure)
- Participant commands (join, view info, chat)
- Group management with SQLite database
- Invite link generation
- Language switching (/lang en|ru)
- Markdown-formatted messages
- Actionable error messages with helpful hints

### Technical
- Python 3.14+
- python-telegram-bot library
- SQLite database
- UV package manager support
- Modular architecture with clean separation of concerns
