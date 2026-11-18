import docx
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

def create_report_with_cover():
    doc = Document()
    
    # 1. TRANG BÌA
    cover_img_path = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\cover_fixed_v3.png"
    if os.path.exists(cover_img_path):
        p_cover = doc.add_paragraph()
        p_cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_cover.add_run()
        # Full page image: Width ~ 6.5 inches (standard A4 margin)
        run.add_picture(cover_img_path, width=Inches(6.5))
    else:
        doc.add_paragraph("LỖI: Không tìm thấy ảnh trang bìa.")
        
    doc.add_page_break()
    
    # 2. NỘI DUNG (tạm thời thêm 1 đoạn test)
    doc.add_heading("NỘI DUNG ĐỀ BÀI VÀ CÁC ĐƯỜNG LINK NỘP BÀI", level=1)
    doc.add_paragraph("Nội dung báo cáo chi tiết ở đây...")
    
    out_path = r"C:\Users\ADMIN\.gemini\antigravity\scratch\cineman_project\reports\FINAL_REPORT_108.docx"
    doc.save(out_path)
    print(f"Document saved to {out_path}")

if __name__ == "__main__":
    create_report_with_cover()
