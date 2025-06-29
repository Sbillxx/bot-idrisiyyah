import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import asyncio
import time
import mysql.connector
import logging
from flask import Flask, request

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")



# Konfigurasi database menggunakan environment variables


# def get_db_connection():
#     return mysql.connector.connect(**DB_CONFIG)
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),
        charset="utf8mb4"
    )
    cursor = conn.cursor()
    cursor.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci")
    return conn


logging.getLogger('telegram.ext.conversationhandler').setLevel(logging.ERROR)

async def start(update: Update, context):
    user = update.message.from_user
    await update.message.reply_text(f"Halo {user.first_name}! Klik /tanyajawab untuk mulai.")

# Handler untuk command /tanyajawab (dari chat)
async def tanyajawab_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 Qna Kemuridan", callback_data="qna_kemuridan")],
        [InlineKeyboardButton("🕌 Qna Fiqih", callback_data="qna_fiqih")],
        [InlineKeyboardButton("🧘 Qna Tassawuf", callback_data="qna_tassawuf")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 Qna Keluarga", callback_data="qna_keluarga")],
        [InlineKeyboardButton("🙌 Panduan", callback_data="panduan")],
        [InlineKeyboardButton("🆘 Bantuan", callback_data="bantuan")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Silakan pilih kategori:", reply_markup=reply_markup)

# Handler untuk callback "tanyajawab" (dari tombol kembali)
async def tanyajawab_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("📖 Qna Kemuridan", callback_data="qna_kemuridan")],
        [InlineKeyboardButton("🕌 Qna Fiqih", callback_data="qna_fiqih")],
        [InlineKeyboardButton("🧘 Qna Tassawuf", callback_data="qna_tassawuf")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 Qna Keluarga", callback_data="qna_keluarga")],
        [InlineKeyboardButton("🙌 Panduan", callback_data="panduan")],
        [InlineKeyboardButton("🆘 Bantuan", callback_data="bantuan")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text("Silakan pilih kategori:", reply_markup=reply_markup)


# async def tanyajawab_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("📖 Qna Kemuridan", callback_data="Qna_kemuridan")],
#         [InlineKeyboardButton("🕌 Qna Fiqih", callback_data="Qna_fiqih")],
#         [InlineKeyboardButton("🧘 Qna Tassawuf", callback_data="Qna_tassawuf")],
#         [InlineKeyboardButton("👨‍👩‍👧‍👦 Qna Keluarga", callback_data="Qna_keluarga")],
#         [InlineKeyboardButton("🙌 Panduan", callback_data="panduan")],
#         [InlineKeyboardButton("🆘 Bantuan", callback_data="bantuan")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text("Silakan pilih kategori:", reply_markup=reply_markup)

# # Fungsi untuk menangani callback dari inline keyboard
# async def tanyajawab_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()

#     keyboard = [
#         [InlineKeyboardButton("📖 Qna Kemuridan", callback_data="Qna_kemuridan")],
#         [InlineKeyboardButton("🕌 Qna Fiqih", callback_data="Qna_fiqih")],
#         [InlineKeyboardButton("🧘 Qna Tassawuf", callback_data="Qna_tassawuf")],
#         [InlineKeyboardButton("👨‍👩‍👧‍👦 Qna Keluarga", callback_data="Qna_keluarga")],
#         [InlineKeyboardButton("🙌 Panduan", callback_data="panduan")],
#         [InlineKeyboardButton("🆘 Bantuan", callback_data="bantuan")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await query.message.edit_text("Silakan pilih kategori:", reply_markup=reply_markup)


# qna option ------------------------------------

async def qna_kemuridan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_kemuridan")
    qna_list = cursor.fetchall()
    conn.close()
    
    if not qna_list:
        await update.callback_query.message.edit_text("Belum ada data dalam kategori ini.")
        return
    
    keyboard = [[InlineKeyboardButton(q, callback_data=f"kemuridan_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="tanyajawab")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Pilih pertanyaan:", reply_markup=reply_markup)

async def qna_fiqih(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_fiqih")
    qna_list = cursor.fetchall()
    conn.close()
    
    if not qna_list:
        await update.callback_query.message.edit_text("Belum ada data dalam kategori ini.")
        return
    
    keyboard = [[InlineKeyboardButton(q, callback_data=f"fiqih_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="tanyajawab")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Pilih pertanyaan:", reply_markup=reply_markup)

async def qna_tassawuf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_tassawuf")
    qna_list = cursor.fetchall()
    conn.close()
    
    if not qna_list:
        await update.callback_query.message.edit_text("Belum ada data dalam kategori ini.")
        return
    
    # Membuat tombol dengan daftar pertanyaan
    keyboard = [[InlineKeyboardButton(q, callback_data=f"tassawuf_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="tanyajawab")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.message.edit_text("Pilih pertanyaan:", reply_markup=reply_markup)

async def qna_keluarga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_keluarga")
    qna_list = cursor.fetchall()
    conn.close()
    
    if not qna_list:
        await update.callback_query.message.edit_text("Belum ada data dalam kategori ini.")
        return
    
    # Membuat tombol dengan daftar pertanyaan
    keyboard = [[InlineKeyboardButton(q, callback_data=f"keluarga_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="tanyajawab")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.message.edit_text("Pilih pertanyaan:", reply_markup=reply_markup)

async def panduan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keterangan FROM panduan LIMIT 1")
    panduan = cursor.fetchone()
    conn.close()

    if panduan:
        response = f"📌 *Panduan:*\n\n{panduan[0]}"
    else:
        response = "Belum ada panduan yang tersedia."

    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="tanyajawab")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(response, reply_markup=reply_markup, parse_mode="Markdown")

async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keterangan FROM bantuan LIMIT 1")
    bantuan = cursor.fetchone()
    conn.close()

    if bantuan:
        response = f"🆘 *Bantuan:*\n\n{bantuan[0]}"
    else:
        response = "Belum ada informasi bantuan yang tersedia."

    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="tanyajawab")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(response, reply_markup=reply_markup, parse_mode="Markdown")

# admin --------------------------------

USERNAME, PASSWORD, INPUT_QUESTION, INPUT_ANSWER, EDIT_QUESTION, EDIT_ANSWER, INPUT_NEW_PASSWORD, INPUT_NEW_USERNAME, INPUT_NEW_PANDUAN, INPUT_NEW_BANTUAN = range(10)
SESSION_TIMEOUT = 300  # 5 menit timeout jika tidak ada aktivitas

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Silakan masukkan username:")
    return USERNAME

async def username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['username'] = update.message.text
    await update.message.reply_text("Silakan masukkan password:")
    return PASSWORD

async def password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password_input = update.message.text
    username_input = context.user_data.get('username')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin_users WHERE username = %s AND password = %s", 
                  (username_input, password_input))
    user = cursor.fetchone()
    conn.close()

    if user:
        context.user_data['admin_logged_in'] = True
        context.user_data['username'] = username_input

        # Mulai timeout sesi
        await refresh_session_timeout(update, context)

        await update.message.reply_text("✅ Login berhasil! Selamat datang di Admin Panel.")
        await admin_panel(update, context)
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Username atau password salah. Silakan coba lagi dengan /admin.")
        return ConversationHandler.END

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Refresh timeout setiap kali mengakses panel admin
    await refresh_session_timeout(update, context)
    
    query = update.callback_query

    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message

    if not context.user_data.get('admin_logged_in'):
        await message.reply_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin.")
        return

    # Update keyboard dengan menambahkan tombol Option
    keyboard = [
        [InlineKeyboardButton("📜 Daftar QnA", callback_data="admin_qna_list")],
        [InlineKeyboardButton("➕ Tambah QnA", callback_data="admin_qna_add")],
        [InlineKeyboardButton("⚙️ Option", callback_data="admin_option")],
        [InlineKeyboardButton("🚪 Logout", callback_data="admin_logout")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query:
        await message.edit_text("🔧 *Admin Panel*\nSilakan pilih menu:", 
                                reply_markup=reply_markup, 
                                parse_mode="Markdown")
    else:
        await message.reply_text("🔧 *Admin Panel*\nSilakan pilih menu:", 
                                 reply_markup=reply_markup, 
                                 parse_mode="Markdown")

# Tambahkan fungsi untuk menangani menu option
async def admin_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("👤 Ganti Username", callback_data="change_username")],
        [InlineKeyboardButton("🔑 Ganti Password", callback_data="change_password")],
        [InlineKeyboardButton("📖 Ganti Panduan", callback_data="change_panduan")],
        [InlineKeyboardButton("❓ Ganti Bantuan", callback_data="change_bantuan")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="admin_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "⚙️ *Option Menu*\n"
        "Silakan pilih menu pengaturan:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Tambahkan fungsi untuk menangani ganti username
async def change_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.message.edit_text(
        "👤 *Ganti Username*\n\n"
        "Silakan ketik username baru Anda:",
        parse_mode="Markdown"
    )
    return INPUT_NEW_USERNAME

async def receive_new_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_username = update.message.text
    old_username = context.user_data.get('username')
    
    # Update username di database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah username baru sudah digunakan
    cursor.execute("SELECT * FROM admin_users WHERE username = %s", (new_username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_option")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "❌ *Gagal!*\n\n"
            "Username sudah digunakan. Silakan pilih username lain.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    
    # Update username jika belum digunakan
    cursor.execute("UPDATE admin_users SET username = %s WHERE username = %s", 
                  (new_username, old_username))
    conn.commit()
    conn.close()
    
    # Update username di context
    context.user_data['username'] = new_username
    
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Berhasil!*\n\n"
        "Username telah diperbarui.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# Tambahkan fungsi untuk menangani ganti password
async def change_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.message.edit_text(
        "🔑 *Ganti Password*\n\n"
        "Silakan ketik password baru Anda:",
        parse_mode="Markdown"
    )
    return INPUT_NEW_PASSWORD

async def receive_new_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_password = update.message.text
    username = context.user_data.get('username')
    
    if len(new_password) < 6:  # Tambahkan validasi minimal panjang password
        keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_option")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "❌ *Gagal!*\n\n"
            "Password harus minimal 6 karakter.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return ConversationHandler.END
    
    # Update password di database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE admin_users SET password = %s WHERE username = %s", 
                  (new_password, username))
    conn.commit()
    conn.close()
    
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Berhasil!*\n\n"
        "Password telah diperbarui.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# Tambahkan fungsi untuk menangani ganti panduan
async def change_panduan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Ambil panduan saat ini
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keterangan FROM panduan LIMIT 1")
    current_panduan = cursor.fetchone()
    conn.close()
    
    current_text = current_panduan[0] if current_panduan else "Belum ada panduan"
    
    await query.message.edit_text(
        "📖 *Ganti Panduan*\n\n"
        f"Panduan saat ini:\n{current_text}\n\n"
        "Silakan ketik panduan baru:",
        parse_mode="Markdown"
    )
    return INPUT_NEW_PANDUAN

async def receive_new_panduan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_panduan = update.message.text
    
    # Update panduan di database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah sudah ada panduan
    cursor.execute("SELECT COUNT(*) FROM panduan")
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("UPDATE panduan SET keterangan = %s", (new_panduan,))
    else:
        cursor.execute("INSERT INTO panduan (keterangan) VALUES (%s)", (new_panduan,))
    
    conn.commit()
    conn.close()
    
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_option")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Berhasil!*\n\n"
        "Panduan telah diperbarui.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# Tambahkan fungsi untuk menangani ganti bantuan
async def change_bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Ambil bantuan saat ini
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keterangan FROM bantuan LIMIT 1")
    current_bantuan = cursor.fetchone()
    conn.close()
    
    current_text = current_bantuan[0] if current_bantuan else "Belum ada bantuan"
    
    await query.message.edit_text(
        "❓ *Ganti Bantuan*\n\n"
        f"Bantuan saat ini:\n{current_text}\n\n"
        "Silakan ketik bantuan baru:",
        parse_mode="Markdown"
    )
    return INPUT_NEW_BANTUAN

async def receive_new_bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_bantuan = update.message.text
    
    # Update bantuan di database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah sudah ada bantuan
    cursor.execute("SELECT COUNT(*) FROM bantuan")
    count = cursor.fetchone()[0]
    
    if count > 0:
        cursor.execute("UPDATE bantuan SET keterangan = %s", (new_bantuan,))
    else:
        cursor.execute("INSERT INTO bantuan (keterangan) VALUES (%s)", (new_bantuan,))
    
    conn.commit()
    conn.close()
    
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_option")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Berhasil!*\n\n"
        "Bantuan telah diperbarui.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# admin qna ----------------------


async def admin_qna_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("📖 Qna Kemuridan", callback_data="admin_qna_kemuridan")],
        [InlineKeyboardButton("🕌 Qna Fiqih", callback_data="admin_qna_fiqih")],
        [InlineKeyboardButton("🧘 Qna Tassawuf", callback_data="admin_qna_tassawuf")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 Qna Keluarga", callback_data="admin_qna_keluarga")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="admin_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text("📜 *Daftar QnA* Silakan pilih kategori:", reply_markup=reply_markup, parse_mode="Markdown")

async def admin_qna_kemuridan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tambahkan refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Cek status login
    if not context.user_data.get('admin_logged_in'):
        await query.message.edit_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_kemuridan")
    qna_list = cursor.fetchall()
    conn.close()

    if not qna_list:
        await query.message.edit_text("Belum ada data dalam kategori ini.", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")]]))
        return

    keyboard = [[InlineKeyboardButton(q, callback_data=f"admin_qna_detail_kemuridan_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("📖 *QnA Kemuridan*\nPilih pertanyaan untuk dikelola:", 
                                  reply_markup=reply_markup, 
                                  parse_mode="Markdown")

async def admin_qna_fiqih(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tambahkan refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Cek status login
    if not context.user_data.get('admin_logged_in'):
        await query.message.edit_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_fiqih")
    qna_list = cursor.fetchall()
    conn.close()

    if not qna_list:
        await query.message.edit_text("Belum ada data dalam kategori ini.", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")]]))
        return

    keyboard = [[InlineKeyboardButton(q, callback_data=f"admin_qna_detail_fiqih_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("📖 *QnA Fiqih*\nPilih pertanyaan untuk dikelola:", 
                                  reply_markup=reply_markup, 
                                  parse_mode="Markdown")

    # print(f"Callback query diterima: {query.data}")

async def admin_qna_tassawuf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tambahkan refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Cek status login
    if not context.user_data.get('admin_logged_in'):
        await query.message.edit_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_tassawuf")
    qna_list = cursor.fetchall()
    conn.close()

    if not qna_list:
        await query.message.edit_text("Belum ada data dalam kategori ini.", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")]]))
        return

    keyboard = [[InlineKeyboardButton(q, callback_data=f"admin_qna_detail_tassawuf_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("📜 *QnA Tassawuf*\nPilih pertanyaan untuk dikelola:", 
                                  reply_markup=reply_markup, 
                                  parse_mode="Markdown")

async def admin_qna_keluarga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tambahkan refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Cek status login
    if not context.user_data.get('admin_logged_in'):
        await query.message.edit_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, question FROM qna_keluarga")
    qna_list = cursor.fetchall()
    conn.close()

    if not qna_list:
        await query.message.edit_text("Belum ada data dalam kategori ini.", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")]]))
        return

    keyboard = [[InlineKeyboardButton(q, callback_data=f"admin_qna_detail_keluarga_{id}")] for id, q in qna_list]
    keyboard.append([InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("📜 *QnA Keluarga*\nPilih pertanyaan untuk dikelola:", 
                                  reply_markup=reply_markup, 
                                  parse_mode="Markdown")


async def refresh_session_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('admin_logged_in'):
        # Batalkan timeout yang sedang berjalan jika ada
        if 'timeout_task' in context.user_data:
            context.user_data['timeout_task'].cancel()
        
        # Buat timeout baru
        context.user_data['session_start'] = time.time()
        context.user_data['timeout_task'] = asyncio.create_task(
            session_timeout(update, context)
        )

async def session_timeout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await asyncio.sleep(SESSION_TIMEOUT)
        if 'admin_logged_in' in context.user_data:
            # Hapus semua data sesi
            context.user_data.clear()
            await update.message.reply_text(
                "⏳ Sesi admin telah berakhir karena tidak ada aktivitas.\n"
                "Silakan login kembali dengan /admin"
            )
            await asyncio.sleep(2)
            await tanyajawab_command(update, context)
    except asyncio.CancelledError:
        # Task dibatalkan karena ada aktivitas baru
        pass

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Hapus sesi admin
    context.user_data.clear()

    await query.message.edit_text("Anda telah logout.")

    # Kembali ke menu Tanya Jawab
    await tanyajawab_callback(update, context)


async def qna_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Parse data callback
    data_parts = query.data.split("_")
    if len(data_parts) >= 4 and data_parts[0] == "admin":  # Handle admin detail view
        category = data_parts[3]  # kemuridan/fiqih/tassawuf/keluarga
        qna_id = data_parts[4]    # id pertanyaan
    else:  # Handle user detail view
        category = data_parts[0]
        qna_id = data_parts[1]

    # Tentukan nama tabel berdasarkan kategori
    table_mapping = {
        "kemuridan": "qna_kemuridan",
        "fiqih": "qna_fiqih",
        "tassawuf": "qna_tassawuf",
        "keluarga": "qna_keluarga"
    }
    
    table_name = table_mapping.get(category)
    if not table_name:
        await query.message.edit_text("Kategori tidak ditemukan.")
        return

    # Ambil data dari database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT question, answer FROM {table_name} WHERE id = %s", (qna_id,))
    qna = cursor.fetchone()
    conn.close()

    if qna:
        response = f"*Pertanyaan:*\n{qna[0]}\n\n*Jawaban:*\n{qna[1]}"
        
        # Tambahkan tombol hapus untuk admin view
        if data_parts[0] == "admin":
            keyboard = [
                [InlineKeyboardButton("🗑️ Hapus", callback_data=f"delete_{category}_{qna_id}")],
                [InlineKeyboardButton("⬅️ Kembali", callback_data=f"admin_qna_{category}")]
            ]
        else:
            keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"qna_{category}")]]
    else:
        response = "Data tidak ditemukan."
        keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_list")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(response, reply_markup=reply_markup, parse_mode="Markdown")

async def delete_qna(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tambahkan refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Cek status login
    if not context.user_data.get('admin_logged_in'):
        await query.message.edit_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin")
        return

    # Parse data callback
    data_parts = query.data.split("_")
    category = data_parts[1]  # delete_[kategori]_[id]
    qna_id = data_parts[2]
    
    # Konfirmasi penghapusan
    keyboard = [
        [
            InlineKeyboardButton("✅ Ya", callback_data=f"confirm_delete_{category}_{qna_id}"),
            InlineKeyboardButton("❌ Tidak", callback_data=f"admin_qna_detail_{category}_{qna_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "⚠️ *Konfirmasi Penghapusan*\n\n"
        "Apakah Anda yakin ingin menghapus pertanyaan ini?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tambahkan refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Cek status login
    if not context.user_data.get('admin_logged_in'):
        await query.message.edit_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin")
        return

    # Parse data callback
    data_parts = query.data.split("_")
    category = data_parts[2]  # confirm_delete_[kategori]_[id]
    qna_id = data_parts[3]
    
    # Mapping nama tabel
    table_mapping = {
        "kemuridan": "qna_kemuridan",
        "fiqih": "qna_fiqih",
        "tassawuf": "qna_tassawuf",
        "keluarga": "qna_keluarga"
    }
    
    table_name = table_mapping.get(category)
    
    # Hapus dari database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (qna_id,))
    conn.commit()
    conn.close()
    
    # Kembali ke daftar QnA
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"admin_qna_{category}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        "✅ *Berhasil!*\n\n"
        "Pertanyaan telah dihapus.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )



# crud
async def admin_qna_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Tampilkan semua kategori QnA ini
    keyboard = [
        [InlineKeyboardButton("📖 Qna Kemuridan", callback_data="admin_add_kemuridan")],
        [InlineKeyboardButton("🕌 Qna Fiqih", callback_data="admin_add_fiqih")],
        [InlineKeyboardButton("🧘 Qna Tassawuf", callback_data="admin_add_tassawuf")],
        [InlineKeyboardButton("👨‍👩‍👧‍👦 Qna Keluarga", callback_data="admin_add_keluarga")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="admin_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text("📝 *Tambah QnA*\nSilakan pilih kategori:", 
                                reply_markup=reply_markup, 
                                parse_mode="Markdown")

async def admin_add_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Parse kategori dari callback data
    category = query.data.split("_")[2]  # admin_add_[kategori]
    
    # Mapping nama tabel
    table_mapping = {
        "kemuridan": "qna_kemuridan",
        "fiqih": "qna_fiqih",
        "tassawuf": "qna_tassawuf",
        "keluarga": "qna_keluarga"
    }
    
    # Ambil data dari database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, question FROM {table_mapping[category]}")
    qna_list = cursor.fetchall()
    conn.close()
    
    # Buat keyboard dengan daftar pertanyaan yang ada
    keyboard = []
    for id, question in qna_list:
        keyboard.append([InlineKeyboardButton(question, callback_data=f"add_qna_{category}_{id}")])
    
    # Tambahkan tombol "Tambah Pertanyaan Baru" dan "Kembali"
    keyboard.extend([
        [InlineKeyboardButton("➕ Tambah Pertanyaan Baru", callback_data=f"add_new_{category}")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="admin_qna_add")]
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Tampilkan pesan dengan judul sesuai kategori
    category_titles = {
        "kemuridan": "Kemuridan",
        "fiqih": "Fiqih",
        "tassawuf": "Tassawuf",
        "keluarga": "Keluarga"
    }
    
    await query.message.edit_text(
        f"📝 *Tambah QnA {category_titles[category]}*\n\n"
        "Daftar pertanyaan yang sudah ada:\n"
        "Pilih pertanyaan untuk menambah atau klik tambah baru.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def add_new_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk tombol Tambah Pertanyaan Baru"""
    query = update.callback_query
    await query.answer()
    
    # Simpan kategori yang dipilih
    category = query.data.split("_")[2]  # add_new_[kategori]
    context.user_data['current_category'] = category
    
    await query.message.edit_text(
        "📝 *Tambah Pertanyaan Baru*\n\n"
        "Silakan ketik pertanyaan yang ingin ditambahkan:",
        parse_mode="Markdown"
    )
    return INPUT_QUESTION

async def receive_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk menerima input pertanyaan"""
    # Simpan pertanyaan
    context.user_data['new_question'] = update.message.text
    
    await update.message.reply_text(
        "✍️ *Masukkan Jawaban*\n\n"
        "Silakan ketik jawaban untuk pertanyaan tersebut:",
        parse_mode="Markdown"
    )
    return INPUT_ANSWER

async def receive_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk menerima input jawaban dan menyimpan ke database"""
    category = context.user_data.get('current_category')
    question = context.user_data.get('new_question')
    answer = update.message.text
    
    # Mapping nama tabel
    table_mapping = {
        "kemuridan": "qna_kemuridan",
        "fiqih": "qna_fiqih",
        "tassawuf": "qna_tassawuf",
        "keluarga": "qna_keluarga"
    }
    
    table_name = table_mapping.get(category)
    
    # Simpan ke database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (question, answer) VALUES (%s, %s)", 
                  (question, answer))
    conn.commit()
    conn.close()
    
    # Buat keyboard untuk kembali
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"admin_add_{category}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Berhasil!*\n\n"
        "Pertanyaan dan jawaban baru telah ditambahkan.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    # Bersihkan data temporary
    context.user_data.pop('current_category', None)
    context.user_data.pop('new_question', None)
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk membatalkan conversation"""
    category = context.user_data.get('current_category')
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"admin_add_{category}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "❌ Dibatalkan.\nProses tambah pertanyaan dibatalkan.",
        reply_markup=reply_markup
    )
    
    # Bersihkan data temporary
    context.user_data.pop('current_category', None)
    context.user_data.pop('new_question', None)
    
    return ConversationHandler.END

# Tambahkan fungsi handler baru ini
async def view_qna_for_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tambahkan refresh timeout
    await refresh_session_timeout(update, context)
    
    query = update.callback_query
    await query.answer()
    
    # Cek status login
    if not context.user_data.get('admin_logged_in'):
        await query.message.edit_text("⚠️ Sesi telah berakhir. Silakan login kembali dengan /admin")
        return

    data_parts = query.data.split("_")
    
    if query.data.startswith("edit_start_"):
        # Handle permulaan proses edit
        category = data_parts[2]
        qna_id = data_parts[3]
        context.user_data['edit_category'] = category
        context.user_data['edit_id'] = qna_id
        
        keyboard = [
            [
                InlineKeyboardButton("📝 Edit Pertanyaan", callback_data=f"edit_question_{category}_{qna_id}"),
                InlineKeyboardButton("📝 Edit Jawaban", callback_data=f"edit_answer_{category}_{qna_id}")
            ],
            [InlineKeyboardButton("⬅️ Kembali", callback_data=f"add_qna_{category}_{qna_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "*Pilih yang ingin diedit:*\n"
            "Pilih bagian yang ingin Anda edit.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    elif query.data.startswith("edit_question_"):
        category = data_parts[2]
        qna_id = data_parts[3]
        context.user_data['edit_category'] = category
        context.user_data['edit_id'] = qna_id
        await query.message.edit_text(
            "📝 *Edit Pertanyaan*\n\n"
            "Silakan ketik pertanyaan baru:",
            parse_mode="Markdown"
        )
        return EDIT_QUESTION

    elif query.data.startswith("edit_answer_"):
        category = data_parts[2]
        qna_id = data_parts[3]
        context.user_data['edit_category'] = category
        context.user_data['edit_id'] = qna_id
        await query.message.edit_text(
            "📝 *Edit Jawaban*\n\n"
            "Silakan ketik jawaban baru:",
            parse_mode="Markdown"
        )
        return EDIT_ANSWER

    elif query.data.startswith("confirm_delete_"):
        category = data_parts[2]
        qna_id = data_parts[3]
        
        # Tentukan nama tabel
        table_mapping = {
            "kemuridan": "qna_kemuridan",
            "fiqih": "qna_fiqih",
            "tassawuf": "qna_tassawuf",
            "keluarga": "qna_keluarga"
        }
        table_name = table_mapping.get(category)
        
        # Hapus dari database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (qna_id,))
        conn.commit()
        conn.close()
        
        # Tampilkan pesan sukses
        keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"admin_add_{category}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "✅ *Berhasil!*\n\nPertanyaan telah dihapus.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    elif query.data.startswith("delete_"):
        category = data_parts[1]
        qna_id = data_parts[2]
        
        # Tampilkan konfirmasi
        keyboard = [
            [
                InlineKeyboardButton("✅ Ya", callback_data=f"confirm_delete_{category}_{qna_id}"),
                InlineKeyboardButton("❌ Tidak", callback_data=f"add_qna_{category}_{qna_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(
            "⚠️ *Konfirmasi Penghapusan*\n\n"
            "Apakah Anda yakin ingin menghapus pertanyaan ini?",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return
    
    else:  # Untuk menampilkan detail QnA
        category = data_parts[2]
        qna_id = data_parts[3]
        
        table_mapping = {
            "kemuridan": "qna_kemuridan",
            "fiqih": "qna_fiqih",
            "tassawuf": "qna_tassawuf",
            "keluarga": "qna_keluarga"
        }
        table_name = table_mapping.get(category)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT question, answer FROM {table_name} WHERE id = %s", (qna_id,))
        qna = cursor.fetchone()
        conn.close()
        
        if qna:
            response = f"*Pertanyaan:*\n{qna[0]}\n\n*Jawaban:*\n{qna[1]}"
            keyboard = [
                [InlineKeyboardButton("✏️ Edit", callback_data=f"edit_start_{category}_{qna_id}")],
                [InlineKeyboardButton("🗑️ Hapus", callback_data=f"delete_{category}_{qna_id}")],
                [InlineKeyboardButton("⬅️ Kembali", callback_data=f"admin_add_{category}")]
            ]
        else:
            response = "Data tidak ditemukan."
            keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"admin_add_{category}")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(response, reply_markup=reply_markup, parse_mode="Markdown")

# Tambahkan fungsi untuk menangani edit pertanyaan
async def edit_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_question = update.message.text
    category = context.user_data.get('edit_category')
    qna_id = context.user_data.get('edit_id')
    
    table_mapping = {
        "kemuridan": "qna_kemuridan",
        "fiqih": "qna_fiqih",
        "tassawuf": "qna_tassawuf",
        "keluarga": "qna_keluarga"
    }
    table_name = table_mapping.get(category)
    
    # Update database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET question = %s WHERE id = %s", (new_question, qna_id))
    conn.commit()
    conn.close()
    
    # Tampilkan pesan sukses
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"add_qna_{category}_{qna_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Berhasil!*\n\n"
        "Pertanyaan telah diperbarui.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# Tambahkan fungsi untuk menangani edit jawaban
async def edit_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_answer = update.message.text
    category = context.user_data.get('edit_category')
    qna_id = context.user_data.get('edit_id')
    
    table_mapping = {
        "kemuridan": "qna_kemuridan",
        "fiqih": "qna_fiqih",
        "tassawuf": "qna_tassawuf",
        "keluarga": "qna_keluarga"
    }
    table_name = table_mapping.get(category)
    
    # Update database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET answer = %s WHERE id = %s", (new_answer, qna_id))
    conn.commit()
    conn.close()
    
    # Tampilkan pesan sukses
    keyboard = [[InlineKeyboardButton("⬅️ Kembali", callback_data=f"add_qna_{category}_{qna_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✅ *Berhasil!*\n\n"
        "Jawaban telah diperbarui.",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    
    return ConversationHandler.END

# Tambahkan fungsi ini di bagian atas setelah fungsi-fungsi import
async def handle_unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk menangani pesan yang tidak sesuai menu"""
    # Jika pesan adalah command yang tidak dikenali
    if update.message.text.startswith('/'):
        await update.message.reply_text(
            "❌ *Maaf, command tidak dikenali*\n\n"
            "Silakan gunakan:\n"
            "• /start - untuk memulai bot\n"
            "• /tanyajawab - untuk melihat daftar pertanyaan\n"
            "• /admin - untuk akses admin panel",
            parse_mode="Markdown"
        )
        return

    # Untuk pesan teks biasa
    keyboard = [
        [InlineKeyboardButton("📖 Mulai Tanya Jawab", callback_data="tanyajawab")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🙏 *Mohon Maaf*\n\n"
        "Kami tidak dapat menjawab pertanyaan melalui chat langsung.\n"
        "Silakan gunakan menu yang tersedia untuk mengakses pertanyaan-pertanyaan "
        "seputar Tarekat Idrisiyyah.\n\n"
        "Klik tombol di bawah untuk melihat daftar pertanyaan:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

def main():
    print("⚡ Memulai bot Telegram...")
    app = Application.builder().token(TOKEN).build()
    
    # Hapus handler yang duplikat
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tanyajawab", tanyajawab_command))
    app.add_handler(CallbackQueryHandler(tanyajawab_callback, pattern="^tanyajawab$"))
    app.add_handler(CallbackQueryHandler(logout, pattern="^admin_logout$"))
    app.add_handler(CallbackQueryHandler(admin_qna_list, pattern="^admin_qna_list$"))

    # Handler QnA
    app.add_handler(CallbackQueryHandler(panduan, pattern="^panduan$"))
    app.add_handler(CallbackQueryHandler(bantuan, pattern="^bantuan$"))
    app.add_handler(CallbackQueryHandler(qna_detail, pattern="^(admin_qna_detail_|)(kemuridan|fiqih|tassawuf|keluarga)_\\d+$"))
    app.add_handler(CallbackQueryHandler(qna_kemuridan, pattern="^qna_kemuridan$"))
    app.add_handler(CallbackQueryHandler(qna_fiqih, pattern="^qna_fiqih$"))
    app.add_handler(CallbackQueryHandler(qna_tassawuf, pattern="^qna_tassawuf$"))
    app.add_handler(CallbackQueryHandler(qna_keluarga, pattern="^qna_keluarga$"))
    
    # Handler Admin
    conv_handler = ConversationHandler(
       entry_points=[CommandHandler("admin", admin)],
       states={
           USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, username)],
           PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, password)]
       },
        fallbacks=[],
        per_message=False
    )
    app.add_handler(conv_handler)

    # Handler Admin QnAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    app.add_handler(CallbackQueryHandler(admin_qna_kemuridan, pattern="^admin_qna_kemuridan$"))
    app.add_handler(CallbackQueryHandler(admin_qna_fiqih, pattern="^admin_qna_fiqih$"))
    app.add_handler(CallbackQueryHandler(admin_qna_tassawuf, pattern="^admin_qna_tassawuf$"))
    app.add_handler(CallbackQueryHandler(admin_qna_keluarga, pattern="^admin_qna_keluarga$"))
    app.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
    app.add_handler(CallbackQueryHandler(admin_qna_add, pattern="^admin_qna_add$"))
    app.add_handler(CallbackQueryHandler(admin_add_category, pattern="^admin_add_(kemuridan|fiqih|tassawuf|keluarga)$"))

    # Handler untuk menambah QnA baru
    add_qna_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_new_question, pattern="^add_new_(kemuridan|fiqih|tassawuf|keluarga)$")],
        states={
            INPUT_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_question)],
            INPUT_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_answer)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False
    )
    app.add_handler(add_qna_handler)

    # Tambahkan handler barusdfsdfsdf
    app.add_handler(CallbackQueryHandler(view_qna_for_add, pattern="^(add_qna|delete|confirm_delete)_(kemuridan|fiqih|tassawuf|keluarga)_\\d+$"))

    # Tambahkan handler untuk delete
    app.add_handler(CallbackQueryHandler(delete_qna, pattern="^delete_(kemuridan|fiqih|tassawuf|keluarga)_\\d+$"))
    app.add_handler(CallbackQueryHandler(confirm_delete, pattern="^confirm_delete_(kemuridan|fiqih|tassawuf|keluarga)_\\d+$"))

    # Handler untuk edit QnA
    edit_conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(view_qna_for_add, pattern="^edit_(question|answer)_(kemuridan|fiqih|tassawuf|keluarga)_\\d+$")
        ],
        states={
            EDIT_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_question)],
            EDIT_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_answer)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False
    )
    app.add_handler(edit_conv_handler)

    # Update pattern untuk view_qna_for_add untuk mencakup edit
    app.add_handler(CallbackQueryHandler(
        view_qna_for_add, 
        pattern="^(add_qna|delete|confirm_delete|edit_start)_(kemuridan|fiqih|tassawuf|keluarga)_\\d+$"
    ))

    # Tambahkan handler untuk option dan ganti password
    app.add_handler(CallbackQueryHandler(admin_option, pattern="^admin_option$"))
    
    # Handler untuk ganti username
    change_username_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(change_username, pattern="^change_username$")],
        states={
            INPUT_NEW_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_username)]
        },
        fallbacks=[],
        per_message=False
    )
    app.add_handler(change_username_handler)
    
    # Handler untuk ganti password
    change_password_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(change_password, pattern="^change_password$")],
        states={
            INPUT_NEW_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_password)]
        },
        fallbacks=[],
        per_message=False
    )
    app.add_handler(change_password_handler)

    # Handler untuk ganti panduan
    change_panduan_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(change_panduan, pattern="^change_panduan$")],
        states={
            INPUT_NEW_PANDUAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_panduan)]
        },
        fallbacks=[],
        per_message=False
    )
    app.add_handler(change_panduan_handler)

    # Handler untuk ganti bantuan
    change_bantuan_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(change_bantuan, pattern="^change_bantuan$")],
        states={
            INPUT_NEW_BANTUAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_new_bantuan)]
        },
        fallbacks=[],
        per_message=False
    )
    app.add_handler(change_bantuan_handler)

    # Handler untuk menangani pesan yang tidak dikenali
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,  # Tangkap semua pesan teks tapi bukan command
        handle_unknown_message
    ))

    print("🤖 Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return 'ok'
