from django.urls import path
from . import views  # Correct import statement

urlpatterns = [
    path('', views.first, name='first'),
    path('<int:id>/', views.home, name='home'),  
    path('stats/', views.stats, name='stats'),
    path('sugarPage/', views.sugarPage, name='sugarPage'),
    path('mediPage/', views.mediPage, name='mediPage'),
    path('weightPage/', views.weightPage, name='weightPage'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
     path('about/', views.about_page, name='about_page'),
     path('api/createUser/', views.create_user, name='create_user'),
    path('api/sugarEntry/<int:id>/', views.create_sugar_entry, name='create_sugar_entry'),
    path('api/addMedication/', views.add_medication, name='add_medication'),
    path('api/addWeight/', views.add_weight, name='add_weight'),
    path('signInCheck/', views.signInCheck, name='signInCheck')
    
]
