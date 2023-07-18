from django.shortcuts import render, redirect
import uuid

from .models import AdditionalInformation, Award, Education, ExistingInformation, InternshipExperience, JobDescription, Objective, PersonalInfo, ProfessionalAffiliation, Reference, Skill, WorkExperience


# Create your views here.
def home_view(request):
    user_id = uuid.uuid4()
    return redirect('personal_info', user_id)

def personal_info_view(request, pk_id: uuid.UUID):
    personal_info, is_found = PersonalInfo.objects.get_or_create(id = pk_id)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        linkedin = request.POST.get('linkedin')
        
        # Create a new instance of PersonalInfo model and save the form data
        personal_info = PersonalInfo(
            id = pk_id,
            name=full_name,
            address=address,
            phone_number=phone_number,
            email=email,
            linked_in_profile_url=linkedin,
        )
        personal_info.save()
        return redirect('objective', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/personal_info.html', context=context)


def objective_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_objective_clicked = True
    personal_info.save()
    if request.method == 'POST':
        objective_text = request.POST.get('objective')
        objective = Objective(
            objective=objective_text,
            personal_info = personal_info
        )
        objective.save()

        return redirect('education', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/objective.html', context=context)

# TODO:: handle field of study aswell
def education_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_education_clicked = True
    personal_info.save()
    if request.method == 'POST':
        institute_names = request.POST.getlist('institute_name')
        degrees = request.POST.getlist('degree')
        graduation_dates = request.POST.getlist('graduation_date')
        gpas = request.POST.getlist('gpa')
        certifications = request.POST.getlist('certifications')
        num_forms = len(institute_names)
        for i in range(num_forms):
            try:
                degree_to_add = degrees[i]
            except Exception as e:
                degree_to_add = '' 
            try:
                graduation_date_to_add=graduation_dates[i] 
            except Exception as e:
                graduation_date_to_add = '' 
            try:
                gpa_to_add=gpas[i] 
            except Exception as e:
                gpa_to_add = 0
            try:
                certification_to_add=certifications[i]
            except Exception as e:
                certification_to_add = '' 

            education = Education(
                personal_info = personal_info,
                field_of_study = '',
                name=institute_names[i],
                degree=degree_to_add,
                graduation_date=graduation_date_to_add,
                gpa=gpa_to_add,
                coursework=certification_to_add
            )
            education.save()

        return redirect('work_experience', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/education.html',  context=context)


def work_experience_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_work_experience_clicked = True
    personal_info.save()
    if request.method == 'POST':
        employer_names = request.POST.getlist('employer_name')
        job_titles = request.POST.getlist('job_title')
        employment_dates = request.POST.getlist('employment_date')
        job_resps = request.POST.getlist('job_resp')
        accomplishments = request.POST.getlist('accomplishments')
        num_forms = len(employer_names)
        for i in range(num_forms):
            try:
                accomplishment_to_add = accomplishments[i]
            except Exception as e:
                accomplishment_to_add = '' 
            try:
                job_title_to_add=job_titles[i] 
            except Exception as e:
                job_title_to_add = '' 
            try:
                employment_date_to_add=employment_dates[i] 
            except Exception as e:
                employment_date_to_add = ''
            try:
                job_resp_to_add=job_resps[i]
            except Exception as e:
                job_resp_to_add = '' 

            work_experience = WorkExperience(
                personal_info = personal_info,
                employer_name=employer_names[i],
                job_itle=job_title_to_add,
                employment_dates=employment_date_to_add,
                job_responsibilities=job_resp_to_add,
                accomplishments=accomplishment_to_add
            )
            work_experience.save()

        return redirect('internship', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/work_experience.html', context=context)


def internship_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_internship_experience_clicked = True
    personal_info.save()
    if request.method == 'POST':
        organization_names = request.POST.getlist('organization_name')
        positions = request.POST.getlist('position')
        involvement_dates = request.POST.getlist('involvement_date')
        job_resps = request.POST.getlist('job_resp')
        accomplishments = request.POST.getlist('accomplishments')
        num_forms = len(organization_names)
        for i in range(num_forms):
            try:
                accomplishment_to_add = accomplishments[i]
            except Exception as e:
                accomplishment_to_add = '' 
            try:
                position_to_add=positions[i] 
            except Exception as e:
                position_to_add = '' 
            try:
                involvement_date_to_add=involvement_dates[i] 
            except Exception as e:
                involvement_date_to_add = ''
            try:
                job_resp_to_add=job_resps[i]
            except Exception as e:
                job_resp_to_add = '' 

            internship_experience = InternshipExperience(
                personal_info = personal_info,
                organization_name=organization_names[i],
                role=position_to_add,
                involvement_dates=involvement_date_to_add,
                job_responsibilities=job_resp_to_add,
                accomplishments=accomplishment_to_add
            )
            internship_experience.save()

        return redirect('skills', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/internship.html', context=context)


def skills_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_skill_clicked = True
    personal_info.save()
    if request.method == 'POST':
        tech_skills = request.POST.get('tech_skills')
        soft_skills = request.POST.get('soft_skills')
        
        # Create a new instance of PersonalInfo model and save the form data
        skill = Skill(
            personal_info = personal_info,
            technical=tech_skills,
            soft=soft_skills,
        )
        skill.save()
        return redirect('awards', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/skills.html', context=context)


def awards_view(request, pk_id: uuid.UUID):
    
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_award_clicked = True
    personal_info.save()
    if request.method == 'POST':
        awards_list = request.POST.get('awards_list')
        
        award = Award(
            personal_info = personal_info,
            award=awards_list,
        )
        award.save()
        return redirect('affiliations', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/awards.html', context=context)


def affiliations_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_professional_affiliation_clicked = True
    personal_info.save()
    if request.method == 'POST':
        affiliations_list = request.POST.get('affiliations_list')
        
        professional_affiliation = ProfessionalAffiliation(
            personal_info = personal_info,
            professional_affiliations=affiliations_list,
        )
        professional_affiliation.save()
        return redirect('references', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/affiliations.html',context=context)


def references_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_refrence_clicked = True
    personal_info.save()
    if request.method == 'POST':
        reference_c = request.POST.get('reference_c')
        reference_a = request.POST.get('reference_a')
        reference_b = request.POST.get('reference_b')
        
        # Create a new instance of PersonalInfo model and save the form data
        reference = Reference(
            personal_info = personal_info,
            reference_a=reference_a,
            reference_b=reference_b,
            reference_c=reference_c
        )
        reference.save()
        return redirect('additional_info', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/references.html', context=context)


def additional_info_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_additional_information_clicked = True
    personal_info.save()
    if request.method == 'POST':
        additional_info = request.POST.get('additional_info')
        additional_information_to_add = AdditionalInformation(
            personal_info = personal_info,
            additional_information=additional_info,
        )
        additional_information_to_add.save()
        return redirect('job_description', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/additional_info.html',context=context)


def job_description_view(request, pk_id: uuid.UUID):
    personal_info = PersonalInfo.objects.get(id = pk_id)
    personal_info.is_job_description_clicked = True
    personal_info.save()
    if request.method == 'POST':
        job_des = request.POST.get('job_des')
        exists = JobDescription.objects.filter(personal_info=personal_info).count()
        if exists < 1:
            job_description = JobDescription(
                personal_info=personal_info,
                job_description=job_des,
            )
            job_description.save()
        return redirect('file_processing', pk_id)
    context = {
        'user_id': pk_id,
        'personal_info': personal_info
    }
    return render(request, 'resume_app/job_description.html', context=context)


def existing_resume_view(request):    
    if request.method == 'POST':
        job_des = request.POST.get('job_des')
        resume = request.POST.get('resume')
        user_id = uuid.uuid4()
        existing_information = ExistingInformation(
            id = user_id,
            job_description=job_des,
            resume = resume
        )
        existing_information.save()
        return redirect('file_processing', user_id)

    context = {
    }
    return render(request, 'resume_app/existing_resume.html', context=context)

def landing_page(request):
    context = {
    }
    return render(request, 'resume_app/landing.html', context=context)