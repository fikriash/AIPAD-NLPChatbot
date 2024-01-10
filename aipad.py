import logging
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import chartgpt as cg
import plotly.io as pio
import io 
from io import BytesIO
import openai
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_IDS = [int(id) for id in os.getenv("ALLOWED_USER_IDS").split(',')]
OPENAI_KEY = os.getenv("API_KEY")
server = os.getenv("server")
database = os.getenv("database")
schema = os.getenv("schema")
username = os.getenv("user")
password = os.getenv("password")
ID_ADMIN = os.getenv("ADMIN")

openai.api_key = OPENAI_KEY
data_agg = ["agregat_mahasiswa_terdaftar.sql", "agregat_mahasiswa_aktif.sql", "agregat_mahasiswa_asing.sql", "agregat_jabatan_fungsional_dosen.sql", "agregat_pendidikan_dosen.sql", "agregat_penerima_beasiswa.sql","output_penulisan_buku.sql","output_review_article.sql","output_rdpd.sql"]
data_raw = ["data_mahasiswa_terdaftar.sql", "data_mahasiswa_aktif.sql","data_mahasiswa_asing.sql", "data_dosen_jabfung.sql", "data_dosen_pendidikan.sql", "data_penerima_beasiswa.sql","output_penulisan_buku.sql","output_review_article.sql","output_rdpd.sql"]
connection = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(connection)
conn = engine.connect()
print("Connected to SQL Server")

MENU, SUBMENU1, SUBMENU2, DATA_MESSAGE, GPT_CHART, PROMPT, GPT_RAW, GPT_AGG, SEND_CHART, WAITING_MESSAGE = range(10)

def limited_keyword(input_message):
    food_keywords = ["data", "aggregat", "raw", "informasi", 'agregat']
    for keyword in food_keywords:
        if keyword in input_message:
            return True
    return False

