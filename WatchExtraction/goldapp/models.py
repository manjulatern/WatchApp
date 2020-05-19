from django.db import models

# Create your models here.
class Configuration(models.Model):
    
    gold_c = models.FloatField()
    platinum_c = models.FloatField()
    silver_c = models.FloatField()
    gold_sp = models.FloatField()
    platinum_sp = models.FloatField()
    silver_sp = models.FloatField()
    platinum_bp = models.FloatField()

class GoldPriceWeight(models.Model):
	gold_price = models.FloatField()
	gold_weight = models.FloatField()
	platinum_weight = models.FloatField()
	silver_weight = models.FloatField()
	last_updated = models.DateTimeField()

class CaratInformation(models.Model):
	key_type = models.CharField(max_length=100)
	key = models.CharField(max_length=100)
	value = models.FloatField()

class Coin(models.Model):
	name = models.CharField(max_length=100)
	pure_gold = models.FloatField()
	factor = models.FloatField()