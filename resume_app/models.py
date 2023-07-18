import uuid
from django.db import models

# Create your models here.
class PersonalInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    linked_in_profile_url = models.URLField(max_length=200)
    is_objective_clicked = models.BooleanField(default=False)
    is_education_clicked = models.BooleanField(default=False)
    is_work_experience_clicked = models.BooleanField(default=False)
    is_internship_experience_clicked = models.BooleanField(default=False)
    is_skill_clicked = models.BooleanField(default=False)
    is_award_clicked = models.BooleanField(default=False)
    is_professional_affiliation_clicked = models.BooleanField(default=False)
    is_refrence_clicked = models.BooleanField(default=False)
    is_additional_information_clicked = models.BooleanField(default=False)
    is_job_description_clicked = models.BooleanField(default=False)
    
class Objective(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
    objective = models.TextField()
    
class Education(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=20)
    graduation_date = models.CharField(max_length=20)
    gpa = models.FloatField(default=0)
    coursework = models.CharField(max_length=200)

class WorkExperience(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
    employer_name = models.CharField(max_length=50)
    job_itle = models.CharField(max_length=100)
    employment_dates = models.CharField(max_length=20)
    job_responsibilities  = models.TextField()
    accomplishments  = models.TextField()

class InternshipExperience(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, null=True)
    organization_name = models.CharField(max_length=50)
    role = models.CharField(max_length=100)
    involvement_dates = models.CharField(max_length=20)
    responsibilities  = models.TextField()
    accomplishments  = models.TextField()

class Skill(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
    technical  = models.TextField()
    soft  = models.TextField()

class Award(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
    award = models.CharField(max_length=200)

class ProfessionalAffiliation(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
    professional_affiliations = models.CharField(max_length=200)

class Reference(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
    reference_a = models.CharField(max_length=200)
    reference_b = models.CharField(max_length=200)
    reference_c = models.CharField(max_length=200)

class AdditionalInformation(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
    additional_information = models.TextField()

class JobDescription(models.Model):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE, null=True)
    job_description = models.TextField()
    
class ExistingInformation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    job_description = models.TextField()
    resume = models.TextField()
    