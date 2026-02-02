import requests
import time
import subprocess
import os
from datetime import datetime
from random import choice

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID_JA = os.environ["CHAT_ID_JA"]
CHAT_ID_EMMKA = os.environ["CHAT_ID_EMMKA"]
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

CUSTOM_COMMANDS = {
    '/status': 'uptime',
    '/disk': 'df -h',
    '/mem': 'free -h',
    '/temp': 'vcgencmd measure_temp',
    '/cpu': 'grep "model name" /proc/cpuinfo | head -1 && top -bn1 | grep "Cpu(s)"',
    '/ip': 'hostname -I',
    '/ps': 'ps -eo pid,comm,%mem,%cpu --sort=-%mem | head -n 6',
    '/ports': 'ss -tuln',
    '/who': 'who',
    '/update': 'sudo apt update && sudo apt upgrade -y',
    '/reboot': 'sudo reboot',
    '/log': 'tail -n 20 /home/matej/telegram_bot/bot.log',
    '/message': None,
    '/help': None,
}

BREAKFAST = ['kaiserka so šunkou', 'kaiserka s avokádom', 'kaiserka s maťkom', 'koláčik', 'páročky', 'praženica', 'omeleta', 'toastíky']
LUNCH = ['cestoviny s pestom', 'cestoviny s kuracím', 'kuracie s ryžou', 'zemaiky s balkánskym syrom', 'losos so zemiakmi']
DINNER = ['cestoviny s pestom', 'páročky', 'prazenica', 'omeleta', 'toasíky', 'losos so zemiakmi']

EMMKA_COMMANDS = {
    '/ranajky': lambda: choice(BREAKFAST),
    '/obed': lambda: choice(LUNCH),
    '/vecera': lambda: choice(DINNER),
    '/pomoc' : None,
}

def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    return requests.get(f'{API_URL}/getUpdates', params=params).json()

def log_message(username, chat_id, text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/home/matej/telegram_bot/bot.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {username} ({chat_id}): {text}\n")

def send_message(text, chat_id):
    requests.post(f'{API_URL}/sendMessage', data={'chat_id': chat_id, 'text': text})

def run_command(command):
    if command == '/help':
        return "🧠 Available commands:\n" + "\n".join(sorted(CUSTOM_COMMANDS))

    if command.startswith('/message'):
        message_text = command[len('/message '):].strip()
        send_message(message_text, CHAT_ID_EMMKA)
        return f"✅ Custom message sent ({message_text})"

    cmd = CUSTOM_COMMANDS.get(command)
    if not cmd:
        return "❌ Unknown command. Use /help."

    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=60, text=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return f"Error:\n{e.output.strip()}"
    except subprocess.TimeoutExpired:
        return "⚠️ Command timed out"

def run_command_emmka(command):
    if command == '/pomoc':
        send_message("🧠 Dostupné príkazy:\n" + "\n".join(sorted(EMMKA_COMMANDS)), CHAT_ID_EMMKA)
        return "✅ Helped emmka"
    
    if command in ['/ranajky', '/obed', '/vecera']:
        func = EMMKA_COMMANDS.get(command)
        food = func() if callable(func) else "niečo dobré"
        send_message(f"Môžeš si dať napríklad: {food} 😘", CHAT_ID_EMMKA)
        return f"✅ Food recommended ({food})"
    
    cmd = EMMKA_COMMANDS.get(command)
    if not cmd:
        send_message("❌ Neznámy príkaz, použi: /pomoc", CHAT_ID_EMMKA)
        return f"❌ Unknown emmka's command ({command})"
    
    return "❌ Emmka's command not handled" # shouldnt happen


def main():
    last_update_id = None
    send_message("🤖 Bot is online. Send /help to see commands.", CHAT_ID_JA)
    while True:
        updates = get_updates(offset=last_update_id)
        for update in updates.get('result', []):
            last_update_id = update['update_id'] + 1
            msg = update.get('message')

            text = msg.get('text')
            if not text:
                continue

            username = msg['from'].get('username', 'unknown')
            chat_id = msg['chat']['id']
            log_message(username, chat_id, text)

            if str(chat_id) == str(CHAT_ID_JA):
                result = run_command(text.strip())

            elif str(chat_id) == str(CHAT_ID_EMMKA):
                result = run_command_emmka(text.strip())

            else:
                continue

            if result and len(result) > 4096:
                result = result[:4093] + "..."
            send_message(result, CHAT_ID_JA)

        time.sleep(1)

if __name__ == '__main__':
    main()
