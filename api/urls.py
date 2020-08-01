from django.urls import path
from . import views


urlpatterns = [
    path('' , views.get_last_cover_before_search),
    path('render/' ,views.get_last_cover)
    # path('new/' , views.new)
] 