def main_menu(update:Update, context:CallbackContext):
    user_id = update.message.from_user.id
    if user_id in ALLOWED_USER_IDS:
        message = "Selamat datang di AIPAD\nArtifical Intelligence Universitas Padjadjaran for Data and Information\nPlease choose a menu :"
        buttons = [
            [InlineKeyboardButton("Ensiklopedia", callback_data="submenu1")],
            [InlineKeyboardButton("Permintaan data & Informasi", callback_data="submenu2")],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(text=message, reply_markup=reply_markup)
        return MENU
    else:
        update.message.reply_text("Maaf, anda tidak memiliki akses ke chatbot ini")

def submenu1(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    message = """ Berikut ensiklopedia AIPAD\n/start --> memulai program chatbot\n/regist --> registrasi ID Telegram untuk akses chatbot\nRaw --> format data berupa detail yang dapat diolah lebih lanjut\nAgregat --> format data berupa ringkasan yang mengandung agregasi data (jumlah/rata-rata)\nInfografis --> option menu untuk generate grafik data sesuai keinginan"""
    query.edit_message_text(text=message)
   ## df = pd.read_excel('./File_excel/data_mahasiswa_aktif.xlsx')
    return ConversationHandler.END

def submenu2(update:Update, context:CallbackContext):
    user = update.callback_query.from_user
    message = "Permintaan data & Informasi terpilih\nSilahkan pilih format data yang kamu inginkan di bawah ini"
    buttons = [
        [InlineKeyboardButton("Raw", callback_data="submenu2a")],
        [InlineKeyboardButton("Agregat", callback_data="submenu2b")],
        [InlineKeyboardButton("Infografis", callback_data="submenu2c")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="back_main_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=user.id, text=message, reply_markup=reply_markup)
    return SUBMENU2

def submenu2a(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    if query['data'] == 'submenu2a':
        format = "Raw"
    message = f"Anda memilih format {format}. Data apa yang anda perlukan?"
    query.edit_message_text(text=message)
    return GPT_RAW

def submenu2b(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    if query['data'] == 'submenu2b':
        format = "Agregat"
    message = f"Anda memilih format {format}. Data apa yang anda perlukan?"
    query.edit_message_text(text=message)
    return GPT_AGG

def submenu2c(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    if query['data'] == 'submenu2c':
        format = "Infografis"
    user= update.callback_query.from_user
    message = f"Anda memilih format {format}.Silahkan pilih terlebih dahulu jenis grafik apa yang anda ingin gunakan?"
    buttons = [
        [InlineKeyboardButton("Bar Chart", callback_data="barplot")],
        [InlineKeyboardButton("Pie Chart", callback_data="pie")],
        [InlineKeyboardButton("Line Chart", callback_data="lineplot")],
        [InlineKeyboardButton("Scatter Chart", callback_data="scatterplot")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    context.bot.send_message(chat_id=user.id, text=message, reply_markup=reply_markup)
    print("Memasuki return DATA_MESSAGE")
    return DATA_MESSAGE

def generate_excel_bytes(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)
    return output

def generate_chart(prompt, graph, data):

    user_query = f"write only python code (do not add your description and do not add '```') to {prompt} menggunakan seaborn {graph} dengan pallete pastel, figsize (8,6), dan menambahkan %matplotlib inline based on the following data:\n\n{data}"

    # Menggunakan GPT-4 untuk mendapatkan instruksi untuk plot
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Sesuaikan dengan model terbaru yang tersedia
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates plots."},
            {"role": "user", "content": user_query}
        ],
        max_tokens=200,
    )

    # Mengambil instruksi dari hasil respons GPT-4
    plot_instructions = response.choices[0].message["content"].strip()
    print(plot_instructions)

    try:
        # Mencoba menjalankan instruksi menggunakan exec
        exec(plot_instructions)
        
        # Simpan plot dalam bentuk bytes
        img_bytes_io = BytesIO()
        plt.savefig(img_bytes_io, format='png')
        img_bytes_io.seek(0)
        return img_bytes_io
    except Exception as e:
        print(f"Error while executing plot instructions: {e}")
        return None

def gpt_raw(update: Update, context:CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    content = update.message.text.lower()
    if user_id in ALLOWED_USER_IDS:
        if limited_keyword(content):
            response = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : f"Saya hanya memerlukan jawaban singkat, tolong sebutkan data '{content}'",
                }]
            )
            hasil_gpt = response.choices[0].message["content"]
            next_input = f"Apakah judul data dari kalimat '{hasil_gpt}' ada yang sesuai dengan list nama sql file yang saya miliki disini : '{data_raw}'? Jika ya ada, keluarkan hanya 'nama sql file' nya saja! Jika tidak berikan output 'Data tidak ada.' Saya mengharapkan jawaban yang akurat!"
            response2 = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : next_input,
                }]
            )
            hasil_gpt2 = response2.choices[0].message["content"]
            next_input2 = f"Ekstrak nama SQL dari teks berikut : {hasil_gpt2}, jawab singkat!"
            response3 = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : next_input2,
                }]
            )
            hasil_sql = response3.choices[0].message["content"]
            print(hasil_sql)
            try:
                # Query read
                with open(f'./data/{hasil_sql}', 'r') as file:
                    sql_query = file.read()
                query = text(sql_query)

                # Eksekusi query
                df = pd.read_sql_query(query, conn)
                excel_bytes = generate_excel_bytes(df)
                split = hasil_sql.split('.')
                nama_file = split[0]
                # print(f"nama file : {nama_file}")
                file_name = f"{nama_file}.xlsx"

                # Kirim file Excel ke pengguna
                chat_id = update.effective_chat.id
                context.bot.send_document(chat_id=chat_id, document=InputFile(excel_bytes, filename=file_name))
            except Exception as e:
                update.message.reply_text(f"Permintaan anda tidak dapat dipenuhi karena {e}")
        else:
            update.message.reply_text("Maaf, permintaan anda diluar ruang lingkup chatbot ini")
    else:
        update.message.reply_text("Maaf, anda tidak memiliki akses ke chatbot ini")

