print("🚀 Bot sedang dijalankan...")

import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import google.generativeai as genai  


# Load environment variables dari .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or not TOKEN:
    raise ValueError("API Key Gemini atau Bot Token Telegram tidak ditemukan. Pastikan ada di .env")

print("✅ API Key & Token berhasil dimuat.")

genai.configure(api_key=GEMINI_API_KEY)

# FAQ yang udah fix
faq = {
    "tasawuf": """“Ilmu tasawuf adalah ilmu untuk mengetahui kondisi jiwa manusia, kondisi yang terpuji maupun yang tercela, mengetahui bagaimana cara membersihkannya dari kondisi yang tercela dan menghiasinya dengan sifat-sifat yang terpuji serta untuk mengetahui tata cara/proses perjalanan menuju kepada Allah SWT”.\n
قال القاضي شيخ الإسلام زكريا الأنصاري رحم الله تعالى ( التصوف علم يعرف به أحوال تزكية النفوس وتصفية الأخلاق وتعمير الظاهر والباطن لنيل السعادة الأبدية ) هامش الرسالة القشيرية\n
“Al-Qadhi Al-Syaikh Zakaria Al-Anshari berkata: Ilmu tasawuf adalah ilmu yang dapat menunjukkan keadaan bersihnya hati seorang manusia, dan penjernihan perilaku, dan menggerakkan zahir dan batin (tubuh dan hati) untuk beribadah kepada Allah SWT, untuk meraih kebahagiaan yang abadi.”""",
    
    "tarekat": """اَلسَّيْرَةُ الْمُخْتَصَّةُ بِالسَّالِكِيْنَ إِلَى اللهِ عَزَّ وَجَلَّ مِنْ قَطْعِ الْمَنَازِلِ وَالتَّرَاقِيْ فِى الْمَقَامَاتِ.\n
"Tarekat adalah Jalan khusus orang-orang yang melakukan pengembaraan spiritual menuju kepada Allah 'Azza wa Jalla, yaitu dengan menempuh manazil (level-level hawa nafsu) dan menaiki pilar-pilar ruhani (maqamat) [seperti tawakal, ikhlas, dan lain-lainnya]”. (Al Jurjani, at Ta’rifat, hlm 183, dan ‘Abdur Razaq, Mu’jam ishthilahat ash-Shufiyyah, hlm. 85.)""",

"idrisiyyah": """Idrisiyyah adalah sebuah pergerakan Islam global dengan manhaj tarekat Shufiyah yang intens dalam proses pembersihan jiwa, pembeningan hati, dan pembentukan akhlaq al-karimah. Bergerak di bidang dakwah, pendidikan, ekonomi dan sosial kemasyarakatan.""",

"syarat_murid_idrisiyyah": """Syarat menjadi murid yaitu:\n
1. Memiliki kesadaran hati menghadap kepada Allah dan akhirat serta berpaling dari tipu daya dunia dan makhluk.\n
2. Mempercayai wali mursyid sebagai pewaris Nabi Saw.\n
3. Ingin dibimbing lahir dan batin.\n
4. Taubat nasuha dari segala dosa dan maksiat.\n
5. Mendapatkan talqin dzikir dan ijazah wirid.\n
6. Menjalankan suluk tarekat.""",

"talqin": """Talqin maknanya adalah pengajaran agama, terutama pokok agama, yaitu kalimah thayyibah. 
Ijazah artinya mengabsahkan seseorang untuk mengamalkan wirid sebuah tarekat karena sebelumnya telah diajarkan apa itu wirid, dari mana wirid tersebut, bagaimana kaifiat (tata cara)nya dan sebagainya. 
Sedangkan Baiat adalah suatu proses menjadikan mursyid sebagai imam dalam agama, khususnya dalam pengamalan syariat. Tujuan baiat adalah mengamalkan ajaran Nabi Saw tentang urgennya baiat dan supaya murid belajar berkomitmen terhadap seluruh syariat dan sunah Nabi Saw.

Perbedaan ketiganya: 
- **Talqin** adalah wilayah pengajaran dan bimbingan. 
- **Ijazah** adalah pengabsahan mengamalkan suatu amalan dzikir. 
- **Baiat** merupakan wilayah pengangkatan pemimpin dalam mengamalkan syariat.""",


}

# Fungsi start
async def start(update: Update, context):
    user = update.message.from_user
    first_name = user.first_name  
    await update.message.reply_text(f"Hai, {first_name}! 🚀 Selamat datang di bot kami.\n\nGunakan /tanyajawab untuk mulai bertanya yaaa")

