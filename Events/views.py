from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Prefetch, Sum
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse


from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

# Create your views here.

def Dashboard(request):
    today = timezone.now().date()

    total_participants = Participant.objects.count()
    total_events = Event.objects.count()

    # Optimized aggregate query
    participant_agg = Event.objects.aggregate(
        total=Count('participants')
    )
    total_event_participants = participant_agg['total']

    upcoming_events = Event.objects.filter(date__gte=today).count()   #_gte = Greater Than or Equal (>=) , today 
    past_events = Event.objects.filter(date__lt=today).count()   #_lt = Less Than (<), today 

    filter_type = request.GET.get('filter')
    if filter_type == 'upcoming':
        today_events = Event.objects.filter(date__gte=today)\
            .select_related('category')\
            .prefetch_related('participants')

    elif filter_type == 'past':
        today_events = Event.objects.filter(date__lt=today)\
            .select_related('category')\
            .prefetch_related('participants')

    elif filter_type == 'total_events':
        today_events = Event.objects.all()\
            .select_related('category')\
            .prefetch_related('participants')

    else:
        today_events = Event.objects.filter(date=today)\
            .select_related('category')\
            .prefetch_related('participants')

    context = {
        'total_participants': total_participants,
        'total_event_participants': total_event_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'today_events': today_events,
        'today': today,
    }
    return render(request, 'dashboard.html', context)



def Category_list(request):
    categories = Category.objects.all() 
    return render(request,'category/list.html',{"categories":categories}) 

def Category_create(request):
    form = CategoryForm.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect("category_list") 
    else:
        form = CategoryForm() 
    
    return render(request,'category/create.html', {"form": form})



def Category_update(request, id): 
    category = Category.objects.get(id=id)

    form = CategoryForm.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST , instance=category) 
        if form.is_valid():
            form.save()
            return redirect("category_list") 
    else:
        form = CategoryForm(instance=category) 
    
    return render(request,'category/update.html', {"form": form})


def Category_delete(request, id):
    form = Category.objects.get(id=id) 
    if request.method == "POST":
        form.delete() 
        return redirect("category_list") 
    return  render(request, "category/delete.html",{"form":form}) 

#...................
# ........Events....
#...................

def Event_list(request):
    search = request.GET.get("search", "")

    events = Event.objects.select_related("category").prefetch_related("participants")

    # Search Feature
    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )

    # Category Filter Feature
    category_filter = request.GET.get("category")
    if category_filter:
        events = events.filter(category__id=category_filter)

    # Date Range Filter
    start = request.GET.get("start")
    end = request.GET.get("end")
    if start and end:
        events = events.filter(date__range=[start, end])

    # Total participant count
    total_participants = Event.objects.aggregate(
        total=Count("participants")
    )["total"]

    return render(request, "events/list.html", {
        "events": events,
        "total_participants": total_participants,
    })
 

def Event_detail(request, id):
    events = ( Event.objects.select_related("category")
    .prefetch_related("participants")
    .get(id=id) 
    )  

    return render(request,'events/detail.html',{"events":events}) 


def Event_create(request):
    # form = EventForm.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect("event_list") 
    else:
        form = EventForm() 
    return render(request, "events/create.html",{"form":form})


def Event_update(request, id): 
    event = Event.objects.get(id=id)
   
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save() 
            return redirect("event_list") 
    else:
        form = EventForm(instance=event) 
    return render(request, "events/create.html",{"form":form})  


def Event_delete(request, id): 
    event = Event.objects.get(id=id)
    
    if request.method == 'POST':
        event.delete() 
        return redirect("event_list") 
     
    return render(request, "events/create.html",{"event":event})  

#...................
# ..Participants....
#...................

def Participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'participants/list.html', {'participants': participants}) 


def Participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)  # instance save কিন্তু M2M এখনো না
            participant.save()                     # instance DB-তে save
            form.save_m2m()                        # ManyToMany (events) save
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participants/create.html', {'form': form})


def Participant_update(request, id):
    participant = Participant.objects.get(id=id)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participants/update.html', {'form': form}) 


def Participant_delete(request, id):
    participant = Participant.objects.get(id=id)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participants/delete.html', {'participant': participant})
