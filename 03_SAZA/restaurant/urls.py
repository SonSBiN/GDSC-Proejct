from django.urls import path, include
from restaurant.views import index, mypage, restaurantList, final_results, get_current_coordinate, load_restaurants_csv, update_geo, update_reviews, RestaurantDetailView

app_name = 'restaurant'

urlpatterns = [
    path('', index, name='index'), 
    path('mypage/', mypage, name='mypage'), 
    path('load-restaurants/', load_restaurants_csv, name='load_restaurants'),
    path('restaurantList/', restaurantList, name='restaurantList'), 
    path('update-geo/', update_geo, name='update_geos'),
    path('update-reviews/', update_reviews, name='update_reviews'), 
    path('results/', final_results, name='final_results'),
    path('get-current-coordinate/', get_current_coordinate, name='get_current_coordinate'), 
    path('<int:pk>/', RestaurantDetailView.as_view(), name='article-detail'),
]
