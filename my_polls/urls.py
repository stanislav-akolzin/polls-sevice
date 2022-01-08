'''My_polls URLs'''
from django.urls import path
from .import views


app_name = 'my_polls'

urlpatterns = [
    path('api/polls/', views.PollsList.as_view()),
    path('api/get_questions/<int:pk>', views.QuestionsList.as_view()),
    path('api/take_poll/', views.TakePoll.as_view()),
    path('api/get_polls/<int:user_id>', views.GetPolls.as_view()),
]