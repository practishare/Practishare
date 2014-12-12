from django.contrib import admin
from practices.models import Subject, Practice, Axis

class AxisInline(admin.StackedInline):
    model = Axis
    max_num = 2

class SubjectAdmin(admin.ModelAdmin):
    inlines = [AxisInline,]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Practice)