# Menu utama
async def tanyajawab(update: Update, context):
    user = update.message.from_user
    first_name = user.first_name 
    keyboard = [
        [InlineKeyboardButton("🔍 QnA seputar tarekat ?🤔", callback_data="cari_jawaban")],
        [InlineKeyboardButton("📜 Lihat Panduan", callback_data="lihat_panduan")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="bantuan")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(f"Haii {first_name}! Sini pertanyaannya... Pilih menu di bawah ini:", reply_markup=reply_markup)

# Tampilkan daftar pertanyaan
async def show_questions(update: Update, context):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🟢 Apa itu Tasawuf?", callback_data="tasawuf")],
        [InlineKeyboardButton("🟢 Apa itu Tarekat?", callback_data="tarekat")],
        [InlineKeyboardButton("🟢 Apakah Idrisiyyah itu?", callback_data="idrisiyyah")],
        [InlineKeyboardButton("🟢 Apa syarat menjadi murid Tarekat Idrisiyyah?", callback_data="syarat_murid_idrisiyyah")],
        [InlineKeyboardButton("🟢 Apa itu Talqin, Ijazah, dan Baiat?", callback_data="talqin")],
        [InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="back_to_menu")]
    ]

    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text("Pilih pertanyaan yang ingin kamu tanyakan lagi yaa :", reply_markup=reply_markup)

# Jawaban pertanyaan
async def answer_question(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data in faq:
        await query.message.reply_text(f"{faq[query.data]}")

        keyboard = [
            [InlineKeyboardButton("🔙 Kembali ke Pertanyaan", callback_data="cari_jawaban")],
            [InlineKeyboardButton("🏠 Kembali ke Menu Utama", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text("Pilih opsi di bawah ini:", reply_markup=reply_markup)

# Kembali ke menu utama
async def back_to_menu(update: Update, context):
    query = update.callback_query
    user = query.from_user
    first_name = user.first_name 
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("🔍 QnA seputar tarekat ?🤔", callback_data="cari_jawaban")],
        [InlineKeyboardButton("📜 Lihat Panduan", callback_data="lihat_panduan")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="bantuan")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(f"Hai {first_name}! Sini pertanyaannya... Pilih menu di bawah ini:", reply_markup=reply_markup)

# Handler untuk menu utama
async def menu_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "cari_jawaban":
        await show_questions(update, context)
    elif query.data == "lihat_panduan":
        await query.message.reply_text("📜 Berikut adalah panduan penggunaan bot ini:\n1. Gunakan /tanyajawab untuk memulai\n2. Klik menu yang tersedia\n3. Ajukan pertanyaanmu langsung\n4. Ajukan pertanyaan random dengan reply pesan bot setelah ketik /tanyajawab")
    elif query.data == "bantuan":
        await query.message.reply_text("❓ Butuh bantuan? Hubungi admin @Nueeeeeeeeeeeeeeeee ajaaaa🤙 yaaa 👨‍💻")
    elif query.data == "back_to_menu":
        await back_to_menu(update, context)

# Menjawab pertanyaan yang tidak ada di FAQ dengan AI
async def chat_with_ai(update: Update, context):
    user_message = update.message.text
    
    if user_message.lower() in faq:
        await update.message.reply_text(faq[user_message.lower()])
    else:
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(user_message)
            ai_reply = response.text if response.text else "Maaf, saya tidak bisa menjawab itu."
            await update.message.reply_text(ai_reply)
        except Exception as e:
            await update.message.reply_text(f"Terjadi kesalahan: {str(e)}")

# Menyambut member baru pake nama grup
async def welcome_new_member(update: Update, context):
    chat_title = update.message.chat.title  # Ambil nama grup
    for new_member in update.message.new_chat_members:
        first_name = new_member.first_name
        await update.message.reply_text(f"🎉 Selamat datang {first_name} di grup {chat_title}! 🚀")



# Fungsi utama untuk menjalankan bot
def main():
    print("⚡ Memulai bot Telegram...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tanyajawab", tanyajawab))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^(cari_jawaban|lihat_panduan|bantuan|back_to_menu)$"))
    app.add_handler(CallbackQueryHandler(answer_question, pattern="^(tasawuf|tarekat|idrisiyyah|syarat_murid_idrisiyyah|talqin)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    print("🤖 Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
