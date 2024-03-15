import fitz  # PyMuPDF

def extract_resume_data(pdf_path):
    extracted_text = []

    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            text = page.get_text()
            # Split text by spaces to get each word
            words = text.split()
            extracted_text.extend(words)        

    return extracted_text

def extractDetails(filepath):
    pdf_path = filepath

    # Extract data from the resume PDF
    resume_data = extract_resume_data(pdf_path)
    fields=['Education','EDUCATION','Achievements','ACHIEVEMENTS','Projects','PROJECTS','Languages','LANGUAGES','Online','ONLINE','Profiles','PROFILES','TECHNICAL']
    # Print each word separately
    index=resume_data.index('SKILLS')
    skills=[]
    for i in range(index+1,len(resume_data)):
        if resume_data[i] in fields:
            break
        skills.append(resume_data[i])
    with open('sharing.txt','w',  encoding='utf-8') as file:
        for item in skills:
            file.write(item+ '\n')