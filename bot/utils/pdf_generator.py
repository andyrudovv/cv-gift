from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import json

async def create_cv_pdf(cv_data: dict | str, filename: str) -> str:
    # Ensure cv_data is a dictionary
    if isinstance(cv_data, str):
        try:
            cv_data = json.loads(cv_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")
    
    if not isinstance(cv_data, dict):
        raise ValueError("CV data must be a dictionary or valid JSON string")

    # Create the PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Initialize story and styles
    story = []
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2C3E50')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
        textColor=colors.HexColor('#34495E')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12
    )
    
    # Add content sections
    # Name
    story.append(Paragraph(str(cv_data.get('name', '')), title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Introduction
    story.append(Paragraph('Introduction', heading_style))
    story.append(Paragraph(str(cv_data.get('intro', '')), normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Experience
    story.append(Paragraph('Experience', heading_style))
    story.append(Paragraph(str(cv_data.get('experience', '')), normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Education
    story.append(Paragraph('Education', heading_style))
    story.append(Paragraph(str(cv_data.get('education', '')), normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Technical Skills
    story.append(Paragraph('Technical Skills', heading_style))
    tech_stack = cv_data.get('tech_stack', [])
    if isinstance(tech_stack, list):
        tech_stack_text = ', '.join(str(skill) for skill in tech_stack)
    else:
        tech_stack_text = str(tech_stack)
    story.append(Paragraph(tech_stack_text, normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Summary
    story.append(Paragraph('Professional Summary', heading_style))
    story.append(Paragraph(str(cv_data.get('summary', '')), normal_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Wishes/Career Objectives
    story.append(Paragraph('Career Objectives', heading_style))
    story.append(Paragraph(str(cv_data.get('wishes', '')), normal_style))
    
    # Build and save the PDF
    doc.build(story)
    return filename