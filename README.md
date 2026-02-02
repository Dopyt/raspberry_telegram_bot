# Telegram Control & Utility Bot

A Python-based Telegram bot for **remote system monitoring and administration** of a Linux machine (Raspberry Pi), built using the Telegram Bot API.
The project started as a tool to remotely control and monitor a Raspberry Pi without SSH access and was later extended with **user-specific command sets**.

This project was my first meaningful hands-on project in a Linux environment. While building it, I learned how to work with system-level commands,
manage long-running processes, and securely handle API keys using environment variables. I also gained experience handling permissions and
structuring a small but extensible Python tool.

## Features
### System Monitoring & Control
- Uptime, CPU, memory, and disk usage
- Running processes overview
- Open ports and IP address lookup
- Remote OS update and reboot
- Command execution with timeout handling
- Message logging

### Multi-User Command Handling
- Different command sets per chat ID
- Custom utility responses
- Message forwarding between users

## Tech Stack
- Python 3
- Telegram Bot API
- Linux
- Raspberry Pi

## Configuration
Sensitive data is handled via environment variables:
```bash
export BOT_TOKEN="..."
export CHAT_ID_JA="..."
export CHAT_ID_EMMKA="..."
```

## Notes
- Designed to run in trusted environments only
