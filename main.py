import requests
import os
import json
import schedule
import time

# Fungsi untuk mengirim pesan ke Telegram
def send_to_telegram(message, bot_token, chat_id):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"  # Gunakan HTML untuk format pesan
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
    # Konfigurasi Telegram
    BOT_TOKEN = "5899849808:AAEubX8DW-g4KVsIRj4osnzvGV0owwMEuQU"  # Ganti dengan token bot Anda
    CHAT_ID = "-1002365305736"  # Ganti dengan ID channel Anda

    # Mendapatkan daftar buku dari API
    books = get_books()
    if not books:
        print("Daftar buku tidak ditemukan. Program dihentikan.")
        return

    # Membaca data terakhir dari file, atau mengatur ke default
    if os.path.exists("last_id.json"):
        try:
            with open("last_id.json", "r") as file:
                last_data = json.load(file)
                current_book = last_data.get("current_book", books[0]["id"])
                last_id = last_data.get("last_id", 1)
        except json.JSONDecodeError:
            print("Error: Format file last_id.json tidak valid. Mengatur ulang ke default.")
            current_book = books[0]["id"]
            last_id = 1
    else:
        current_book = books[0]["id"]
        last_id = 1

    # Mencari buku saat ini dalam daftar buku
    book_info = next((book for book in books if book["id"] == current_book), None)
    if not book_info:
        print(f"Buku '{current_book}' tidak ditemukan. Mengatur ulang ke buku pertama.")
        book_info = books[0]
        current_book = book_info["id"]
        last_id = 1

    # Membuat URL endpoint dinamis
    url = f"https://api.hadith.gading.dev/books/{current_book}/{last_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if not data.get("data"):
            print(f"Data tidak ditemukan untuk ID {last_id} di buku '{current_book}'.")
        else:
            arab_text = data["data"]["contents"]["arab"]
            indonesian_translation = data["data"]["contents"]["id"]
            name = data["data"]["name"]
            hadith_number = data["data"]["contents"]["number"]

            # Membuat pesan untuk Telegram
            message = f"""
<b>Hadits Hari Ini</b>
<b>Kitab:</b> {name}
<b>Nomor Hadits:</b> {hadith_number}

<b>Bahasa Arab:</b>
{arab_text}

<b>Terjemahan:</b>
{indonesian_translation}

<b>Support kami dsini:</b>
<a href="https://linktr.ee/shariputdin">Klik di sini</a>
"""
            send_to_telegram(message, BOT_TOKEN, CHAT_ID)

        # Menambahkan ID berikutnya
        last_id += 1

        # Jika ID melebihi jumlah hadits tersedia, ganti buku
        if last_id > book_info["available"]:
            current_index = books.index(book_info)
            next_index = (current_index + 1) % len(books)
            current_book = books[next_index]["id"]
            last_id = 1  # Reset ke 1 untuk buku berikutnya
            print(f"Berpindah ke buku berikutnya: {books[next_index]['name']}")

        # Menyimpan data terbaru
        with open("last_id.json", "w") as file:
            json.dump({"current_book": current_book, "last_id": last_id}, file)
    else:
        print(f"Error: {response.status_code}. Mengatur ulang ke buku pertama.")
        with open("last_id.json", "w") as file:
            json.dump({"current_book": books[0]["id"], "last_id": 1}, file)

# Menjadwalkan script agar berjalan pada jam 12:30, 18:00, dan 04:00
schedule.every().day.at("12:30").do(get_hadith)
schedule.every().day.at("18:00").do(get_hadith)
schedule.every().day.at("04:00").do(get_hadith)

print("Scheduler berjalan. Program akan mengirim hadits pada jam 12:30, 18:00, dan 04:00.")

# Looping untuk menjalankan jadwal
while True:
    schedule.run_pending()
    time.sleep(1)  # Menunggu 1 detik sebelum mengecek kembali
