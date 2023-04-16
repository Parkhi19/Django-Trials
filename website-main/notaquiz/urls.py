"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path,include
from exam import views as exam_views
from users import views as user_views
from student import views as st_views
from createquiz import views as createquiz_views
from tutorials import views as tut_views
from safebook import urls as safebook_urls
# from CreateAssignment import urls as assignment_urls
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('exam.urls')),
    path('assign/',include('CreateAssignment.urls')),
     path('tut/',include('tutorials.urls')),
    path('f/',include(safebook_urls)),
    path('certies/',include('certies.urls')),
    path('quizzes/',exam_views.yourquizzes,name='quizzes'),
    path('about/',exam_views.about,name='about'),
    path('about/team/',exam_views.team,name='team'),
    path('resource/',exam_views.resource,name='resource'),
    path('placement/',exam_views.placement_quizzes,name="placement"),
    path('talk-add/',exam_views.add_it,name="add-talk"),
    path('talk-edit/',exam_views.edit_it,name="edit-talk"),
    path('talk-del/',exam_views.delete_it,name="edit-del"),
    path('contact/',exam_views.contact,name='contact'),
    path('contact/save',exam_views.contact_save,name='contactsave'),
    path('contact/join',exam_views.join_save,name='joinus'),
    path('c/',include('createquiz.urls')),
    path('accounts/', include('allauth.urls')),
    path('register/', user_views.register,name='register'),
    path('profile/<int:pk>/', user_views.profile_edit,name='profile'),
    path('login/', user_views.do_login,name='login'),
    path('placement-talks/',createquiz_views.talks,name="placement-talks"),
    path('stdata/',createquiz_views.stdata_tab,name="stdata"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"),name='logout'),
#     path('branding/', user_views.brands,name='branding'),
#     path('delete-brand/', user_views.delete_brand,name='Delete-brand'),
    path('change-password/', user_views.change_password,name='change-password'),
    path('puzzle/',exam_views.puzzle,name='puzzle'),
    path('addpuzzle/',exam_views.addpuzzle,name='addpuzzle'),
    path('hr/',exam_views.hr,name='hr'),
    path('puzzle/like/<int:pk>',exam_views.likes,name='likes'),
    path('hr/like/<int:pk>',exam_views.likes,name='likes'),
    path('do-lower/',user_views.do_lower,name ='do-lower'),
    path('email-verify/', user_views.emailVerify,name='email-verify'),
    path('email-verify/send', user_views.send,name='email-send'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(template_name = 'users/reset.html'),
        name = "password-reset"),
    path('password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name = 'users/reset_done.html'),
        name = "password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name = 'users/reset_confirm.html'),
        name = "password_reset_confirm"),
    path('password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name = 'users/reset_complete.html'),
        name = "password_reset_complete"),
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('',st_views.temppage,name="exam-home"),
#     ]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# handler404 = 'student.views.temppage'


handler404 = 'student.views.error_404'
handler500 = 'student.views.error_500'
handler403 = 'student.views.error_403'
handler400 = 'student.views.error_400'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

