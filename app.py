import streamlit as st
import google.generativeai as genai
from PIL import Image
from docx import Document
from io import BytesIO
from docx.shared import Pt, Cm

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Trợ lý giáo viên tiểu học",
    page_icon="📘",
    layout="centered"
)

# ================== TIÊU ĐỀ ==================
st.markdown("""
<div style="text-align:center;">
    <h1>📘 TRỢ LÝ GIÁO VIÊN TIỂU HỌC</h1>
    <h3>KỊCH BẢN LÊN LỚP CHI TIẾT TỪ ẢNH SGK</h3>
    <p><i>Chụp nhiều trang SGK → AI đọc → Viết lời GV & HS chuẩn</i></p>
    <p style="color:#555;"><b>✍️ Tác giả:</b> NGUYỄN VĂN DU – Giáo viên Tiểu học</p>
</div>
<hr>
""", unsafe_allow_html=True)

# ================== SIDEBAR: API KEY ==================
with st.sidebar:
    st.header("🔐 Google Gemini API Key")
    api_key = st.text_input(
        "Nhập API Key (tạo tại aistudio.google.com)",
        type="password"
    )
    st.caption("✔ Dạng key: AIzaSy...")

if not api_key:
    st.warning("⬅️ Nhập API Key để bắt đầu")
    st.stop()

# ================== CẤU HÌNH GEMINI ==================
try:
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ API Key không hợp lệ. Hãy tạo key mới tại Google AI Studio.")
    st.stop()

# 🔥 MODEL ỔN ĐỊNH – ĐỌC ẢNH – KHÔNG LỖI 404
model = genai.GenerativeModel("models/gemini-pro-vision")

# ================== THÔNG TIN BÀI DẠY ==================
st.markdown("## 📝 THÔNG TIN BÀI DẠY")
mon = st.selectbox("📚 Môn học", ["Tin học", "Công nghệ", "Toán", "Tiếng Việt"])
lop = st.selectbox("🎓 Lớp", ["3", "4", "5"])
ten_bai = st.text_input("📖 Tên bài học")

# ================== ẢNH SGK ==================
st.markdown("## 📸 ẢNH SÁCH GIÁO KHOA")
uploaded_images = st.file_uploader(
    "Chụp hoặc tải NHIỀU ảnh trang SGK (rõ chữ)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# ================== XỬ LÝ ==================
if st.button("🚀 TẠO KỊCH BẢN LÊN LỚP"):
    if not uploaded_images:
        st.warning("⚠️ Vui lòng tải ít nhất 1 ảnh SGK")
        st.stop()

    images = []
    for f in uploaded_images:
        img = Image.open(f).convert("RGB")
        images.append(img)

    st.markdown("### 🖼️ Ảnh đã tải")
    cols = st.columns(3)
    for i, img in enumerate(images):
        with cols[i % 3]:
            st.image(img, use_column_width=True)

    # ================== PROMPT CHUẨN GIÁO VIÊN ==================
    prompt = f"""
Bạn là GIÁO VIÊN TIỂU HỌC có kinh nghiệm dạy thật và dự giờ.

Dựa vào TOÀN BỘ nội dung trong các ảnh SGK,
hãy viết KỊCH BẢN TIẾN TRÌNH LÊN LỚP CHI TIẾT cho bài:

- Môn: {mon}
- Lớp: {lop}
- Bài: {ten_bai}

YÊU CẦU BẮT BUỘC:
1. Đúng kiến thức SGK.
2. Chia 4 hoạt động:
   a) Khởi động
   b) Hình thành kiến thức
   c) Luyện tập
   d) Vận dụng
3. MỖI HOẠT ĐỘNG PHẢI CÓ:
   - 🎤 GV nói: (viết câu nói CỤ THỂ, đúng sư phạm)
   - 👧👦 HS trả lời: (dự kiến phản hồi)
   - ✅ GV chốt: (kết luận ngắn gọn, chính xác)
4. Ngôn ngữ:
   - Chuẩn giáo viên tiểu học
   - Nói được ngay trên lớp
   - Không chung chung
5. Phù hợp 1 tiết 35 phút.

TRÌNH BÀY RÕ RÀNG – DỄ IN – DỄ DÙNG.
"""

    with st.spinner("🤖 AI đang đọc ảnh và viết kịch bản..."):
        try:
            response = model.generate_content([prompt, *images])
            content = response.text
        except Exception as e:
            st.error(f"❌ Lỗi Gemini: {e}")
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

    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
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
        "⬇️ Tải file Word (Kịch bản lên lớp)",
        buf,
        file_name=f"Kich_ban_len_lop_{ten_bai}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666;'>© 2026 – Trợ lý giáo viên | Nguyễn Văn Du</div>",
    unsafe_allow_html=True
)