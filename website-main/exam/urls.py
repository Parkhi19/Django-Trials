from django.urls import path
from . import views
from quiz import views as quiz_views

urlpatterns = [
    path('',views.home,name = 'exam-home'),
    path('announce-edit',views.announce_edit,name = 'edit-announce'),
    path('announce-add',views.announce_add,name = 'add-announce'),
    path('announce-change/<int:that>',views.announce_change,name = 'change-announce'),
    path('announce-del/<int:that>',views.announce_del,name = 'del-announce'),
    
    # path('<slug:link>/',quiz_views.home,name='quiz-home'),
    # path('<slug:link>/edit/<int:pk>',quiz_views.PostUpdateView.as_view(),name='post-update'),
    # path('<slug:link>/delete/<int:pk>',quiz_views.PostDeleteView.as_view(),name='post-delete'),
]
