import json
from multiprocessing import context
import re
from time import sleep
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from numpy import append
from restaurant.models import Restaurant, TOP_10_RES
from restaurant.register_functions.load_restaurants import load_restaurants_csv
from restaurant.register_functions.load_reviews import get_reviews
from restaurant.distance_functions.cal_distance import get_distance, check_1km
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView


import random
import googlemaps

googlemaps_key = "AIzaSyCfvx6iYQVGdPer3AqofpSB-jAKnw_PoVE"
gmaps = googlemaps.Client(key=googlemaps_key)

@csrf_exempt
def index(request):
    return render(request, 'restaurant/index.html',)

class RestaurantDetailView(DetailView):
    model = Restaurant

def mypage(request):
    return render(request, 'restaurant/mypage.html',)

def restaurantList(request):
    top_10 = TOP_10_RES.objects.get(pk=1)

    list = top_10.list.split(" ")
    list.pop()

    temp = map(int, list)

    top_10_restaurants = Restaurant.objects.filter(id__in=temp)
    top_10_current = top_10.current.split(" ")

                
    print("temp: ", temp)

    print("top_10:", top_10_restaurants)

    context = {
                'top_10_restaurants': top_10_restaurants, 
                'user_lat': top_10_current[0], 
                'user_lng': top_10_current[1], 
    } 

    print(context)
    return render(request, 'restaurant/restaurantList.html', context)

def load_restaurants_csv(request):
    load_restaurants_csv()

    return render(request)

def update_geo(request):
    
    rs = Restaurant.objects.all()

    for r in rs:
        geo_location = gmaps.geocode(r.address)[0].get('geometry')
        lat = geo_location['location']['lat']
        lng = geo_location['location']['lng']

        r.latitude = lat
        r.hardness = lng 

        r.save()

    print('지리 정보가 업데이트 되었습니다.')

def update_reviews(request):

    rs = Restaurant.objects.all()

    for r in rs:
        get_reviews(r.dong, r.name)

def current_position(request):
    context = {
        'status':200, 
    }
    return render(request, 'restaurant/restaurantList.html', context)

@csrf_exempt
def get_current_coordinate(request):

    if request.method == 'POST':

        coordinate = json.loads(request.body.decode('utf-8'))
        current = [coordinate['user_lat'], coordinate['user_lng']]

        print(current)

        rs = Restaurant.objects.all()

        restaurants = []

        for r in rs:
            destination = [r.latitude, r.hardness]
            distance = get_distance(current, destination)
            if check_1km(distance): 
                restaurants.append(r)

        candidate_restaurants = []
        top_10_restaurants = []
        random_20_restaurants = random.sample(restaurants, 20)

        for r in random_20_restaurants:
            try: 
                visitor_reviews, blog_reviews, link = get_reviews(r.dong, r.name)
                r.visitor_reviews = visitor_reviews
                r.blog_reviews = blog_reviews
                r.total_counts = visitor_reviews + blog_reviews
                r.link = link
                r.save()

                candidate_restaurants.append(r.pk)

                if (len(candidate_restaurants) == 3): 
                    break
            except:
                continue
        
        top_10_restaurants = Restaurant.objects.filter(id__in=candidate_restaurants).order_by('-total_counts')

        result = ""
        
        for r in top_10_restaurants:
            result += str(r.pk)
            result += " "
        

        top_10 = TOP_10_RES.objects.get(pk=1)

        top_10.current = str(current[0]) + " " + str(current[1])
        top_10.list = result 
        
        top_10.save()
        
        context = {
            'top_10_restaurants': top_10_restaurants, 
            'user_lat': coordinate['user_lat'], 
            'user_lng': coordinate['user_lng'], 
        }

        return redirect('/results/')
    else:
        top_10 = TOP_10_RES.objects.get(pk=1)

        list = top_10.list.split(" ")
        list.pop()

        temp = map(int, list)

        temp = map(int, top_10)

        top_10_restaurants = Restaurant.objects.filter(id__in=temp)


        top_10_current = top_10.current.split(" ")

        context = {
                    'top_10_restaurants': top_10_restaurants, 
                    'user_lat': top_10_current[0], 
                    'user_lng': top_10_current[1], 
        } 

        print(context)
        return render(request, 'restaurant/resultRestaurantList.html', context)

def final_results(request): 
    top_10 = TOP_10_RES.objects.get(pk=1)

    list = top_10.list.split(" ")
    list.pop()

    temp = map(int, list)

    top_10_restaurants = Restaurant.objects.filter(id__in=temp)
    top_10_current = top_10.current.split(" ")

                
    print("temp: ", temp)

    print("top_10:", top_10_restaurants)

    context = {
                'top_10_restaurants': top_10_restaurants, 
                'user_lat': top_10_current[0], 
                'user_lng': top_10_current[1], 
    } 

    print(context)

    return render(request, 'restaurant/resultRestaurantList.html', context)




