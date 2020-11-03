from django.db import models
from ckeditor.fields import RichTextField

class MotherModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class BELProvince(MotherModel):
    name = models.CharField(max_length=200)
    name_source = models.CharField(max_length=200,blank=True,null=True)
    hasc = models.CharField(max_length=5,blank=True,null=True)
    population = models.IntegerField(default=1)

    ordering = ['name']

    def __str__(self):
        return self.name

class BELAgeGroups(MotherModel):
    name = models.CharField(max_length=200)
    population = models.IntegerField(default=1)
    ordering = ['name']

    def __str__(self):
        return self.name

class BELCases(MotherModel):
    province = models.ForeignKey(BELProvince, on_delete=models.CASCADE)
    date = models.DateField()
    cases0_9 = models.IntegerField(default=0)
    cases10_19 = models.IntegerField(default=0)
    cases20_29 = models.IntegerField(default=0)
    cases30_39 = models.IntegerField(default=0)
    cases40_49 = models.IntegerField(default=0)
    cases50_59 = models.IntegerField(default=0)
    cases60_69 = models.IntegerField(default=0)
    cases70_79 = models.IntegerField(default=0)
    cases80_89 = models.IntegerField(default=0)
    cases90plus = models.IntegerField(default=0)

    ordering = ['province__pk', 'date', 'cases']

    def __str__(self):
        return f"{self.province} {self.date}"
