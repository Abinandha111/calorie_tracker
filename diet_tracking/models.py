from django.db import models

# Create your models here.
from accounts.models import User
class FoodLog(models.Model):

    title = models.CharField(max_length=200,null=True)

    quantity = models.CharField(max_length=200)

    MEAL_OPTIONS = [
        ("breakfast","breakfast"),
        ("lunch","lunch"),
        ("snack","snack"),
        ("dinner","dinner"),
    ]

    meal_type = models.CharField(max_length=200,choices=MEAL_OPTIONS,default="breakfast")

    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    food_image = models.ImageField(upload_to="food",null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    calorie = models.FloatField()

    