# Generated by Django 5.1.4 on 2024-12-09 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TA_Scheduler', '0005_alter_course_course_code_alter_course_course_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_instructor',
            field=models.ForeignKey(default='john doe', on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='TA_Scheduler.user'),
        ),
    ]