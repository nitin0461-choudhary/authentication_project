from django.contrib import admin
from student.models import Profile,New_Profile,WorkLog
from django.utils.html import format_html
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('id','name','email','password')
# Register your models here.
@admin.register(New_Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('id','name','email','password','resume_file','image_file')
    def view_resume(self, obj):
        if obj.resume_file:
            return format_html(
                '<a href="{}" target="_blank">View PDF</a>', obj.resume_file.url
            )
        return "No file"

    def image_preview(self, obj):
        if obj.image_file:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: contain;"/>',
                obj.image_file.url
            )
        return "No image"

    view_resume.short_description = "Resume"
    image_preview.short_description = "Photo"
@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'morning_work', 'evening_work')
    list_filter = ('date', 'employee')
    search_fields = ('employee__name', 'morning_work', 'evening_work')