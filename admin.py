from django.contrib import admin
from .models import Register, Contact, Comment, FitnessRecord

admin.site.register(Register)
admin.site.register(Contact)
admin.site.register(FitnessRecord)

admin.site.register(Comment)



# Register your models here.
