import os, re, time, socket, requests, subprocess
from datetime import datetime

WEBHOOK_URL = "https://discord.com/api/webhooks/1385049626943557642/QiegCi7X00_Y18iGpapQ_b3eWac41LH6BhaPN9RnNwR_4JzLjNYBpoR1_1JcCAxlSrut"
DEVICE_ID = "STB-HG680P-01"
MINER_SH_PATH = "/root/ccminer/miner.sh"
LOG_PATH = "/root/ccminer/miner.log"

def get_ping(host="8.8.8.8"):
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", host], text=True)
        match = re.search(r'time=(\d+\.\d+) ms', output)
        if match:
            return f"{match.group(1)} ms"
        else:
            return "Timeout"
    except Exception as e:
        return "Error"
    
ping = get_ping("8.8.8.8")

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return f"{int(f.read()) / 1000:.1f}°C"
    except: return "N/A"

def get_cpu_load():
    try:
        with open("/proc/stat", "r") as f:
            line = f.readline()
        parts = [int(val) for val in line.split()[1:]]
        idle1 = parts[3]
        total1 = sum(parts)

        time.sleep(0.5)

        with open("/proc/stat", "r") as f:
            line = f.readline()
        parts = [int(val) for val in line.split()[1:]]
        idle2 = parts[3]
        total2 = sum(parts)

        idle_delta = idle2 - idle1
        total_delta = total2 - total1

        cpu_usage = 100.0 * (1.0 - idle_delta / total_delta)
        return f"{cpu_usage:.1f}%"
    except:
        return "N/A"


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except: return "Unknown"

def get_uptime():
    try:
        with open("/proc/uptime") as f:
            total = float(f.readline().split()[0])
        d, h = int(total // 86400), int(total % 86400 // 3600)
        m = int(total % 3600 // 60)
        return f"{d} days, {h} hours, {m} minutes"
    except: return "N/A"

def get_wallet_and_worker():
    try:
        with open(MINER_SH_PATH) as f:
            content = f.read()
        match = re.search(r"-u\s+['\"]?([\w]+)\.([\w]+)['\"]?", content)
        return match.groups() if match else ("UnknownWallet", "UnknownWorker")
    except: return ("Error", "Error")

def get_hashrate():
    try:
        with open(LOG_PATH) as f:
            for line in reversed(f.readlines()):
                if "accepted" in line and "kH/s" in line:
                    parts = line.strip().split(",")
                    if parts:
                        clean = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                        rate = clean.sub('', parts[-1]).replace("yes!", "").strip()
                        return rate
        return "N/A"
    except: return "N/A"

def get_pool():
    try:
        ansi_clean = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        with open("/root/ccminer/miner.log", "r") as f:
            for line in f:
                match = re.search(r"stratum\+tcp://[^\s]+", line)
                if match:
                    clean_pool = ansi_clean.sub('', match.group(0))
                    return clean_pool
        return "Not found"
    except:
        return "Error"


def get_timestamp():
    return datetime.now().strftime("%a, %d/%m/%Y at %I:%M %p")

def send_webhook():
    wallet, worker = get_wallet_and_worker()

    stats = (
        f"📊 **Stats**\n"
        f"🧠 CPU Load : `{get_cpu_load()}`\n"
        f"🌡️ CPU Temp : `{get_temp()}`\n"
        f"<a:baalpetir:1146069258116280490> HashRate : `{get_hashrate()}`\n"
        f"🌐 Running at IP : ||{get_local_ip()}||\n"
        f"<a:online:1270831642977767434> Ping : `{get_ping()}`"
    )

    pool_info = (
        f"🎯 **Pool**\n"
        f"<:Server_NyxCloud:1255935173246062602> Server : `{get_pool()}`\n"
        f"💳 Wallet : ||{wallet}||\n"
        f"🪪 Worker : `{worker}`"
    )

    uptime = f"⏱️ **Uptime:**\n`{get_uptime()}`"

    payload = {
    "embeds": [{
        "color": 15844367,
        "fields": [
            { "name": "<:banhammer3:1346683070597824604> **MonMining**", "value": "Supervised Mining System\n\u200B", "inline": False },
            { "name": "<:Emulator:1340504951037759601> Device ID", "value": f"`{DEVICE_ID}`", "inline": False },
            { "name": "\u200B", "value": stats, "inline": False },
            { "name": "\u200B", "value": pool_info, "inline": False },
            { "name": "\u200B", "value": uptime, "inline": False }
        ],
        "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/1072128152106704936/1333794066013622362/20250128_203906.png"
        },
        "image": {
            "url": "https://cdn.discordapp.com/attachments/1072128152106704936/1333794065572954254/20250128_204046.png"
        },
        "footer": {
            "text": f"{get_timestamp()} | SuperScript by SuperMon"
        }
    }]
}


    try:
        requests.post(WEBHOOK_URL, json=payload)
        print("✅ Webhook sent.")
    except Exception as e:
        print("❌ Failed to send webhook:", e)

# === RUN LOOP ===
if __name__ == "__main__":
    while True:
        send_webhook()
        time.sleep(600)
