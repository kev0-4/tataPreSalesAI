import ast
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

# Get the project root directory (assuming the script is in src/data/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Input file path (relative to project root)
input_file_path = os.path.join(project_root, 'data', 'raw', 'extracted_data.txt')

# Output directory and file name (relative to project root)
output_dir = os.path.join(project_root, 'data', 'processed')
output_filename = "extracted_data.pdf"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Full path for the output PDF
output_file_path = os.path.join(output_dir, output_filename)

# Read the input file
try:
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data_str = file.read()
except UnicodeDecodeError:
    # If UTF-8 fails, try with 'latin-1' encoding
    with open(input_file_path, 'r', encoding='latin-1') as file:
        data_str = file.read()

# Parse the string to Python data structure
try:
    car_data = ast.literal_eval(data_str)
except SyntaxError as e:
    print(f"Failed to parse the file content: {e}")
    print("First 500 characters of the file:")
    print(data_str[:500])
    exit()

# Create custom styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

def create_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    story = []

    for item in data:
        for model, qa_list in item.items():
            # Add model name as a heading
            story.append(Paragraph(model, styles['Heading1']))
            story.append(Spacer(1, 12))

            for qa_pair in qa_list:
                for question, answer in qa_pair.items():
                    # Add question as a subheading
                    story.append(Paragraph(question, styles['Heading3']))
                    story.append(Spacer(1, 6))
                    # Add answer as a paragraph
                    story.append(Paragraph(answer, styles['Justify']))
                    story.append(Spacer(1, 12))

            story.append(Spacer(1, 12))

    doc.build(story)
    print(f"PDF has been created: {filename}")

# Create the PDF
create_pdf(car_data, output_file_path)

print(f"Total number of car models: {len(car_data)}")
print(f"Total number of Q&A pairs: {sum(len(qa_list) for item in car_data for qa_list in item.values())}")