import streamlit as st
import os
import re
import zipfile
import io
from PIL import Image
from fpdf import FPDF
import base64

# تكوين الصفحة
st.set_page_config(
    page_title="مستخرج صور البطاقات ",
    page_icon="🆔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# إعداد حالة الليل والنهار
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = "الرئيسية"

# دالة للحصول على CSS حسب الوضع
def get_css():
    if st.session_state.dark_mode:
        return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(45deg, #1a1a2e, #16213e, #0f3460, #533c7b);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #e8e8e8;
        font-family: 'Cairo', sans-serif;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(185, 147, 72, 0.3); }
        50% { box-shadow: 0 0 40px rgba(185, 147, 72, 0.6), 0 0 60px rgba(185, 147, 72, 0.3); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #b99348, #8b7355, #6b5b73);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(185, 147, 72, 0.5);
        animation: gradientShift 8s ease infinite, float 6s ease-in-out infinite;
    }
    
    .upload-section {
        border: 3px solid transparent;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        background: linear-gradient(#1a1a2e, #1a1a2e) padding-box,
                    linear-gradient(45deg, #b99348, #8b7355, #6b5b73, #b99348) border-box;
        backdrop-filter: blur(15px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        animation: glow 4s ease-in-out infinite;
    }
    
    .upload-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.8),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .success-message {
        background: linear-gradient(135deg, #2d4a22, #3e5a2f, #4a7c59);
        color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #4a7c59;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(74, 124, 89, 0.4);
        animation: float 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .success-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .warning-message {
        background: linear-gradient(135deg, #6b4423, #8b5a2b, #a0733c);
        color: #fef3e2;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #a0733c;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(160, 115, 60, 0.4);
        animation: float 3s ease-in-out infinite 0.5s;
    }
    
    .error-message {
        background: linear-gradient(135deg, #5c2e2e, #7a3d3d, #914848);
        color: #ffeaea;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #914848;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(145, 72, 72, 0.4);
        animation: float 3s ease-in-out infinite 1s;
    }
    
    .card-info {
        background: linear-gradient(135deg, #2a2a3e, #363654, #424267);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 6px solid #b99348;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card-info:hover {
        transform: translateX(10px);
        box-shadow: 0 15px 40px rgba(185, 147, 72, 0.3);
    }
    
    .about-card {
        background: linear-gradient(135deg, #2a2a3e, #363654, #424267);
        padding: 3rem;
        border-radius: 18px;
        margin: 2rem 0;
        border: 3px solid transparent;
        background-clip: padding-box;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.7),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        animation: float 4s ease-in-out infinite;
    }
    
    .about-card:hover {
        transform: scale(1.02);
        box-shadow: 0 25px 60px rgba(185, 147, 72, 0.4);
    }
    
    .sidebar .stRadio > div {
        background: linear-gradient(135deg, #2a2a3e, #363654) !important;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(185, 147, 72, 0.3);
    }
    
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(45deg, #b99348, #8b7355, #6b5b73);
        border-radius: 2px;
    }
    
    /* تحسين الأزرار */
    .stButton > button {
        background: linear-gradient(45deg, #b99348, #8b7355);
        border: none;
        border-radius: 12px;
        color: #fff;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(185, 147, 72, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #8b7355, #6b5b73);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(185, 147, 72, 0.5);
    }
    
    /* تحسين المدخلات */
    .stFileUploader {
        border-radius: 12px;
        background: rgba(42, 42, 62, 0.8);
        border: 2px dashed #b99348;
    }
</style>
"""
    else:
        return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(45deg, #2c3e50, #34495e, #5d6d7e, #85929e);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        color: #2c3e50;
        font-family: 'Cairo', sans-serif;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(52, 73, 94, 0.3); }
        50% { box-shadow: 0 0 40px rgba(52, 73, 94, 0.6), 0 0 60px rgba(52, 73, 94, 0.3); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-8px); }
        60% { transform: translateY(-4px); }
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #34495e, #5d6d7e, #85929e);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(52, 73, 94, 0.3);
        animation: gradientShift 10s ease infinite, bounce 3s ease-in-out infinite;
    }
    
    .upload-section {
        border: 3px solid transparent;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        background: linear-gradient(rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.95)) padding-box,
                    linear-gradient(45deg, #34495e, #5d6d7e, #85929e, #34495e) border-box;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 60px rgba(52, 73, 94, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.8);
        transition: all 0.4s ease;
        animation: glow 5s ease-in-out infinite;
    }
    
    .upload-section:hover {
        transform: translateY(-6px) scale(1.01);
        box-shadow: 0 30px 80px rgba(52, 73, 94, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 1);
    }
    
    .success-message {
        background: linear-gradient(135deg, #d5e8d4, #a4c492, #7fb069);
        color: #2e5233;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #7fb069;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(127, 176, 105, 0.3);
        animation: float 4s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .success-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .warning-message {
        background: linear-gradient(135deg, #f4e4c1, #e6c569, #d4ac0d);
        color: #7d6608;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #d4ac0d;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(212, 172, 13, 0.3);
        animation: float 4s ease-in-out infinite 1s;
    }
    
    .error-message {
        background: linear-gradient(135deg, #f5b7b1, #ec7063, #cb4335);
        color: #78281f;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #cb4335;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(203, 67, 53, 0.3);
        animation: float 4s ease-in-out infinite 2s;
    }
    
    .card-info {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(245, 245, 245, 0.95));
        padding: 2rem;
        border-radius: 18px;
        margin: 1rem 0;
        border-left: 8px solid #34495e;
        box-shadow: 0 15px 40px rgba(52, 73, 94, 0.2);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .card-info:hover {
        transform: translateX(12px) scale(1.02);
        box-shadow: 0 20px 50px rgba(52, 73, 94, 0.3);
        border-left-color: #5d6d7e;
    }
    
    .about-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(245, 245, 245, 0.95));
        padding: 3rem;
        border-radius: 22px;
        margin: 2rem 0;
        border: 4px solid transparent;
        background-clip: padding-box;
        box-shadow: 0 25px 60px rgba(52, 73, 94, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.8);
        text-align: center;
        transition: all 0.4s ease;
        animation: float 6s ease-in-out infinite;
    }
    
    .about-card:hover {
        transform: scale(1.03);
        box-shadow: 0 30px 70px rgba(52, 73, 94, 0.4);
    }
    
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(45deg, #34495e, #5d6d7e, #85929e);
        border-radius: 3px;
        box-shadow: 0 2px 4px rgba(52, 73, 94, 0.3);
    }
    
    /* تحسين الأزرار */
    .stButton > button {
        background: linear-gradient(45deg, #34495e, #5d6d7e);
        border: none;
        border-radius: 15px;
        color: white;
        font-weight: 700;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(52, 73, 94, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #5d6d7e, #85929e);
        transform: translateY(-3px) scale(1.03);
        box-shadow: 0 12px 30px rgba(52, 73, 94, 0.5);
    }
    
    /* تحسين المدخلات */
    .stFileUploader {
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.9);
        border: 3px dashed #34495e;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        background: rgba(255, 255, 255, 1);
        border-color: #5d6d7e;
    }
    
    /* تحسين المقاييس */
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(52, 73, 94, 0.2);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(52, 73, 94, 0.3);
    }
</style>
"""

# تطبيق CSS
st.markdown(get_css(), unsafe_allow_html=True)

def parse_filename(filename):
    """
    تحليل اسم الملف لاستخراج البيانات
    تنسيق الملف المتوقع: {الرقم_القومي}_{الوجه}_{الاسم}.jpg
    """
    # إزالة امتداد الملف
    name_without_ext = os.path.splitext(filename)[0]
    
    # تقسيم الاسم بناءً على "_"
    parts = name_without_ext.split('_')
    
    if len(parts) < 3:
        return None
    
    national_id = parts[0]
    face_type = parts[1]
    name = '_'.join(parts[2:])  # في حالة وجود "_" في الاسم
    
    # التحقق من صحة face_type
    if face_type not in ['1', '2']:
        return None
    
    # التحقق من أن الرقم القومي يحتوي على أرقام فقط
    if not national_id.isdigit():
        return None
    
    return {
        'national_id': national_id,
        'face_type': int(face_type),
        'name': name,
        'filename': filename
    }

def create_pdf_with_images(front_image=None, back_image=None, output_name="output.pdf"):
    """
    إنشاء ملف PDF يحتوي على الصور
    """
    pdf = FPDF('P', 'mm', 'A4')
    
    # إضافة الصفحة الأولى (الوجه الأمامي)
    if front_image:
        pdf.add_page()
        
        # تحويل الصورة إلى تنسيق مؤقت
        img_buffer = io.BytesIO()
        front_image.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        # حساب أبعاد الصورة للحفاظ على النسبة
        img_width, img_height = front_image.size
        
        # أبعاد صفحة A4 (210 x 297 mm) مع هوامش
        page_width = 190  # 210 - 20 (هوامش)
        page_height = 277  # 297 - 20 (هوامش)
        
        # حساب النسبة للحفاظ على أبعاد الصورة
        width_ratio = page_width / img_width
        height_ratio = page_height / img_height
        ratio = min(width_ratio, height_ratio)
        
        new_width = img_width * ratio
        new_height = img_height * ratio
        
        # توسيط الصورة
        x = (210 - new_width) / 2
        y = (297 - new_height) / 2
        
        # حفظ الصورة في ملف مؤقت
        temp_image_path = f"temp_front_{output_name}.jpg"
        front_image.save(temp_image_path, 'JPEG')
        
        try:
            pdf.image(temp_image_path, x, y, new_width, new_height)
        finally:
            # حذف الملف المؤقت
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
    
    # إضافة الصفحة الثانية (الوجه الخلفي) إذا كانت موجودة
    if back_image:
        pdf.add_page()
        
        # نفس العملية للصورة الخلفية
        img_width, img_height = back_image.size
        
        page_width = 190
        page_height = 277
        
        width_ratio = page_width / img_width
        height_ratio = page_height / img_height
        ratio = min(width_ratio, height_ratio)
        
        new_width = img_width * ratio
        new_height = img_height * ratio
        
        x = (210 - new_width) / 2
        y = (297 - new_height) / 2
        
        temp_image_path = f"temp_back_{output_name}.jpg"
        back_image.save(temp_image_path, 'JPEG')
        
        try:
            pdf.image(temp_image_path, x, y, new_width, new_height)
        finally:
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
    
    # إنشاء buffer للـ PDF
    pdf_buffer = io.BytesIO()
    pdf_content = pdf.output(dest='S')
    if isinstance(pdf_content, str):
        pdf_content = pdf_content.encode('latin-1')
    pdf_buffer.write(pdf_content)
    pdf_buffer.seek(0)
    
    return pdf_buffer

def process_images(uploaded_files):
    """
    معالجة الصور المرفوعة وإنشاء ملفات PDF
    """
    # تحليل أسماء الملفات
    parsed_files = []
    invalid_files = []
    
    for uploaded_file in uploaded_files:
        parsed = parse_filename(uploaded_file.name)
        if parsed:
            # إضافة الصورة إلى البيانات المحللة
            parsed['image'] = Image.open(uploaded_file)
            parsed_files.append(parsed)
        else:
            invalid_files.append(uploaded_file.name)
    
    # تجميع الملفات حسب الرقم القومي والاسم
    grouped_cards = {}
    
    for file_data in parsed_files:
        key = f"{file_data['national_id']}_{file_data['name']}"
        if key not in grouped_cards:
            grouped_cards[key] = {
                'national_id': file_data['national_id'],
                'name': file_data['name'],
                'front': None,
                'back': None
            }
        
        if file_data['face_type'] == 1:
            grouped_cards[key]['front'] = file_data['image']
        elif file_data['face_type'] == 2:
            grouped_cards[key]['back'] = file_data['image']
    
    # إنشاء ملفات PDF
    pdf_files = {}
    
    for key, card_data in grouped_cards.items():
        if card_data['front'] or card_data['back']:
            pdf_name = f"{card_data['national_id']}_{card_data['name']}.pdf"
            pdf_buffer = create_pdf_with_images(
                front_image=card_data['front'],
                back_image=card_data['back'],
                output_name=pdf_name
            )
            pdf_files[pdf_name] = {
                'buffer': pdf_buffer,
                'card_data': card_data
            }
    
    return pdf_files, invalid_files

def create_zip_file(pdf_files):
    """
    إنشاء ملف ZIP يحتوي على جميع ملفات PDF
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for pdf_name, pdf_data in pdf_files.items():
            pdf_data['buffer'].seek(0)
            zip_file.writestr(pdf_name, pdf_data['buffer'].read())
    
    zip_buffer.seek(0)
    return zip_buffer

def get_download_link(file_buffer, filename, link_text):
    """
    إنشاء رابط تحميل للملف
    """
    file_buffer.seek(0)
    b64 = base64.b64encode(file_buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

# صفحة حول التطبيق
def about_page():
    st.markdown('<h1 class="main-header">ℹ️ حول التطبيق</h1>', unsafe_allow_html=True)
    
    # إضافة تأثير ترحيبي
    st.balloons()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 👨‍💻 معلومات المطور")
        st.markdown("Abdulrahman Sayed")
    with col2:
        st.markdown("## 👑 معلومات المالك")
        st.markdown("Ahmed ElCiCi")
        st.markdown("مــــــصـــــــر")
    
    st.markdown("---")
    
    st.markdown("## 🚀 عن التطبيق")
    st.markdown("**مستخرج صور البطاقات** هو تطبيق ويب متقدم مصمم لمعالجة وتنظيم صور البطاقات الشخصية بطريقة احترافية.")
    
    st.markdown("### 🎯 الهدف من التطبيق:")
    st.markdown("""
    - تسهيل عملية تنظيم صور البطاقات
    - إنشاء ملفات PDF عالية الجودة
    - توفير واجهة سهلة الاستخدام
    - معالجة عدة بطاقات في وقت واحد
    """)
    
    st.markdown("### ✨ المميزات:")
    st.markdown("""
    - دعم تام للغة العربية
    - واجهة جميلة ومتجاوبة
    - وضع ليلي ونهاري
    - معالجة سريعة وآمنة
    - تصدير PDF و ZIP
    """)
    
    st.markdown("### 📊 الإحصائيات:")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("الإصدار", "2.0")
    with col2:
        st.metric("التاريخ", "أغسطس 2025")
    with col3:
        st.metric("المنصة", "Streamlit")
    with col4:
        st.metric("اللغة", "Python")
    
    st.markdown("---")
    
    st.markdown("## 📧 التواصل والدعم")
    st.markdown("للاستفسارات والدعم الفني، يرجى التواصل مع فريق التطوير")
    st.success("شكراً لاستخدامكم تطبيق مستخرج صور البطاقات! 🙏")

# الواجهة الرئيسية
def main_app():
    # العنوان الرئيسي
    st.markdown('<h1 class="main-header">🆔 مستخرج صور البطاقات الخاص بأحمد السيسي</h1>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # شرح التطبيق
    st.markdown("""
    ### مرحباً بك في مستخرج صور البطاقات! 👋
    
    **كيفية استخدام التطبيق:**
    1. ارفع صور البطاقات بالتنسيق المطلوب
    2. اضغط على "بدء المعالجة"
    3. حمّل ملفات PDF منفردة أو جميعها في ملف ZIP واحد
    
    **تنسيق أسماء الملفات المطلوب:**
    ```
    {الرقم_القومي}_{الوجه}_{الاسم}.jpg
    ```
    - **الرقم القومي**: رقم البطاقة الشخصية
    - **الوجه**: 1 للوجه الأمامي، 2 للوجه الخلفي
    - **الاسم**: اسم صاحب البطاقة
    
    **مثال:** `26708050104304_1_نادية خميس على محمد.jpg`
    """)
    
    st.markdown("---")
    
    # قسم رفع الملفات
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    st.markdown("### 📁 رفع صور البطاقات")
    
    uploaded_files = st.file_uploader(
        "اختر صور البطاقات",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        help="يمكنك رفع عدة صور معاً. تأكد من تسمية الملفات بالتنسيق المطلوب."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_files:
        st.markdown(f"### 📋 تم رفع {len(uploaded_files)} ملف")
        
        # عرض معاينة مصغرة للصور
        st.markdown("#### معاينة الصور المرفوعة:")
        
        cols = st.columns(min(len(uploaded_files), 5))
        for idx, uploaded_file in enumerate(uploaded_files[:5]):  # عرض أول 5 صور فقط
            with cols[idx % 5]:
                try:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=uploaded_file.name, width="stretch")
                except Exception as e:
                    st.error(f"خطأ في عرض الصورة: {uploaded_file.name}")
        
        if len(uploaded_files) > 5:
            st.info(f"تم عرض 5 صور من أصل {len(uploaded_files)}. جميع الصور ستتم معالجتها.")
        
        # زر بدء المعالجة
        if st.button("🚀 بدء المعالجة", type="primary", width="stretch"):
            
            # شريط التقدم
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # تحديث شريط التقدم
                status_text.text("جاري تحليل أسماء الملفات...")
                progress_bar.progress(25)
                
                # معالجة الصور
                pdf_files, invalid_files = process_images(uploaded_files)
                
                progress_bar.progress(50)
                status_text.text("جاري إنشاء ملفات PDF...")
                
                # عرض الملفات غير الصالحة
                if invalid_files:
                    st.markdown('<div class="warning-message">', unsafe_allow_html=True)
                    st.markdown("⚠️ **تحذير:** الملفات التالية لا تتبع التنسيق المطلوب:")
                    for invalid_file in invalid_files:
                        st.markdown(f"- {invalid_file}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                progress_bar.progress(75)
                status_text.text("جاري إنشاء ملف ZIP...")
                
                if pdf_files:
                    # إنشاء ملف ZIP
                    zip_buffer = create_zip_file(pdf_files)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ تمت المعالجة بنجاح!")
                    
                    # إضافة تأثير نجاح
                    st.success("🎉 تمت معالجة البطاقات بنجاح!")
                    st.balloons()
                    
                    # رسالة النجاح
                    st.markdown('<div class="success-message">', unsafe_allow_html=True)
                    st.markdown(f"🎉 **تمت معالجة {len(pdf_files)} بطاقة بنجاح!**")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # زر تحميل ملف ZIP
                    st.markdown("### 📦 تحميل جميع البطاقات")
                    
                    zip_buffer.seek(0)
                    st.download_button(
                        label="📥 تحميل جميع البطاقات كـ ZIP",
                        data=zip_buffer.read(),
                        file_name="all_cards.zip",
                        mime="application/zip",
                        type="primary",
                        width="stretch"
                    )
                    
                    # عرض البطاقات المعالجة مع أزرار التحميل المنفردة
                    st.markdown("### 📄 البطاقات المعالجة")
                    
                    for pdf_name, pdf_data in pdf_files.items():
                        card_data = pdf_data['card_data']
                        
                        st.markdown(f'<div class="card-info">', unsafe_allow_html=True)
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**📋 {card_data['name']}**")
                            st.markdown(f"🆔 الرقم القومي: {card_data['national_id']}")
                            
                            faces = []
                            if card_data['front']:
                                faces.append("الوجه الأمامي")
                            if card_data['back']:
                                faces.append("الوجه الخلفي")
                            st.markdown(f"📑 الصفحات: {' + '.join(faces)}")
                        
                        with col2:
                            pdf_data['buffer'].seek(0)
                            st.download_button(
                                label="📥 تحميل",
                                data=pdf_data['buffer'].read(),
                                file_name=pdf_name,
                                mime="application/pdf",
                                key=f"download_{pdf_name}"
                            )
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                else:
                    st.markdown('<div class="error-message">', unsafe_allow_html=True)
                    st.markdown("❌ **خطأ:** لم يتم العثور على ملفات صالحة للمعالجة.")
                    st.markdown("تأكد من أن أسماء الملفات تتبع التنسيق المطلوب.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.markdown('<div class="error-message">', unsafe_allow_html=True)
                st.markdown(f"❌ **خطأ في المعالجة:** {str(e)}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            finally:
                # إخفاء شريط التقدم ونص الحالة
                progress_bar.empty()
                status_text.empty()
    
    # معلومات سريعة
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("الصيغ المدعومة", "JPG, PNG", "JPEG")
    with col2:
        st.metric("حجم الصفحة", "A4", "297×210 mm")
    with col3:
        st.metric("الإصدار", "2.0", "محدث")

# التنقل الجانبي
def sidebar_navigation():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #2E86AB;'>🆔 القائمة</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        # تبديل الوضع
        theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        theme_text = "تفعيل الوضع الليلي" if not st.session_state.dark_mode else "تفعيل الوضع النهاري"
        
        if st.button(f"{theme_icon} {theme_text}", width="stretch"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        
        # اختيار الصفحة
        page = st.radio(
            "اختر الصفحة:",
            ["الرئيسية", "حول التطبيق"],
            index=0 if st.session_state.current_page == "الرئيسية" else 1
        )
        
        if page != st.session_state.current_page:
            st.session_state.current_page = page
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 🔧 معلومات سريعة")
        st.markdown("**👨‍💻 المطور:** Abdulrahman Sayed")
        st.markdown("**👑 المالك:** Ahmed ElCiCi")  
        st.markdown("**📱 الإصدار:** 2.0")

# التطبيق الرئيسي
def main():
    sidebar_navigation()
    
    if st.session_state.current_page == "الرئيسية":
        main_app()
    elif st.session_state.current_page == "حول التطبيق":
        about_page()

if __name__ == "__main__":
    main()
