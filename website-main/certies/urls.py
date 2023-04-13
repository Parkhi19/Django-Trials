from django.urls import path
from . import views
from quiz import views as quiz_views

urlpatterns = [
    path('add-certi/',views.add_certi,name = 'add-certi'),
    path('all-certi/',views.all_certi,name = 'all-certi'),
    path('verify-certi/<code>',views.verify_certi,name = 'verify-certi'),

]
