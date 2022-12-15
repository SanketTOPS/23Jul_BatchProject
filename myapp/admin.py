from django.contrib import admin
from .models import userSignup,notes

# Register your models here.
class signupAdmin(admin.ModelAdmin):
    list_display=['firstname','lastname','username','state','city','mobile']

class notesAdmin(admin.ModelAdmin):
    list_display=['title','select','myfiles','comments']

admin.site.register(userSignup,signupAdmin)
admin.site.register(notes,notesAdmin)
