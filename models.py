from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'register'

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    comment = models.TextField()

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return f"{self.name} - {self.email}"

class FitnessRecord(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    date = models.DateField()

    # Raw input fields
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    sleep_hours = models.FloatField()
    water_intake_liters = models.FloatField()
    workout_duration_mins = models.FloatField()
    steps_walked = models.FloatField()
    calories_burned = models.FloatField()
    total_calories_intake_est = models.FloatField()
    avg_heart_rate_bpm = models.FloatField()
    protein_intake_g = models.FloatField()
    carb_intake_g = models.FloatField()
    fat_intake_g = models.FloatField()

    # Calculated fields
    bmi = models.FloatField()
    bmi_status = models.CharField(max_length=50)

    calorie_balance = models.FloatField()
    caloriebalance_status = models.CharField(max_length=100)

    hydration_score = models.FloatField()
    hydration_status = models.CharField(max_length=100)

    sleep_score = models.FloatField()
    sleep_status = models.CharField(max_length=100)

    nutrition_score = models.FloatField()
    nutrition_status = models.CharField(max_length=100)

    steps_score = models.FloatField()
    steps_status = models.CharField(max_length=100)

    workout_score = models.FloatField()
    workout_status = models.CharField(max_length=100)

    fitness_score = models.FloatField()

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Fitness_report'
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_user_fitness_date')
        ]

    def __str__(self):
        return f"{self.user.email} - {self.date} (Score: {self.fitness_score})"