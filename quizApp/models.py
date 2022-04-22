from django.db import models

# Master record
class Master(models.Model):
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=12)
    IsActive = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'master'


gender_choice = (
    ('m', 'male'),
    ('f', 'female'),
)
class Profile(models.Model):
    Master = models.ForeignKey(Master, on_delete=models.CASCADE)
    ProfileImage = models.FileField(upload_to="profile/", default="default.png")
    FullName = models.CharField(max_length=50, default='')
    Mobile = models.CharField(max_length=10, default='')
    Gender = models.CharField(max_length=6, choices=gender_choice)
    City = models.CharField(max_length=50, default='')
    State = models.CharField(max_length=50, default='')
    AdderssLine = models.CharField(max_length=150, default='')

    class Meta:
        db_table = 'profile'

class Category(models.Model):
    Name = models.CharField(max_length=25)

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'

class QuesSet(models.Model):
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quesset'

class OptionSet(models.Model):
    QuesSet = models.ForeignKey(QuesSet, on_delete=models.CASCADE)
    Question = models.CharField(max_length=255)
    Options = models.TextField(max_length=255)
    Correct = models.CharField(max_length=4)
    Point = models.IntegerField()
    DateCreated = models.DateTimeField(auto_now_add=True)
    LastUpdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'optionset'