def gpt_agg(update: Update, context:CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    content = update.message.text.lower()
    if user_id in ALLOWED_USER_IDS:
        if limited_keyword(content):
            response = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : f"Saya hanya memerlukan jawaban singkat, tolong sebutkan data '{content}'",
                }]
            )
            hasil_gpt = response.choices[0].message["content"]
            next_input = f"Apakah judul data dari kalimat '{hasil_gpt}' ada yang sesuai dengan list nama sql file yang saya miliki disini : '{data_agg}'? Jika ya ada, keluarkan hanya 'nama sql file' nya saja! Jika tidak berikan output 'Data tidak ada.' Saya mengharapkan jawaban yang akurat!"
            response2 = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : next_input,
                }]
            )
            hasil_gpt2 = response2.choices[0].message["content"]
            next_input2 = f"Ekstrak nama SQL dari teks berikut : {hasil_gpt2}, jawab singkat!"
            response3 = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : next_input2,
                }]
            )
            hasil_sql = response3.choices[0].message["content"]
            print(hasil_sql)
            try:
                # Query read
                with open(f'./data/{hasil_sql}', 'r') as file:
                    sql_query = file.read()
                query = text(sql_query)

                # Eksekusi query
                df = pd.read_sql_query(query, conn)
                text_data = df.to_string(index=False)
                next_input3 = f"Informasikan data berikut:\n\n{text_data}!"
                response4 = openai.ChatCompletion.create(
                    model = "gpt-4",
                    messages = [{
                        "role" : "user",
                        "content" : next_input3,
                    }]
                )
                hasil_agg = response4.choices[0].message["content"]
                chat_id = update.effective_chat.id
                context.bot.send_message(chat_id=chat_id, text=hasil_agg)
            except Exception as e:
                update.message.reply_text(f"Permintaan anda tidak dapat dipenuhi karena {e}")
        else:
            update.message.reply_text("Maaf, permintaan anda diluar ruang lingkup chatbot ini")
    else:
        update.message.reply_text("Maaf, anda tidak memiliki akses ke chatbot ini")

def graph_type(update: Update, context:CallbackContext):
    print("Return DATA_MESSAGE success, menjalankan fungsi get_graph")
    chat_id = update.callback_query.message.chat.id
    context.user_data['graph_type'] = update.callback_query.data
    graph_type = context.user_data['graph_type']
    print(graph_type)
    message = f"Anda memilih format {graph_type}, Data apa yang anda perlukan?"
    context.bot.send_message(chat_id=chat_id, text=message)
    print("Memasuki return GPT_CHART")
    return GPT_CHART

def graph_data(update: Update, context:CallbackContext):
    print("Return GPT_CHART success, menjalankan fungsi graph_data")
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    content = update.message.text.lower()
    if user_id in ALLOWED_USER_IDS:
        if limited_keyword(content):
            response = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : f"Saya hanya memerlukan jawaban singkat, tolong sebutkan nama data yang diminta user dari kalimat '{content}'",
                }]
            )
            hasil_gpt = response.choices[0].message["content"]
            next_input = f"Apakah judul data dari kalimat '{hasil_gpt}' ada yang sesuai dengan list nama sql file yang saya miliki disini : '{data_raw}'? Jika ya ada, keluarkan hanya 'nama sql file' nya saja! Jika tidak berikan output 'Data tidak ada.' Saya mengharapkan jawaban yang akurat!"
            response2 = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : next_input,
                }]
            )
            hasil_gpt2 = response2.choices[0].message["content"]
            next_input2 = f"Ekstrak nama .sql dari teks berikut : {hasil_gpt2}, jawab singkat!"
            response3 = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = [{
                    "role" : "user",
                    "content" : next_input2,
                }]
            )
            hasil_sql = response3.choices[0].message["content"]
            print(hasil_sql)
            nama_data = hasil_sql.split('.')
            # try:
            # Query read
            with open(f'./data/{hasil_sql}', 'r') as file:
                sql_query = file.read()
            query = text(sql_query)

            # Eksekusi query
            df = pd.read_sql_query(query, conn)
            context.user_data['df'] = df
            print(df.head())
            print("")
            print("Memasuki return PROMPT...")
            print("Return PROMPT success, menjalankan fungsi prompt_input")
            graph_type = context.user_data.get('graph_type')
            print(graph_type)
            chat_id = update.effective_chat.id

            # Tanyakan prompt kepada pengguna
            context.bot.send_message(chat_id = chat_id, text=f"Anda memilih jenis grafik {graph_type} untuk {nama_data[0]}. Silahkan masukan perintah pembuatan infografis yang dibutuhkan\n\n Contoh : tampilkan persentase jumlah mahasiswa berdasarkan angkatan")
            
            # Ganti state ke PROMPT_INPUT
            print("Memasuki return SEND_CHART")
            return SEND_CHART
        else:
            context.bot.send_message(chat_id=chat_id, text="Maaf, data yang anda minta tidak ada") 
    else:
        context.bot.send_message(chat_id=chat_id, text="Maaf, anda tidak memiliki akses ke chatbot ini") 

