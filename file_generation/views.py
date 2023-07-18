from base64 import b64decode
import os
import uuid
import zipfile
from io import BytesIO
from PyPDF2 import PageObject, PdfWriter
from django.http import FileResponse, HttpResponseNotFound, JsonResponse, HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMessage
from .file_funcs import compile_latex_to_pdf, create_empty_pdf, save_text_file, upload_to_file_io
from .openai_utils import generate_response
from resume_app.models import *
from django.views.decorators.csrf import csrf_exempt
from django_tex.shortcuts import render_to_pdf
from django_tex.core import compile_template_to_pdf
from django.http import FileResponse
from django.views import View
from pylatex import Document


def index(request, pk_id: uuid.UUID):
    context = {
        'user_id' : pk_id 
    }
    return render(request, 'file_generation/index.html', context=context)

def remove_meta_info(data_dict):
    # Filter out keys starting with an underscore
    filtered_dict = {key: value for key, value in data_dict.items() if not key.startswith('_')}
    
    # Recursively remove meta info from nested dictionaries and lists
    for key, value in filtered_dict.items():
        if isinstance(value, dict):
            filtered_dict[key] = remove_meta_info(value)
        elif isinstance(value, list):
            filtered_dict[key] = [remove_meta_info(item) for item in value]
    
    return filtered_dict

@csrf_exempt
def generate(request, pk_id: uuid.UUID):
    if request.method == 'POST':
        existing_information = ExistingInformation.objects.filter(id = pk_id)
        resume_data = None
        job_description = ''
        if existing_information.count() > 0 :
            resume_data = existing_information.first().resume
            job_description = existing_information.first().job_description
        else:
            personal_info = PersonalInfo.objects.get(id = pk_id)
            objective = Objective.objects.filter(personal_info = personal_info).first()
            skills = Skill.objects.filter(personal_info = personal_info).first()
            award = Award.objects.filter(personal_info = personal_info).first()
            personal_affiliation = ProfessionalAffiliation.objects.filter(personal_info = personal_info).first()
            reference = Reference.objects.filter(personal_info = personal_info).first()
            additional_information = AdditionalInformation.objects.filter(personal_info = personal_info).first()
            education = Education.objects.filter(personal_info = personal_info)
            work_experience = WorkExperience.objects.filter(personal_info = personal_info)
            internship_experience = InternshipExperience.objects.filter(personal_info = personal_info)
            job = JobDescription.objects.filter(personal_info = personal_info).first()
            job_description = '' if job is None else job.job_description

            # Convert objects to dictionaries
            personal_info_dict = personal_info.__dict__
            objective_dict = objective.__dict__ if objective is not None else {}
            skills_dict = skills.__dict__ if skills is not None else {}
            award_dict = award.__dict__ if award is not None else {}
            personal_affiliation_dict = personal_affiliation.__dict__ if personal_affiliation is not None else {}
            reference_dict = reference.__dict__ if reference is not None else {}
            additional_information_dict = additional_information.__dict__ if additional_information is not None else {}
            education_list = list(education.values())
            work_experience_list = list(work_experience.values())
            internship_experience_list = list(internship_experience.values())

            # Combine all dictionaries into a single dictionary
            resume_data = {
                'personal_info': personal_info_dict,
                'objective': objective_dict,
                'skills': skills_dict,
                'award': award_dict,
                'personal_affiliation': personal_affiliation_dict,
                'reference': reference_dict,
                'additional_information': additional_information_dict,
                'education': education_list,
                'work_experience': work_experience_list,
                'internship_experience': internship_experience_list
            }
        
        resume_data = remove_meta_info(resume_data)
        # Process the resume data into a single string
        resume = ""

        # resume_prompt = ""
        # cover_letter_prompt = ""
        latex_resume_prompt = ""
        latex_cover_letter_prompt = ""

        if resume_data:
            resume = resume_data
            latex_resume_prompt = f"Generate a complete LaTeX document for a customized resume based on the following information from the applicant's Resume tailored for this Job Description. Ensure that the resume highlights the relevant skills, experience, and interests without adding any new qualifications or past jobs. Please start the LaTeX code with '---' and end it with '---' so we can easily identify and extract it:\n\nApplicant's Resume:\n{resume}\n\nJob Description:\n{job_description}\n\n"

            latex_cover_letter_prompt = f"Generate a complete LaTeX document for a customized cover letter based on the following information from the applicant's Resume tailored for this Job Description. Ensure that the cover letter emphasizes the applicant's relevant skills, experiences, and interests without adding any new qualifications or past jobs. Please start the LaTeX code with '---' and end it with '---' so we can easily identify and extract it:\n\nApplicant's Resume:\n{resume}\n\nJob Description:\n{job_description}\n\n"
        else:
            # Process resume form fields
            for key in resume_data:
                value = resume_data.get(key)
                if value == "":
                    continue
                if isinstance(value, list):
                    for i, instance in enumerate(value):
                        resume += f"{key} {i+1} responses: ("
                        for sub_key in instance:
                            sub_value = instance[sub_key]
                            resume += f"{sub_key}: {sub_value}, "
                        resume = resume[:-2]
                        resume += "), "
                else:
                    resume += f"{key}: {value}, "

            latex_resume_prompt = f"Generate a complete LaTeX document for a customized resume based on the following information only from the applicant's field fields in the Resume form tailored for this Job Description. Ensure that the resume highlights the relevant skills, experience, and interests without adding any new qualifications or past jobs. Please start the LaTeX code with '---' and end it with '---' so we can easily identify and extract it:\n\nApplicant's Resume:\n{resume}\n\nJob Description:\n{job_description}\n\n"

            latex_cover_letter_prompt = f"Generate a complete LaTeX document for a customized cover letter based on the following information only from the applicant's field fields in the Resume form tailored for this Job Description. Ensure that the cover letter emphasizes the applicant's relevant skills, experiences, and interests without adding any new qualifications or past jobs. Please start the LaTeX code with '---' and end it with '---' so we can easily identify and extract it:\n\nApplicant's Resume:\n{resume}\n\nJob Description:\n{job_description}\n\n"

        # Call OpenAI API to generate the LaTeX code for resume and cover letter
        resume_latex = generate_response(latex_resume_prompt)
        cover_letter_latex = generate_response(latex_cover_letter_prompt)

        # Process LaTeX response
        resume_latex = resume_latex.split('---')[1].strip()
        cover_letter_latex = cover_letter_latex.split('---')[1].strip()

        # Save LaTeX code to text files
        resume_latex_file = save_text_file(resume_latex, f'{pk_id}_resume.tex')
        cover_letter_latex_file = save_text_file(cover_letter_latex, f'{pk_id}_cover_letter.tex')

        resume_zip = f"file_generation/tex_templates/{pk_id}_resume.zip"
        cover_letter_zip = f"file_generation/tex_templates/{pk_id}_cover_letter.zip"
        with zipfile.ZipFile(resume_zip, "w") as zf:
            zf.write(resume_latex_file)
        with zipfile.ZipFile(cover_letter_zip, "w") as zf:
            zf.write(cover_letter_latex_file)

        # Upload LaTeX files to file.io and get the download links
        resume_zip_url = upload_to_file_io(resume_zip)
        cover_letter_zip_url = upload_to_file_io(cover_letter_zip)

        # Compile LaTeX to PDF
        
        resume_zip = f"file_generation/tex_templates/{pk_id}_resume.pdf"
        cover_letter_zip = f"file_generation/tex_templates/{pk_id}_cover_letter.pdf"
        resume_pdf_file = compile_latex_to_pdf(resume_latex, resume_latex_file)
        cover_letter_pdf_file = compile_latex_to_pdf(cover_letter_latex, cover_letter_latex_file)

        # Close and delete temporary files
        # os.remove(resume_latex_file)
        # os.remove(cover_letter_latex_file)
        # os.remove(resume_pdf_file)
        # os.remove(cover_letter_pdf_file)

        # Prepare the response
        
        # template_name = 'file_generation/tex_templates/'+ '' + f'{pk_id}_resume.tex'
        # context = resume_data
        # pdf = compile_template_to_pdf(template_name, context)
        # return PDFResponse()
        # return render_to_pdf(request, resume_latex_file, context,
        #             filename=f'{pk_id}_resume.pdf')
        # zip_buffer.seek(0)
        response = JsonResponse({
            'resume_zip_url': resume_zip_url,
            'cover_letter_zip_url': cover_letter_zip_url,
            })
        # response['Content-Disposition'] = 'attachment; filename=documents.zip'
        return response

    return JsonResponse({'message': 'Invalid request method.'})

