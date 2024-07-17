from django.contrib import admin
from .models import User, BSEntry, Medication, WeightEntry

# Register the User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'name', 'email')
    search_fields = ('name', 'email')

# Register the BSEntry model
@admin.register(BSEntry)
class BSEntryAdmin(admin.ModelAdmin):
    list_display = ('bpentry_id', 'user', 'sugar', 'measured', 'entry_date', 'entry_time')
    list_filter = ('measured', 'entry_date')
    search_fields = ('user__name', 'sugar')

# Register the Medication model
@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('medication_id', 'user', 'medication_text', 'unit', 'dosage', 'medication_date', 'medication_time')
    list_filter = ('unit', 'medication_date')
    search_fields = ('user__name', 'medication_text')

# Register the WeightEntry model
@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ('weight_id', 'user', 'weight', 'entry_date', 'entry_time')
    list_filter = ('entry_date',)
    search_fields = ('user__name', 'weight')
