# Generated by Django 4.1.6 on 2023-06-11 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='personal_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_app.personalinfo'),
        ),
        migrations.AlterField(
            model_name='internshipexperience',
            name='personal_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_app.personalinfo'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='personal_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_app.personalinfo'),
        ),
    ]