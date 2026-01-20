import streamlit as st
from PIL import Image
from docx import Document
from io import BytesIO
from docx.shared import Pt, Cm

# ================== CẤU HÌNH TRANG ==================
st.set_page_config(
    page_title="Trợ lý giáo viên tiểu học (Không AI)",
    page_icon="📘",
    layout="centered"
)

# ================== TIÊU ĐỀ ==================
st.markdown("""
<div style="text-align:center;">
    <h1>📘 TRỢ LÝ GIÁO VIÊN TIỂU HỌC</h1>
    <h3>VIẾT TIẾN TRÌNH LÊN LỚP – KHÔNG CẦN AI</h3>
    <p><i>Chụp ảnh SGK → GV nhập ý chính → App soạn kịch bản chuẩn</i></p>
    <p style="color:#555;"><b>✍️ Tác giả:</b> NGUYỄN VĂN DU – Giáo viên Tiểu học</p>
</div>
<hr>
""", unsafe_allow_html=True)

# ================== THÔNG TIN BÀI DẠY ==================
st.markdown("## 📝 THÔNG TIN BÀI DẠY")
mon = st.selectbox("📚 Môn học", ["Tin học", "Công nghệ", "Toán", "Tiếng Việt"])
lop = st.selectbox("🎓 Lớp", ["3", "4", "5"])
ten_bai = st.text_input("📖 Tên bài học")

# ================== ẢNH SGK ==================
st.markdown("## 📸 ẢNH SÁCH GIÁO KHOA (THAM KHẢO)")
uploaded_images = st.file_uploader(
    "Chụp hoặc tải NHIỀU ảnh trang SGK",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_images:
    cols = st.columns(3)
    for i, f in enumerate(uploaded_images):
        img = Image.open(f)
        with cols[i % 3]:
            st.image(img, use_column_width=True)

# ================== NỘI DUNG CHÍNH ==================
st.markdown("## ✍️ GIÁO VIÊN NHẬP NỘI DUNG CHÍNH")
noidung = st.text_area(
    "Ghi các ý chính của bài học (theo SGK):",
    height=200,
    placeholder="- Khái niệm...\n- Ví dụ...\n- Ghi nhớ..."
)

# ================== TẠO TIẾN TRÌNH ==================
if st.button("🚀 TẠO TIẾN TRÌNH LÊN LỚP"):
    if not ten_bai or not noidung:
        st.warning("⚠️ Vui lòng nhập TÊN BÀI và NỘI DUNG CHÍNH")
        st.stop()

    content = f"""
BÀI: {ten_bai}
MÔN: {mon} – LỚP: {lop}

--------------------------------
I. KHỞI ĐỘNG (5 phút)
🎤 GV nói:
- Hôm nay chúng ta sẽ học bài: {ten_bai}.
- GV nêu câu hỏi gợi mở liên quan đến bài học.

👧👦 HS:
- Lắng nghe, trả lời theo hiểu biết.

✅ GV chốt:
- Dẫn dắt vào bài mới.

--------------------------------
II. HÌNH THÀNH KIẾN THỨC (15 phút)
🎤 GV nói:
- GV giới thiệu nội dung chính của bài.
- GV lần lượt trình bày từng ý:

{noidung}

👧👦 HS:
- Quan sát, lắng nghe.
- Trả lời câu hỏi của giáo viên.

✅ GV chốt:
- Nhấn mạnh kiến thức trọng tâm.

--------------------------------
III. LUYỆN TẬP (10 phút)
🎤 GV nói:
- GV giao bài tập hoặc câu hỏi luyện tập.
- Hướng dẫn HS thực hiện.

👧👦 HS:
- Thực hành cá nhân / nhóm.
- Trình bày kết quả.

✅ GV chốt:
- Nhận xét, sửa sai, tuyên dương.

--------------------------------
IV. VẬN DỤNG (5 phút)
🎤 GV nói:
- Yêu cầu HS vận dụng kiến thức vào tình huống thực tế.

👧👦 HS:
- Trả lời, liên hệ thực tế.

✅ GV chốt:
- Dặn dò, củng cố bài học.
"""

    st.markdown("## 📄 TIẾN TRÌNH LÊN LỚP")
    st.text(content)

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

    doc.add_paragraph("Tác giả: NGUYỄN VĂN DU – Giáo viên Tiểu học").italic = True

    for line in content.split("\n"):
        doc.add_paragraph(line)

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)

    st.download_button(
        "⬇️ Tải file Word (.docx)",
        buf,
        file_name=f"Tien_trinh_{ten_bai}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#666;'>© 2026 – Trợ lý giáo viên | Nguyễn Văn Du</div>",
    unsafe_allow_html=True
)