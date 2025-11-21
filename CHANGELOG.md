# Changelog

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
