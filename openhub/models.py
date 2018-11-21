from django.db import models


class Contributors(models.Model):

    cid = models.AutoField(primary_key=True)
    user_firstname = models.CharField(max_length=25)
    user_lastname = models.CharField(max_length=25)
    git_username = models.CharField(max_length=255)
    country = models.CharField(max_length=25)
    office = models.CharField(max_length=25)
    user_photo = models.ImageField(upload_to='profile_image', blank=True, default="profile_image/default.png")

    class Meta:
        managed = True
        db_table = 'openhub_contributors'


class RepoDetails(models.Model):

    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=25)
    vcs_url = models.CharField(max_length=500)
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    project_techstack = models.CharField(max_length=500)
    contributor = models.ForeignKey(Contributors, on_delete=models.CASCADE, default="")

    class Meta:
        managed = True
        db_table = 'openhub_repos'



