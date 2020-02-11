from django.db import models

# Create your models here.


class Commit(models.Model):
    commit_hash = models.CharField(max_length=40, unique=True)
    branch = models.CharField(max_length=100)
    author = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    datetime_object = models.DateTimeField()
    commit_note = models.CharField(max_length=200)
    file_changed_count = models.IntegerField()
    insertions_count = models.IntegerField()
    deletions_count = models.IntegerField()
    class Meta:
    	ordering = ('-datetime_object',)


    def __str__(self):
    	decoed_branch =  '(' + self.branch + ')'
    	return " ".join([self.commit_hash[:7],decoed_branch,self.commit_note])


