"""
URL configuration for fit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from fitstore import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('splash_page/', views.splash_page, name="splash_page"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('classes/', views.classes, name="classes"), 
    path('contact/', views.contact, name="contact"),     
    path('gallery/', views.gallery, name="gallery"),    
    path('blog/', views.blog, name="blog"),  
    path('blog-details/', views.details, name="details"),  
    path('blog2/', views.blog_two, name="blog2"),     
    path('blog3/', views.blog_three, name="blog3"),   
    path('comment/', views.comment, name="comment"),     
      
    path('new/', views.new, name="new"),
    path('fitness_dashboard/', views.fitness_dashboard, name="fitness_dashboard"),
    path('user_summary/', views.fitness_summary, name="fitness_summary"),
    path('fitness/chart/', views.fitness_chart, name="fitness_chart"),
    path('fitness/all_chart/', views.fitness_chart, name='fitness_chart_all'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('fitness_result/', views.fitness_result, name='fitness_result'),
    path('user_fitness/', views.user_fitness, name='user_fitness'),
    path('fitness_plan_strategies/', views.plan, name='fitness_plan'),
    path('nutrition_diet/', views.diet, name='diet'),  
    path('mindset/', views.mindset, name='mindset'),
    path('workout/', views.workout, name="workout") ,
    path('weight_loss/', views.weight_loss, name="loss") ,
    path('fat_burn/', views.fat_burn, name="fat_burn"),
    path('yoga_flow/', views.yoga_flow, name="yoga_flow"),
    path('yoga/', views.yoga, name="yoga"),
       
    path('fitness-charts/', views.fitness_charts, name='fitness_charts'),
    path('fitness_chatbot/', views.fitness_chatbot, name='fitness_chatbot'),


]