@csrf_exempt
def download_pdf(request, pk_id:uuid.UUID):
    # Define the path to the LaTeX file
    latex_file_path = f"file_generation\\tex_templates\\{pk_id}_resume.tex"
# D:\Replite\smart_c\file_generation\tex_templates\21cb08f9-05b4-471a-8c84-1b70ea556cb4_resume.tex
    # Generate the PDF file
    pdf_file_path = generate_pdf(latex_file_path)
 
    # Compile LaTeX to PDF
    # resume_pdf_file = compile_latex_to_pdf(resume_latex, resume_latex_file)
    # cover_letter_pdf_file = compile_latex_to_pdf(cover_letter_latex, cover_letter_latex_file)

    # Create a file response for the PDF file
    response = FileResponse(open(pdf_file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pk_id}_resume.pdf"'

    # Return the file response
    return response

@csrf_exempt
def download_pdf_file(request, pk_id:uuid.UUID, file_type:str):
    # Define the file path
    file_path = f"file_generation/tex_templates/{pk_id}_{file_type}.pdf"

    if os.path.exists(file_path):
        # Open the file and create a FileResponse
        file = open(file_path, 'rb')
        response = FileResponse(file, content_type='application/pdf')

        # Set the appropriate attachment header
        response['Content-Disposition'] = f'attachment; filename="{pk_id}_{file_type}.pdf"'

        return response
    else:
        return HttpResponseNotFound("PDF file not found")

def generate_pdf(latex_file_path):
    # Read the latex file contents
    with open(latex_file_path, 'r') as file:
        content = file.read()
    
    decoded_pdf_content = b64decode(content)

    # Remove the file extension from the text file name
    pdf_file_path = latex_file_path.rsplit('.', 1)[0] + '.pdf'

    # Create a new PDF writer
    pdf_writer = PdfWriter()

    # # Create a new page object
    # page = PageObject.create_blank_page(width=200, height=200)
    # page.merge_page(pdf_writer.create_page_from_text(content))

    # Add the page to the PDF writer
    pdf_writer.add_page(decoded_pdf_content)

    # Create a new page and add the  content to it
    # pdf_writer.add_page()
    # pdf_writer.add_text(10, 10, content)

    # Save the PDF file
    with open(pdf_file_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

    return pdf_file_path

def upload(request, pk_id: uuid.UUID):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # Save the file to file.io
        file_io_url = upload_to_file_io(uploaded_file)

        return JsonResponse({'url': file_io_url})

    return JsonResponse({'message': 'Invalid request method.'})
