from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [


    path('addflip/',views.flip_upload,name='addflip'),
    path('view/',views.yourflips,name='flipsummary'),
    path('<slug:link>/editflip/',views.editflip,name='editflip'),
    path('<slug:link>/deleteflip/',views.deleteflip,name='deleteflip'),
#     path('<slug:link>/customflip/',views.customflip,name='customflip'),
#     path('<slug:link>/customflip/<int:nu>/delete-branding/',views.delete_branding,name='customflip'),
#     path('<slug:link>/refreshflip/',views.refreshflip,name='refreshflip'),
#     path('<slug:link>/viewcounts/',views.viewcounts,name='countflip'),
#     path('<slug:link>/flipprivacy/',views.privacyflip,name='flipprivacy'),
#     path('<slug:link>/flipcollection/',views.collectflip,name='flipcollection'),
#     path('<slug:link>/sview/',views.studentflip,name='studentflip'),
#     path('<slug:link>/removeflip/',views.removeflip,name='removeflip'),
#     path('<slug:link>/shareflip/',views.shareflip,name='shareflip'),
#     path('<slug:link>/sview/saveflip/',views.addtocollections,name='saveflip'),
#     path('<slug:link>/sview/pass-check/',views.passcheck,name='pass-check'),
#     # path('<slug:nu>/delete-branding/',views.delete_branding,name = 'delete-branding')
    
    
]

