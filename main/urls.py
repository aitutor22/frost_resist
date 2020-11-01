from django.urls import path, include

from . import views

app_name = 'main'


urlpatterns = [
    # # about us paths
    # path('about/', views.about, name='about'),
    # path('curriculum/', views.curriculum, name='curriculum'),
    # path('technology/', views.technology, name='technology'),
    # path('teachers/', views.teachers, name='teachers'),

    # # programme paths
    # path('preschool/', views.preschool, name='preschool'),
    # path('lower_primary/', views.lower_primary, name='lower_primary'),
    # path('upper_primary/', views.upper_primary, name='upper_primary'),
    # path('holiday_camps/', views.holiday_camps, name='holiday_camps'),
    # path('online_lesson/', views.online_lesson, name='online_lesson'),

    # path(r'enquiry/', views.create_enquiry, name='create_enquiry'),

    # # other paths
    # path('pricing/', views.pricing, name='pricing'),
    # path('success_stories/', views.success_stories, name='success_stories'),
    # path('contact_us/', views.contact_us, name='contact_us'),
    # path('thank_you/', views.thank_you, name='thank_you'),
    # path('error_enquiry/', views.error_enquiry, name='error_enquiry'),
    path('', views.index, name='index'),
]