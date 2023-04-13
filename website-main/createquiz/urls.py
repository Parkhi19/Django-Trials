from users.models import Profile
from django.urls import path
from .views import linkcreate
from . import views
from quiz import views as quiz_views 
from django.http import request
from .models import createlink
from student import views as stu_views


urlpatterns = [
    path('',quiz_views.home,name = 'exam-final-home'),
    path('some/',linkcreate,name='createquiz-home'),
    path('<slug:link>/new/<slug:section>',quiz_views.add_question,name='cquiz-new'),
    path('<slug:link>/instructions',quiz_views.timechecker,name='test'),
    path('<slug:link>/test',quiz_views.st_answer,name='test'),
    path('<slug:link>/leaderboard',quiz_views.leaderboard,name='test'),
    path('<slug:link>/settings/',quiz_views.settings,name='settings'),
    path('<slug:link>/detailed-result',stu_views.combined_result,name='test'),
    path('<slug:link>/add-section/',quiz_views.add_section,name="add-section"),
    path('<slug:link>/preview-instructions',quiz_views.instructs,name = 'instructions-preview'),
    path('<slug:link>/res',quiz_views.res,name='result-data'),
    path('<slug:link>/feedback',stu_views.feedback_fun,name = 'feedback'),
    path('<slug:link>/feed',stu_views.render_feed,name = 'allfeed'),
    path('<slug:link>/add_feed',stu_views.add_feed,name = 'addfeed'),
    path('<slug:link>/del_feed/<int:it>',stu_views.delete_feed,name = 'delfeed'),
    path('<slug:link>/update-name',quiz_views.update_name,name='update-name'),
    path('<slug:link>/edit_feed/<int:it>',stu_views.edit_feed,name = 'editfeed'),
    path('<slug:link>/instruction_update',stu_views.instructions_update,name = 'saveInstructions'),
    path('<slug:link>/resd',quiz_views.respect,name='result-delete'),
    path('<slug:link>/resu',quiz_views.result_edit_update,name='result-edit'),
    # path('<slug:link>/stuansupdate',quiz_views.update_stuans,name='update-result'),
    path('<slug:link>/result',stu_views.individual_result,name='results'),
    path('<slug:link>/',quiz_views.home,name='quiz-home'),
    path('<slug:link>/get_question/',quiz_views.json_loader,name='josn-load'),
    path('<slug:link>/edit/<int:qno>',quiz_views.update_question,name='post-update'),
    path('<slug:link>/delete/<int:nu>',quiz_views.delete_question,name='post-delete'),
    path('<slug:link>/delete-quiz/',views.deletelink,name='quiz-delete'),
    path('<slug:link>/delete-section/',views.deletesection,name='section-delete'),
    
]

