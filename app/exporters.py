import os
from datetime import datetime
from fpdf import FPDF

STATIC_DIR = os.path.join(os.getcwd(), "static")
EXPORT_FOLDER = os.path.join(STATIC_DIR, "exports")
os.makedirs(EXPORT_FOLDER, exist_ok=True)


class ComicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(120, 120, 140)
        self.cell(0, 8, "ComicCraft AI - Story Creator", align="R", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def clean_text_for_pdf(text: str) -> str:
    """Replaces Unicode characters that cannot be encoded by Latin-1 in basic FPDF fonts."""
    replacements = {
        '—': '--',
        '–': '-',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '…': '...',
        '•': '*',
        '✨': '*',
        '★': '*',
        '🎨': '',
        '📖': '',
        '⭐': '*'
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    # Filter non-latin1 characters
    return text.encode('latin-1', 'replace').decode('latin-1')


def save_pdf(layout: list) -> str:
    """
    Compiles the full comic into a multi-page PDF file using FPDF.
    
    Args:
        layout (list): List of panel dictionaries.
        
    Returns:
        str: Relative path to the generated PDF.
    """
    pdf = ComicPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        panel_num = panel.get("panel", 1)
        title = panel.get("title", f"Panel {panel_num}")
        image_path = panel.get("image_path", "")
        story_text = panel.get("text", "")
        scene_desc = panel.get("scene_description", "")

        # 1. Panel Header Banner
        pdf.set_fill_color(30, 41, 59)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 15)
        clean_title = clean_text_for_pdf(f"Panel {panel_num}: {title}")
        pdf.cell(0, 12, f"  {clean_title}", ln=True, fill=True, align="L")
        pdf.ln(5)

        # 2. Image Placement
        # A4 width is 210mm; margins = 15mm on each side -> printable width = 180mm
        img_width = 170
        img_height = 100
        x_pos = (210 - img_width) / 2
        
        # Check image existence
        resolved_img_path = image_path
        if not os.path.isabs(resolved_img_path):
            resolved_img_path = os.path.join(os.getcwd(), image_path)

        if os.path.exists(resolved_img_path):
            try:
                pdf.image(resolved_img_path, x=x_pos, y=pdf.get_y(), w=img_width, h=img_height)
                pdf.set_y(pdf.get_y() + img_height + 6)
            except Exception as e:
                print(f"⚠️ Failed to insert image into PDF: {e}")
                pdf.ln(5)
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(200, 50, 50)
                pdf.cell(0, 10, f"[Image file unavailable: {image_path}]", ln=True, align="C")
        else:
            pdf.ln(5)
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(200, 50, 50)
            pdf.cell(0, 10, f"[Image not found: {image_path}]", ln=True, align="C")

        # 3. Scene Description (Italics)
        if scene_desc:
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(100, 116, 139)
            clean_desc = clean_text_for_pdf(scene_desc)
            pdf.multi_cell(0, 6, f"Scene: {clean_desc}")
            pdf.ln(3)

        # 4. Narration & Dialogue Text
        if story_text:
            pdf.set_fill_color(248, 250, 252)
            pdf.set_text_color(15, 23, 42)
            pdf.set_font("Helvetica", "", 11)
            
            clean_story = clean_text_for_pdf(story_text)
            pdf.multi_cell(0, 7, clean_story, border=0, fill=False)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    full_pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(full_pdf_path)

    relative_path = f"static/exports/{filename}"
    print(f"📄 PDF successfully compiled at: {full_pdf_path}")
    return relative_path
