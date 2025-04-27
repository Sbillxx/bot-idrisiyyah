# Bot Telegram Tarekat Idrisiyyah

Bot informasi untuk menjawab pertanyaan-pertanyaan seputar Tarekat Idrisiyyah. Bot ini menyediakan informasi terstruktur dalam bentuk Q&A (Question and Answer) yang dikelompokkan dalam beberapa kategori.

## 🌟 Fitur

### Fitur Umum
- Menu Q&A terstruktur dengan 4 kategori:
  - 📖 Kemuridan
  - 🕌 Fiqih
  - 🧘 Tassawuf
  - 👨‍👩‍👧‍👦 Keluarga
- 🙌 Panduan penggunaan bot
- 🆘 Menu bantuan
- Interface yang user-friendly dengan tombol inline
- Pesan otomatis untuk chat di luar menu

### Fitur Admin
- 🔐 Sistem login admin
- ⚙️ Manajemen Q&A:
  - Tambah pertanyaan dan jawaban
  - Edit pertanyaan dan jawaban
  - Hapus pertanyaan
- 📝 Pengaturan konten:
  - Update panduan
  - Update bantuan
- 👤 Manajemen akun:
  - Ganti username
  - Ganti password
- ⏳ Timeout sesi (5 menit)

## 🛠️ Teknologi

- Python 3.x
- python-telegram-bot
- MySQL Database
- python-dotenv

## ⚙️ Konfigurasi

1. Buat file `.env` di root direktori dengan isi:
```env
BOT_TOKEN=your_telegram_bot_token
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```

2. Struktur database yang dibutuhkan:
```sql
-- Tabel admin
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(255)
);

-- Tabel QnA untuk setiap kategori
CREATE TABLE Qna_kemuridan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    answer TEXT
);

CREATE TABLE Qna_fiqih (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    answer TEXT
);

CREATE TABLE Qna_tassawuf (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    answer TEXT
);

CREATE TABLE Qna_keluarga (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT,
    answer TEXT
);

-- Tabel panduan dan bantuan
CREATE TABLE panduan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keterangan TEXT
);

CREATE TABLE bantuan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keterangan TEXT
);
```

## 🚀 Instalasi

1. Clone repository:
```bash
git clone [url-repository]
cd [nama-folder]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan bot:
```bash
python chatbot.py
```

## 📱 Penggunaan

### User
1. Mulai bot dengan command `/start`
2. Akses menu Q&A dengan command `/tanyajawab`
3. Pilih kategori yang diinginkan
4. Pilih pertanyaan untuk melihat jawaban

### Admin
1. Akses panel admin dengan command `/admin`
2. Login menggunakan username dan password
3. Kelola konten melalui menu admin yang tersedia
4. Sesi admin akan timeout setelah 5 menit tidak aktif

## ⚠️ Penting

- Bot hanya menerima interaksi melalui menu yang tersedia
- Pesan teks langsung akan direspon dengan arahan ke menu yang tersedia
- Pastikan database selalu tersedia dan terkoneksi
- Backup database secara berkala

## 👥 Kontribusi

Jika Anda ingin berkontribusi pada pengembangan bot ini:
1. Fork repository
2. Buat branch baru
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## 📝 Lisensi

[Sesuaikan dengan lisensi yang digunakan]

## 📞 Kontak

ibnusidik.ali@gmail.com

