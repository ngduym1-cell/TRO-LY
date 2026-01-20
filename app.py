import streamlit as st
import google.generativeai as genai
from PIL import Image
from docx import Document
from io import BytesIO
from docx.shared import Pt, Cm

# ================== CẤU HÌNH ==================
st.set_page_config(
    page_title="Trợ lý giáo viên – Kịch bản lên lớp chi tiết",
    page_icon="📘",
    layout="centered"
)

# ================== TIÊU ĐỀ ==================
st.markdown("""
<div style="text-align:center;">
    <h1>📘 TRỢ LÝ GIÁO VIÊN TIỂU HỌC</h1>
    <h3>KỊCH BẢN LÊN LỚP CHI TIẾT TỪ SGK</h3>
    <p><i>Chụp ảnh SGK → AI hiểu bài → Viết lời GV & HS từng bước</i></p>
    <p style="color:#555;"><b>✍️ Tác giả:</b> NGUYỄN VĂN DU – Giáo viên Tiểu học</p>
</div>
<hr>
""", unsafe_allow_html=True)

# ================== SIDEBAR: API KEY ==================
with st.sidebar:
    st.header("🔐 Google Gemini API Key")
    api_key = st.text_input("Nhập API Key (AIzaSy...)", type="password")

if not api_key:
    st.warning("⬅️ Vui lòng nhập API Key ở thanh bên trái")
    st.stop()

try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"API Key không hợp lệ: {e}")
    st.stop()

model = genai.GenerativeModel("gemini-1.5-flash")

# ================== NHẬP THÔNG TIN ==================
st.markdown("## 📝 THÔNG TIN BÀI DẠY")
mon = st.selectbox("📚 Môn học", ["Tin học", "Công nghệ", "Toán", "Tiếng Việt"])
lop = st.selectbox("🎓 Lớp", ["3", "4", "5"])
ten_bai = st.text_input("📖 Tên bài học")

st.markdown("## 📸 ẢNH SÁCH GIÁO KHOA")
uploaded_images = st.file_uploader(
    "Chụp hoặc tải NHIỀU ảnh trang SGK (rõ chữ)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# ================== NÚT XỬ LÝ ==================
if st.button("🚀 TẠO KỊCH BẢN LÊN LỚP CHI TIẾT"):
    if not uploaded_images:
        st.warning("⚠️ Cần ít nhất 1 ảnh SGK")
        st.stop()

    images = [Image.open(f) for f in uploaded_images]

    st.markdown("### 🖼️ Ảnh đã tải")
    cols = st.columns(3)
    for i, img in enumerate(images):
        with cols[i % 3]:
            st.image(img, use_column_width=True)

    # ================== PROMPT CHUYÊN SÂU ==================
    prompt = f"""
Bạn là GIÁO VIÊN TIỂU HỌC GIỎI, có kinh nghiệm dạy thật và dự giờ.

NHIỆM VỤ:
Dựa vào TOÀN BỘ nội dung trong các ảnh sách giáo khoa,
hãy viết **KỊCH BẢN TIẾN TRÌNH LÊN LỚP CHI TIẾT** cho bài:

- Môn: {mon}
- Lớp: {lop}
- Bài: {ten_bai}

YÊU CẦU BẮT BUỘC:
1. Viết đúng kiến thức trong SGK (từ ảnh).
2. Chia ĐÚNG 4 hoạt động:
   1) Khởi động
   2) Hình thành kiến thức
   3) Luyện tập
   4) Vận dụng
3. MỖI HOẠT ĐỘNG PHẢI CÓ:
   - 🎤 GV nói: (viết câu nói cụ thể, ngắn gọn, chuẩn sư phạm)
   - 👧👦 HS trả lời/dự kiến phản hồi
   - ✅ GV chốt kiến thức (rõ ràng, chính xác)
4. Ngôn ngữ:
   - Đúng kiểu giáo viên tiểu học
   - Dễ nói, dễ nhớ
   - Không dùng thuật ngữ cao siêu
5. Thời lượng: tiết học 35 phút (phân bổ hợp lý).
6. KHÔNG viết chung chung, KHÔNG liệt kê suông.

HÌNH THỨC TRÌNH BÀY:
- Viết theo từng HOẠT ĐỘNG
- Gạch đầu dòng rõ ràng
- Dùng biểu tượng 🎤 👧👦 ✅ để dễ đọc
"""

    with st.spinner("🤖 AI đang phân tích SGK và viết kịch bản lên lớp..."):
        try:
            response = model.generate_content([prompt, *images])
            content = response.text
        except Exception as e:
            st.error(f"Lỗi Gemini: {e}")
            st.stop()

    # ================== HIỂN THỊ ==================
    st.markdown("## 📄 KỊCH BẢN LÊN LỚP CHI TIẾT")
    st.markdown(content)

    # ================== XUẤT WORD ==================
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(3)
    section.right_margin = Cm(2)

    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(14)

    doc.add_paragraph(
        "Tác giả: NGUYỄN VĂN DU – Giáo viên Tiểu học"
    ).italic = True

    for line in content.split("\n"):
        doc.add_paragraph(line)

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)

    st.download_button(
        "⬇️ Tải file Word – Kịch bản lên lớp",
        buf,
        file_name=f"Kich_ban_len_lop_{ten_bai}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666;'>© 2026 – Trợ lý giáo viên | Nguyễn Văn Du</div>",
    unsafe_allow_html=True
)