import os
import re
from datetime import datetime, date, timedelta
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

class PyBuddyPDF(FPDF):
    def header(self):
        # Header banner styling
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(55, 118, 171) # Python Blue
        self.cell(0, 8, 'PyBuddy - AI Python Learning Buddy', border=False, align='L')
        self.set_text_color(100, 100, 100)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 8, f'Generated on {datetime.now().strftime("%Y-%m-%d")}', border=False, align='R')
        self.ln(10)
        self.line(10, 18, 200, 18)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}', border=False, align='C')

def clean_pdf_text(text: str) -> str:
    """
    Cleans Unicode characters to fit Latin-1 encoding standard used by default FPDF.
    Replaces common smart quotes, emojis, and non-supported symbols.
    """
    if not text:
        return ""
    # Map smart quotes and common symbols
    replacements = {
        '\u201c': '"', '\u201d': '"',
        '\u2018': "'", '\u2019': "'",
        '\u2013': '-', '\u2014': '-',
        '\u2022': '*', '\u2192': '->',
        '\u2264': '<=', '\u2265': '>=',
        '\u2713': '[OK]', '\u274c': '[X]'
    }
    for orig, rep in replacements.items():
        text = text.replace(orig, rep)
    # Remove any other non-ASCII character to avoid encoding crash
    text = re.sub(r'[^\x00-\x7F\u00A0-\u00FF]', '', text)
    return text

def generate_pdf(title: str, content: str) -> bytes:
    """
    Generates a PDF using FPDF and returns raw PDF bytes.
    """
    pdf = PyBuddyPDF()
    pdf.add_page()
    
    # Document Title
    pdf.set_font('helvetica', 'B', 18)
    pdf.set_text_color(55, 118, 171) # Python Blue
    pdf.multi_cell(0, 10, clean_pdf_text(title), align='L')
    pdf.ln(5)
    
    # Document Body
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(30, 30, 30)
    
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('### '):
            pdf.ln(3)
            pdf.set_font('helvetica', 'B', 12)
            pdf.set_text_color(255, 212, 59) # Python Yellow / Darker accent
            pdf.multi_cell(0, 7, clean_pdf_text(line.replace('### ', '').strip()))
            pdf.set_font('helvetica', '', 10)
            pdf.set_text_color(30, 30, 30)
        elif line.strip().startswith('## '):
            pdf.ln(4)
            pdf.set_font('helvetica', 'B', 14)
            pdf.set_text_color(55, 118, 171) # Python Blue
            pdf.multi_cell(0, 8, clean_pdf_text(line.replace('## ', '').strip()))
            pdf.set_font('helvetica', '', 10)
            pdf.set_text_color(30, 30, 30)
        elif line.strip().startswith('# '):
            pdf.ln(5)
            pdf.set_font('helvetica', 'B', 16)
            pdf.set_text_color(55, 118, 171) # Python Blue
            pdf.multi_cell(0, 9, clean_pdf_text(line.replace('# ', '').strip()))
            pdf.set_font('helvetica', '', 10)
            pdf.set_text_color(30, 30, 30)
        else:
            pdf.multi_cell(0, 6, clean_pdf_text(line))
            
    return pdf.output()

def calculate_streak(last_active_str: str, current_streak: int) -> int:
    """
    Calculates the new streak based on the last active date and current date.
    
    Returns:
        New streak count.
    """
    if not last_active_str:
        return 1
        
    try:
        last_active = datetime.strptime(last_active_str.split("T")[0], "%Y-%m-%d").date()
    except Exception:
        return 1
        
    today = date.today()
    delta = today - last_active
    
    if delta == timedelta(days=0):
        # Already active today
        return current_streak
    elif delta == timedelta(days=1):
        # Active yesterday, increment streak
        return current_streak + 1
    else:
        # Missed a day, reset streak to 1
        return 1

def generate_default_assets():
    """
    Generates a beautiful logo and banner using Pillow if they don't already exist.
    """
    logo_path = "assets/logo.png"
    banner_path = "assets/banner.png"
    
    # 1. Create Logo (512x512)
    if not os.path.exists(logo_path):
        img = Image.new("RGBA", (512, 512), color=(15, 23, 42, 255)) # Dark slate background
        draw = ImageDraw.Draw(img)
        
        # Draw elegant Python-inspired circle and letters
        # Outer ring
        draw.arc([40, 40, 472, 472], start=0, end=360, fill=(55, 118, 171, 255), width=16) # Python Blue
        draw.arc([60, 60, 452, 452], start=0, end=360, fill=(255, 212, 59, 255), width=8)  # Python Yellow
        
        # Write "PB" center text using simple shapes or text
        # Since standard fonts might not load reliably, we will draw a stylized logo using geometric shapes
        # Draw a blue head on top, yellow on bottom
        draw.chord([160, 160, 352, 352], start=210, end=330, fill=(55, 118, 171, 255))
        draw.chord([160, 160, 352, 352], start=30, end=150, fill=(255, 212, 59, 255))
        
        # Eyes
        draw.ellipse([210, 200, 230, 220], fill=(248, 250, 252, 255))
        draw.ellipse([280, 290, 300, 310], fill=(248, 250, 252, 255))
        
        # Save logo
        img.save(logo_path)
        
    # 2. Create Banner (1200x400)
    if not os.path.exists(banner_path):
        img = Image.new("RGBA", (1200, 400), color=(15, 23, 42, 255)) # Dark Slate background
        draw = ImageDraw.Draw(img)
        
        # Add subtle pattern (diagonal lines)
        for i in range(-400, 1200, 40):
            draw.line([i, 0, i+400, 400], fill=(30, 41, 59, 255), width=2)
            
        # Draw a beautiful gradient-like accent border
        draw.rectangle([0, 380, 1200, 400], fill=(55, 118, 171, 255)) # Python Blue base
        draw.rectangle([0, 390, 1200, 400], fill=(255, 212, 59, 255)) # Python Yellow base
        
        # Since custom fonts are not guaranteed on all OSes, let's draw stylized tech design blocks
        # Draw stylized terminal blocks
        draw.rectangle([100, 80, 1100, 320], fill=(30, 41, 59, 180), outline=(55, 118, 171, 255), width=4)
        draw.rectangle([100, 80, 1100, 120], fill=(55, 118, 171, 255))
        
        # Terminal Dots
        draw.ellipse([120, 95, 130, 105], fill=(239, 68, 68, 255)) # Red
        draw.ellipse([140, 95, 150, 105], fill=(245, 158, 11, 255)) # Yellow
        draw.ellipse([160, 95, 170, 105], fill=(34, 197, 94, 255)) # Green
        
        # Save banner
        img.save(banner_path)