def create_chart(update: Update, context: CallbackContext):
    print("Return SEND_CHART success, menjalankan fungsi create_chart")
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    prompt = update.message.text
    
    raw = context.user_data.get('df')
    df = pd.DataFrame(raw)
    data = df.head().to_string(index=False)
    print(data)
    graph_type = context.user_data.get('graph_type')
    
    try:
        # Create chart using df, format, and prompt
        print("Creating chart based on the prompt")
        img_bytes_io = generate_chart(prompt, graph_type, data)
        if img_bytes_io is not None:
        # Send chart directly to the user
            context.bot.send_photo(chat_id=chat_id, photo=img_bytes_io, caption=f"{graph_type}.png")
        else:
            update.message.reply_text("Failed to create the chart. Maybe the data format or prompt is incorrect.")
    except Exception as e:
            update.message.reply_text(f" Permintaan anda tidak dapat dipenuhi karena{e}")

    # End the conversation
    return ConversationHandler.END

def back_main_menu(update:Update, context:CallbackContext):
    query = update.callback_query
    query.answer()
    main_menu(update, context)
    return ConversationHandler.END

def regist (update: Update, context:CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(
        """
        Selamat datang di AIPAD, silahkan isi formulir registrasi di bawah ini :
        \nNIP  :
        \nKeperluan :
        
        """
    )
    return WAITING_MESSAGE

def send_regist(update: Update, context: CallbackContext):
    print("starting program...")
    user_id = update.effective_user.id
    message_user = update.message.text
    print(message_user)
    data_regist = f"Pesan dari {update.message.from_user.first_name}: {message_user}\nID : {user_id}"
    logger.info(f"Mengirim pesan ke admin...")
    print(ID_ADMIN)
    context.bot.send_message(chat_id=ID_ADMIN, text=data_regist)
    logger.info("Pesan ke admin berhasil terkirim.")
    update.message.reply_text("Data registrasi anda telah berhasil dikirim, silahkan tunggu verifikasi pendaftaran dalam 5 menit kedepan")
    
    return ConversationHandler.END

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu), CommandHandler('regist',regist)],
        states={
            MENU: [CallbackQueryHandler(submenu1, pattern="^submenu1$"),
                   CallbackQueryHandler(submenu2, pattern="^submenu2$")],
            SUBMENU2: [CallbackQueryHandler(submenu2a, pattern="^submenu2a$"),
                       CallbackQueryHandler(submenu2b, pattern="^submenu2b$"),
                       CallbackQueryHandler(submenu2c, pattern="^submenu2c$"),
                       CallbackQueryHandler(back_main_menu, pattern="^back_main_menu$")],
            GPT_CHART:[MessageHandler(Filters.text, graph_data)],
            GPT_RAW : [MessageHandler(Filters.text, gpt_raw)],
            GPT_AGG : [MessageHandler(Filters.text, gpt_agg)],      
            DATA_MESSAGE: [CallbackQueryHandler(graph_type, pattern="^(barplot|pie|lineplot|scatterplot)$")],
            # PROMPT: [MessageHandler(Filters.text, prompt_input)], # pattern="^(barplot|pie|lineplot|scatterplot)$"
            SEND_CHART: [MessageHandler(Filters.text, create_chart)],
            WAITING_MESSAGE : [MessageHandler(Filters.text, send_regist)],

        },
        fallbacks=[],
        allow_reentry=True
    )

    dp.add_handler(conversation_handler)

    


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
