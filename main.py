import os
import requests
from datetime import datetime, timedelta
import pytz

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

tz = pytz.timezone('Asia/Ho_Chi_Minh')

# 🕒 Danh sách boss (field + raid)
boss_cycle_schedule = {
    # Field Boss
    "Bluemen II": {"start": "2025-05-08 00:30", "cycle_hours": 12},
    "Betalanse II": {"start": "2025-05-08 02:30", "cycle_hours": 12},
    "Cryo II": {"start": "2025-05-08 04:30", "cycle_hours": 12},
    "Sporelex II": {"start": "2025-05-08 06:30", "cycle_hours": 12},
    "Toxspore II": {"start": "2025-05-08 08:30", "cycle_hours": 12},
    "Bristol II": {"start": "2025-05-08 10:30", "cycle_hours": 12},
    "Veilian II": {"start": "2025-05-08 12:30", "cycle_hours": 12},
    "Arque II": {"start": "2025-05-08 14:30", "cycle_hours": 12},
    "Rootrus II": {"start": "2025-05-08 16:30", "cycle_hours": 12},
    "Sapphire Blade II": {"start": "2025-05-08 06:30", "cycle_hours": 12},
    "Coralisk II": {"start": "2025-05-08 08:30", "cycle_hours": 12},
    "Breeze II": {"start": "2025-05-08 10:30", "cycle_hours": 12},
    "Rootrus I": {"start": "2025-05-08 16:40", "cycle_hours": 10},
    "Sapphire Blade I": {"start": "2025-05-11 5:45", "cycle_hours": 10},
    "Coralisk I": {"start": "2025-05-10 14:50", "cycle_hours": 12},
    "Betalanse I": {"start": "2025-05-21 17:05", "cycle_hours": 2},
    "Blumen I": {"start": "2025-06-13 12:00", "cycle_hours": 2},
    "Cryo I": {"start": "2025-06-13 14:10", "cycle_hours": 4},
    "Sporelex I": {"start": "2025-06-13 11:15", "cycle_hours": 4},
    "Toxspore I": {"start": "2025-06-13 14:20", "cycle_hours": 6},
    "Bristol I": {"start": "2025-06-13 15:25", "cycle_hours": 6},
    "Veilian I": {"start": "2025-06-13 13:30", "cycle_hours": 8},
    "Arque I": {"start": "2025-06-13 15:35", "cycle_hours": 8},
    "Breeze I": {"start": "2025-06-13 15:55", "cycle_hours": 12},

    # RAID Boss (gộp AM + PM, chu kỳ 12h)
    "Pierror Raid": {"start": "2025-05-08 07:00", "cycle_hours": 12, "type": "raid"},
}

def send_alert(boss, spawn_time):
    message = {
        "content": f"⚠️ Boss **{boss}** sẽ xuất hiện lúc {spawn_time.strftime('%H:%M')}! Chuẩn bị nào!"
    }
    response = requests.post(WEBHOOK_URL, json=message)
    if response.status_code == 204:
        print(f"✅ Đã gửi cảnh báo cho {boss}")
    else:
        print(f"❌ Lỗi khi gửi webhook: {response.text}")

def check_boss():
    now = datetime.now(tz)
    for boss, info in boss_cycle_schedule.items():
        try:
            start = tz.localize(datetime.strptime(info["start"], "%Y-%m-%d %H:%M"))
            cycle = timedelta(hours=info["cycle_hours"])
            elapsed = max(0, int((now - start).total_seconds() // cycle.total_seconds()))
            spawn_time = start + elapsed * cycle
            if spawn_time + timedelta(minutes=5) < now:
                spawn_time += cycle
            warning_time = spawn_time - timedelta(minutes=5)
            if abs((now - warning_time).total_seconds()) <= 180:  # +-3 phút
                send_alert(boss, spawn_time)
        except Exception as e:
            print(f"Lỗi với boss {boss}: {e}")

if __name__ == "__main__":
    check_boss()