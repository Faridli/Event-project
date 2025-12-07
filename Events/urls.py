from django.urls import path
from Events.views import ( 
    Dashboard,
    Category_list,
    Category_create,
    Category_update, 
    Category_delete,  
    
    #...................
    # ........Events....
    #................... 
    Event_list, 
    Event_detail,
    Event_create,
    Event_update,
    Event_delete,
    #...................
    # ...Participants...
    #................... 
    Participant_list, 
    Participant_create,
    Participant_update,
    Participant_delete,

)

urlpatterns = [
       path('dashboard/', Dashboard, name='dashboard'),
       path('categories/', Category_list, name='category_list'),
       path('categories/add/', Category_create, name='category_create'),
       path('categories/<int:id>/edit/', Category_update, name='category_update'),
       path('categories/<int:id>/delete/', Category_delete, name='category_delete'), 
       
       #...................
       # ........Events....
       #................... 
       path('event/', Event_list, name='event_list'),
       path('event/detail/<int:id>/detail', Event_detail, name='event_detail'),
       path('event/create/', Event_create, name='event_create'),
       path('event/update/<int:id>/edit/', Event_update, name='event_update'),
       path('event/delete/<int:id>/delete/', Event_delete, name='event_delete'), 

       #...................
       # ...Participants...
       #................... 
       path('participant/', Participant_list, name='participant_list'),
       path('participant/create', Participant_create, name='participant_create'),
       path('participant/update/<int:id>/edit/', Participant_update, name='participant_update'),
       path('participant/delete/<int:id>/delete/', Participant_delete, name='participant_delete'),
      
     ]

