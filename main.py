import requests
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()  # Load .env if running locally

# ===🔹 Setup Google Sheets Access ===
def get_gsheet_client():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# ===🔹 Baca last_id dari Google Sheet ===
def read_last_id(sheet):
    try:
        data = sheet.get_all_records()
        if data:
            return data[0].get("current_book"), int(data[0].get("last_id"))
    except Exception as e:
        print(f"❌ Gagal membaca Google Sheet: {e}")
    return None, 1

# ===🔹 Simpan last_id ke Google Sheet ===
def write_last_id(sheet, current_book, last_id):
    try:
        sheet.update('A2', [[current_book, last_id]])
        print(f"✅ Google Sheet diperbarui: {current_book}, Hadits ke-{last_id}")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke Google Sheet: {e}")

# ===🔹 Kirim pesan ke Telegram ===
def send_to_telegram(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Pesan berhasil dikirim ke Telegram.")
    else:
        print(f"❌ Error kirim ke Telegram: {response.status_code}, {response.text}")

# ===🔹 Ambil daftar kitab dari API ===
def get_books():
    url = "https://api.hadith.gading.dev/books"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"❌ Gagal ambil daftar kitab. Status: {response.status_code}")
        return []

# ===🔹 Fungsi utama ===
def get_hadith():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    if not BOT_TOKEN or not CHAT_ID:
        print("❌ BOT_TOKEN atau CHAT_ID belum diset di environment.")
        return

    books = get_books()
    if not books:
        return

    # 🔹 Akses Google Sheet
    client = get_gsheet_client()
    sheet = client.open("HadithData").sheet1

    # 🔹 Baca dari Google Sheet
    current_book, last_id = read_last_id(sheet)
    if not current_book:
        current_book = books[0]["id"]
        last_id = 1
        write_last_id(sheet, current_book, last_id)

    print(f"📌 Kitab: {current_book}, Hadits ke-{last_id}")

    # 🔹 Ambil hadits dari API
    url = f"https://api.hadith.gading.dev/books/{current_book}/{last_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            hadith = data["data"]["contents"]
            message = f"""
<b>📖 Hadits Hari Ini</b>
<b>📚 Kitab:</b> {data["data"]["name"]}
<b>🔢 Nomor Hadits:</b> {hadith["number"]}

<b>🕌 Bahasa Arab:</b>
{hadith["arab"]}

<b>📜 Terjemahan:</b>
{hadith["id"]}

<b>🤲 Dukung & sebarkan channel ini.</b>
"""
            send_to_telegram(message, BOT_TOKEN, CHAT_ID)

        # 🔹 Update indeks hadits
        book_info = next((b for b in books if b["id"] == current_book), books[0])
        last_id += 1
        if last_id > book_info["available"]:
            current_index = books.index(book_info)
            current_book = books[(current_index + 1) % len(books)]["id"]
            last_id = 1

        write_last_id(sheet, current_book, last_id)
    else:
        print(f"❌ API Error: {response.status_code}")
        write_last_id(sheet, books[0]["id"], 1)

# ===🔹 Eksekusi utama ===
if __name__ == "__main__":
    get_hadith()
