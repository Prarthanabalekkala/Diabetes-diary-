from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BSEntry(models.Model):
    MEASURED_CHOICES = [
        ('Before Breakfast', 'Before Breakfast'),
        ('After Breakfast', 'After Breakfast'),
        ('Before Lunch', 'Before Lunch'),
        ('After Lunch', 'After Lunch'),
        ('Before Dinner', 'Before Dinner'),
        ('After Dinner', 'After Dinner'),
    ]

    bpentry_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sugar = models.IntegerField()
    measured = models.CharField(max_length=20, choices=MEASURED_CHOICES)
    entry_date = models.DateField()
    entry_time = models.TimeField()
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"BS Entry for {self.user.name} on {self.entry_date} at {self.entry_time}"

class Medication(models.Model):
    UNIT_CHOICES = [
        ('unit', 'Unit'),
        ('tablet', 'Tablet'),
    ]

    medication_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medication_text = models.CharField(max_length=255)
    unit = models.CharField(max_length=6, choices=UNIT_CHOICES)
    dosage = models.IntegerField()
    medication_date = models.DateField()
    medication_time = models.TimeField()
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Medication for {self.user.name} on {self.medication_date} at {self.medication_time}"

class WeightEntry(models.Model):
    weight_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.IntegerField()
    entry_date = models.DateField()
    entry_time = models.TimeField()
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Weight Entry for {self.user.name} on {self.entry_date} at {self.entry_time}"
