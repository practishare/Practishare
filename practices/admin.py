from django import forms
from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from practices.models import *

class AxisValueInline(NestedTabularInline):
    model = AxisValue
    extra = 1

class AxisInline(NestedStackedInline):
    model = Axis
    inlines = [AxisValueInline]
    extra = 1

class FieldInline(NestedTabularInline):
    model = Field
    extra = 0

class SubjectAdmin(NestedModelAdmin):
    exclude = ["id"]
    inlines = [AxisInline, FieldInline]

class PracticeFieldInline(NestedTabularInline):
    model = PracticeFieldValue
    extra = 0

class PracticeAxisInline(NestedTabularInline):
    model = PracticeAxisValue
    extra = 0

class PracticeAdmin(NestedModelAdmin):
    inlines = [PracticeAxisInline, PracticeFieldInline]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Practice, PracticeAdmin)
admin.site.register(Comment)
