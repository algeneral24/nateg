import sys
import os

# إضافة المسار الرئيسي للـ PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from newe import app as application

# Vercel يتوقع متغير باسم 'app'
app = application
