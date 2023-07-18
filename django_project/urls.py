"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from file_generation.views import download_pdf_file, upload, index, generate
from resume_app.views import additional_info_view, affiliations_view, awards_view, education_view, existing_resume_view, home_view, internship_view, job_description_view, objective_view, personal_info_view, references_view, skills_view, work_experience_view, landing_page
# from file
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', home_view, name='create_new'),
    path('', landing_page, name='landing'),
    path('personal_info/<uuid:pk_id>/', personal_info_view, name='personal_info'),
    path('objective/<uuid:pk_id>/', objective_view, name='objective'),
    path('education/<uuid:pk_id>/', education_view, name='education'),
    path('work_experience/<uuid:pk_id>/', work_experience_view, name='work_experience'),
    path('internship/<uuid:pk_id>/', internship_view, name='internship'),
    path('skills/<uuid:pk_id>/', skills_view, name='skills'),
    path('awards/<uuid:pk_id>/', awards_view, name='awards'),
    path('affiliations/<uuid:pk_id>/', affiliations_view, name='affiliations'),
    path('references/<uuid:pk_id>/', references_view, name='references'),
    path('additional_info/<uuid:pk_id>/', additional_info_view, name='additional_info'),
    path('job_description/<uuid:pk_id>/', job_description_view, name='job_description'),
    path('existing_resume/', existing_resume_view, name="existing_resume"),
    path('download-pdf/<uuid:pk_id>/<str:file_type>/', download_pdf_file, name='download_pdf'),
    path('file_processing/generate/<uuid:pk_id>/', generate, name='generate'),
    path('file_processing/upload/<uuid:pk_id>/', upload, name='upload'),
    path('file_processing/<uuid:pk_id>/', index, name="file_processing"),
    # path('latex-files/<path:filename>', serve_latex_files),
    # path('api/generate-pdf', generate_pdf),
]
