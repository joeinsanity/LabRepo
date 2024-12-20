from enum import UNIQUE
from os.path import split

from django.db import models

# Create your models here.
## Some Notes: ##
# - I created this based off of the drawn model.
# - List Classes will store the data.
# - Do NOT use models.ManytoMany
# - This is still in testing
# - SectionList Class may not be needed
## End Notes ##


class Role(models.Model):
    #role_id = models.IntegerField(primary_key=True)# 0 for Admin, 1 for Supervisor, 2 for Teacher, 3 for TA

    role_id = models.CharField(max_length=15, null = True)
    #action_access = models.IntegerField()# each function will have an assigned number


    def __init__(self, role_id, role_name, action_access):
        self.role_id = role_id
        self.role_name = role_name
        self.action_access = action_access

    def __str__(self):
        return self.role_name


class User(models.Model):
    ROLES = (
        ('admin', 'admin'),
        ('instructor', 'instructor'),
        ('TA', 'TA')
    )
    full_name = models.CharField(max_length=50, primary_key=True)
    email = models.CharField(max_length=50, unique = True)
    password = models.CharField(max_length=25)
    phone = models.IntegerField(10, null=True)
    role_id = models.CharField(max_length=10, choices = ROLES, default='admin')
    is_active = models.BooleanField(default=False)# not sure how this will work yet
    skills = models.JSONField(default=list, null=True , blank=True)  # Add this field

    def __str__(self):
        return self.full_name

    def change_email(self, new_email):
        self.email = new_email
        self.save()
        return True

    def change_password(self, new_password):
        self.password = new_password
        self.save()
        return True

    def change_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number
        self.save()
        return True

    def change_name(self, full_name):
        self.full_name
        self.save()
        return True

    def change_role(self, role_id):
        self.role_id = role_id
        self.save()
        return True

    def toggle_active(self):
        self.is_active = not self.is_active
        self.save()
        return self.is_active



# Data Structure Classes
class SectionList(models.Model):
    section_list = []

class courseList(models.Model):
        course_list = []
#     TestS = Section(0, "Lecture")
#     TestC = Course(0, "CS361", [TestS])
#     print(TestC)
#
#
#     def add_Course(self, course):
#         self.course_list.append(course)
#         self.save()
#         return True
#
#     def remove_Course(self, course):
#         self.course_list.remove(course)
#         self.save()
#         return True
#
#     def get_CourseName(self, course_id):
#         return self.course_list[course_id]

class RolesList(models.Model):
    role_list = []

    TA = Role(0, "TA", [0])
    Teacher = Role(1, "Teacher", [1,0])
    Admin = Role(2, "Admin", [-1])# -1 means all access for simplicity
    Supervisor = Role(3, "Supervisor", [3,2,1,0])
    role_list.append(TA)
    role_list.append(Teacher)
    role_list.append(Admin)
    role_list.append(Supervisor)

class UserList(models.Model):
    user_list = []
    #Test = User(0, "John", "Doe", "address@uwm.edu", "Password123!", "4444444444", RolesList.role_list[0])

    def add_User(self, user):
        self.user_list.append(user)
        self.save()
        return True

    def remove_User(self, user):
        self.user_list.remove(user)
        self.save()
        return True

class CheckPermissions(models.Model):

    def check_create_delete_permissions(self, user):
        permissible = ["Admin", "Supervisor"]

        if user.role_id in permissible:
            return True
        return False

    def check_edit_user_permissions(self, user, edited_user):
        permissible = ["Admin", "Supervisor"]
        if user == edited_user:
            return True
        if user.role_id in permissible:
            return True
        return False

    def check_edit_course_permissions(self, user, course):
        permissible = ["Admin", "Supervisor"]
        if user.role_id == "Teacher" and course.course_instructor == user:
            return True
        if user.role_id in permissible:
            return True
        return False


class Validator(models.Model):


    def contains_Special(self, input_str):
        special_characters = "!@#$%^&*()-+?._=,<>/"

        return any(c in special_characters for c in input_str)

    def contains_Letter(self, input_str):
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

        return any(c in letters for c in input_str)

    def contains_Number(self, input_str):
        numbers = "0123456789"

        return any(c in numbers for c in input_str)

    def validate_Password(self, password):

        return (Validator.contains_Special(self, password) and
                ' ' not in password and 8 <= len(password) <= 25
                and Validator.contains_Letter(self, password) and
                Validator.contains_Number(self, password))

    def validate_Email(self, email, emails_list):
        emails_substr = ["uwm.edu","gmail.com"]
        if '@' not in email or ' ' in email or len(email) < 6 or len(email) > 50:
            return False

        a, b = email.split('@',1)

        if not a or Validator.contains_Special(self, a):
            return False

        if b in emails_substr and email not in emails_list:
            return True
        return False

    def validate_phone(self, phone, phone_list):
        if len(str(phone)) != 10:
            return False

        #if Validator.contains_Special(self, phone) or Validator.contains_Letter(self, phone):
            #return False

        if phone not in phone_list:
            return True
        return False


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=50, unique=True)  # name of the course
    course_code = models.CharField(max_length=15, unique=True, null=True)  # course code
    course_sem = models.CharField(max_length=20, null=True)  # course sem

    def __str__(self):
        return self.course_name

    def change_CourseCode(self, course_code):
        self.course_code = course_code
        self.save()
        return True

    def change_CourseSem(self, course_sem):
        self.course_sem = course_sem
        self.save()
        return True

    def change_CourseInstructor(self, course_instructor):
        self.course_instructor = course_instructor
        self.save()
        return True


class Section(models.Model):
    course = models.ForeignKey('Course', related_name='sections', on_delete=models.CASCADE, null=True, blank=True)
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField(null=True)
    type = models.CharField(max_length=20, choices=[('Lecture', 'Lecture'), ('Lab', 'Lab'), ('Tutorial', 'Tutorial')], null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    days = models.CharField(max_length=50, null=True)
    ta = models.CharField(max_length=100, null=True)
    instructor = models.CharField(max_length=100, null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return self.number

    def course_name(self):
        return self.course.course_name
