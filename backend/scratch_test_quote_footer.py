import os
import sys
sys.path.append('c:/Movies/quotation-ai/quotation-ai/backend')
from quotation import generate_quote

data = {
    "show_bg_logo": True,
    "client_name": "Test Client",
    "items": [],
    "output_path": "c:/Movies/quotation-ai/quotation-ai/backend/test_footer_pdf.pdf"
}

try:
    generate_quote(data)
    print("PDF generated successfully.")
except Exception as e:
    print(f"Error generating PDF: {e}")
