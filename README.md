# Hadith Telegram Bot

## 📌 Deskripsi
Bot ini secara otomatis mengirimkan hadits harian ke grup atau channel Telegram berdasarkan koleksi hadits dari API [Hadith Gading](https://api.hadith.gading.dev). Bot akan menyimpan riwayat hadits yang telah dikirim dan melanjutkan dari hadits terakhir setiap kali dijalankan. berikut adalah channel telegram kami (**REMINDER HADIST HARIAN**: [https://t.me/dailyhadistrm](#)), silahkan join dan sebarkan untuk kaum muslimin

## 🚀 Fitur
- 📖 Mengambil hadits dari berbagai kitab
- 📤 Mengirim hadits secara otomatis ke Telegram
- 📝 Menyimpan riwayat hadits terakhir agar tidak duplikasi
- 🔄 Berpindah ke kitab berikutnya setelah semua hadits dalam satu kitab terkirim

## 🛠 Instalasi
### 1️⃣ Clone Repository
```sh
git clone https://github.com/username/repository.git
cd repository
```

### 2️⃣ Install Dependencies
Pastikan Anda memiliki **Python 3.x** terinstal, lalu jalankan:
```sh
pip install -r requirements.txt
```

### 3️⃣ Konfigurasi Environment
Buat file `.env` dan tambahkan variabel berikut:
```env
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

### 4️⃣ Jalankan Bot
```sh
python bot.py
```

## 🔧 Cara Kerja
1. **Mengambil daftar kitab hadits** dari API.
2. **Membaca riwayat hadits terakhir** dari `last_id.json`.
3. **Mengambil hadits terbaru** dari API berdasarkan kitab dan nomor hadits.
4. **Mengirim hadits ke Telegram** dalam format HTML.
5. **Menyimpan progres hadits terakhir** untuk menghindari duplikasi.
6. **Melanjutkan ke kitab berikutnya** setelah kitab saat ini selesai.

## 📜 Lisensi
MIT License - Hak cipta (c) 2025 SARIPUDIN SAHARDI

## 🤝 Kontribusi
Pull request sangat diterima! Jika Anda menemukan bug atau ingin menambahkan fitur baru, silakan buat issue atau kirim PR.

## 💰 Donasi
Jika Anda ingin mendukung proyek ini, silakan berdonasi melalui e-wallet berikut:
- **BCA**: 4731953001 a/n Saripudin
- **BSI**: 7139446927 a/n Saripudin

## 📬 Kontak
Untuk pertanyaan atau saran, hubungi saya di [saripudinsahardi@gmail.com](mailto:saripudinsahardi@gmail.com).
