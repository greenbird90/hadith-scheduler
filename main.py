import requests
import os
import json

# Fungsi untuk mengirim pesan ke Telegram
def send_to_telegram(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Pesan berhasil dikirim ke Telegram.")
    else:
        print(f"Error mengirim pesan ke Telegram: {response.status_code}, {response.text}")

# Fungsi untuk mengambil daftar buku dari API
def get_books():
    url = "https://api.hadith.gading.dev/books"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error: Tidak dapat mengambil daftar buku. Status: {response.status_code}")
        return []

# Fungsi untuk mengambil dan menampilkan hadits
def get_hadith():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    if not BOT_TOKEN or not CHAT_ID:
        print("BOT_TOKEN atau CHAT_ID tidak ditemukan. Pastikan sudah diatur di environment variables.")
        return

    books = get_books()
    if not books:
        print("Daftar buku tidak ditemukan. Program dihentikan.")
        return

    # Membaca data terakhir dari file
    last_id, current_book = 1, books[0]["id"]
    if os.path.exists("last_id.json"):
        try:
            with open("last_id.json", "r") as file:
                last_data = json.load(file)
                current_book = last_data.get("current_book", current_book)
                last_id = last_data.get("last_id", 1)
        except json.JSONDecodeError:
            print("Error membaca file last_id.json, reset ke default.")

    book_info = next((book for book in books if book["id"] == current_book), None)
    if not book_info:
        book_info = books[0]
        current_book = book_info["id"]
        last_id = 1

    url = f"https://api.hadith.gading.dev/books/{current_book}/{last_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            message = f"""
<b>Hadits Hari Ini</b>
<b>Kitab:</b> {data["data"]["name"]}
<b>Nomor Hadits:</b> {data["data"]["contents"]["number"]}

<b>Bahasa Arab:</b>
{data["data"]["contents"]["arab"]}

<b>Terjemahan:</b>
{data["data"]["contents"]["id"]}

<b>Support kami dengan sebarkan hadist & channel ini:</b>
"""
            send_to_telegram(message, BOT_TOKEN, CHAT_ID)

        last_id += 1
        if last_id > book_info["available"]:
            current_index = books.index(book_info)
            next_index = (current_index + 1) % len(books)
            current_book = books[next_index]["id"]
            last_id = 1

        with open("last_id.json", "w") as file:
            json.dump({"current_book": current_book, "last_id": last_id}, file)
    else:
        print(f"Error: {response.status_code}, reset ke awal.")
        with open("last_id.json", "w") as file:
            json.dump({"current_book": books[0]["id"], "last_id": 1}, file)

if __name__ == "__main__":
    get_hadith()
