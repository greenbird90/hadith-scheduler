import requests
import os
import json

# Fungsi untuk menyimpan last_id.json dengan debug
def save_last_id(current_book, last_id):
    data = {"current_book": current_book, "last_id": last_id}
    print(f"🔥 Menyimpan last_id.json dengan data: {data}")  # 🔍 Debugging
    with open("last_id.json", "w") as file:
        json.dump(data, file)

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
            print(f"📂 last_id.json ditemukan: {last_data}")  # 🔍 Debugging
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

        save_last_id(current_book, last_id)  # 🔥 Gunakan fungsi debug di sini
    else:
        print(f"Error: {response.status_code}, reset ke awal.")
        save_last_id(books[0]["id"], 1)

if __name__ == "__main__":
    get_hadith()
