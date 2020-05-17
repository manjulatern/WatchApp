from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from datetime import datetime

from .models import *

# Create your views here.
def home(request):
	template = loader.get_template('gold/home.html')

	#Populate Gold Price Weight using curl
	gold_price_weight = populate_gold_price()
	
	# Load Carat Information
	carat_gold = CaratInformation.objects.filter(key_type='gold')
	carat_silver = CaratInformation.objects.filter(key_type='silver')
	
	# Load Configuration
	config = Configuration.objects.all().first()
	
	#Load grams data
	grams_data = calculate_grams(config,gold_price_weight)

	context = {
		'carat_gold': carat_gold,
		'carat_silver':carat_silver,
		'gold_price_weight': gold_price_weight,
		'config':config,
		'grams_data':grams_data
		}
	return HttpResponse(template.render(context, request))

def populate_gold_price():
	gold_price_weight = GoldPriceWeight.objects.all().first()
	if not gold_price_weight:
		gold_price_weight = GoldPriceWeight()

	gold_price = 44.00

	gold_weight = 1706.00
	platinum_weight = 894.00
	silver_weight = 15.00
	last_updated = datetime.now()

	gold_price_weight.gold_price = gold_price
	gold_price_weight.gold_weight = gold_weight
	gold_price_weight.platinum_weight = platinum_weight
	gold_price_weight.silver_weight = silver_weight
	gold_price_weight.last_updated = last_updated
	gold_price_weight.save()
	return gold_price_weight

def update_configuration(request):
	if request.method == "POST":
		config = Configuration.objects.all().first()
		if not config:
			config = Configuration()
		print(config)
		gold_c = request.POST.get('gold_c')
		platinum_c = request.POST.get('platinum_c')
		silver_c = request.POST.get('silver_c')
		gold_sp = request.POST.get('gold_sp')
		platinum_sp = request.POST.get('platinum_sp')
		silver_sp = request.POST.get('silver_sp')
		platinum_bp = request.POST.get('platinum_bp')

		config.gold_c = gold_c
		config.platinum_c = platinum_c
		config.silver_c = silver_c
		config.gold_sp = gold_sp
		config.silver_sp = silver_sp
		config.platinum_sp = platinum_sp
		config.platinum_bp = platinum_bp
		print(config)
		config.save()

		return redirect('/gold')

def calculate_grams(config,gold_price_weight):

	calc_data = []
	kilos = []

	#Calculating Kilos with 32.15
	gold_k = round(gold_price_weight.gold_weight * 32.15,2)
	silver_k = round(gold_price_weight.silver_weight * 32.15,2)
	platinum_k = round(gold_price_weight.platinum_weight * 32.15,2)
	kilos.append(gold_k)
	kilos.append(platinum_k)
	kilos.append(silver_k)
	calc_data.append(kilos)

	purity = []
	#Calculating Purity
	gold_purity = round(gold_k * (config.gold_sp/100),2)
	platinum_purity = round(platinum_k * (config.platinum_sp/100),2)
	silver_purity = round(silver_k * (config.silver_sp/100),2)
	purity.append(gold_purity)
	purity.append(platinum_purity)
	purity.append(silver_purity)
	calc_data.append(purity)
	
	comission = []
	#Calculating Comission
	gold_comission = round(gold_purity * (1-(config.gold_c/100)),2)
	platinum_comission = round(platinum_purity * (1- (config.platinum_c/100)),2)
	silver_comission = round(silver_purity * (1-(config.silver_c/100)),2)
	comission.append(gold_comission)
	comission.append(platinum_comission)
	comission.append(silver_comission)
	calc_data.append(comission)
	
	grams = []
	#Calculating Grams
	for i in comission:
		grams.append(round(i/1000,2))
	
	calc_data.append(grams)
	
	return calc_data




