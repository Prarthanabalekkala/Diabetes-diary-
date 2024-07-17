from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


from django.shortcuts import render, redirect
from django.db.models import Avg
from datetime import datetime, timedelta
from django.utils import timezone
from .models import BSEntry, User, Medication, WeightEntry  # Adjust the import path according to your project structure
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import User, Medication


def home(request, id):
    return render(request,"management/index.html", {"data" :id})

def stats(request):
    # Get the start and end of the current week
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)


    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)
    end_of_month = next_month - timedelta(days=next_month.day)

    # Define meal timings for aggregation
    MEAL_TIMINGS = [
        ('Before Breakfast', 'Before_Breakfast'),
        ('After Breakfast', 'After_Breakfast'),
        ('Before Lunch', 'Before_Lunch'),
        ('After Lunch', 'After_Lunch'),
        ('Before Dinner', 'Before_Dinner'),
        ('After Dinner', 'After_Dinner'),
    ]

    # Calculate average sugar levels for each meal timing
    weekly_details = {}
    for timing_key, timing_display in MEAL_TIMINGS:
        avg_sugar = BSEntry.objects.filter(
            measured=timing_key,
            entry_date__range=[start_of_week, end_of_week]
        ).aggregate(avg_sugar=Avg('sugar'))['avg_sugar']
        weekly_details[timing_display] = avg_sugar

    # Pass the calculated details to the template
    # print(weekly_details)
    monthly_details = {}
    for timing_key, timing_display in MEAL_TIMINGS:
        avg_sugar = BSEntry.objects.filter(
            measured=timing_key,
            entry_date__range=[start_of_month, end_of_month]
        ).aggregate(avg_sugar=Avg('sugar'))['avg_sugar']
        monthly_details[timing_display] = avg_sugar
    context = {
        'weekly_details': weekly_details,
        'monthly_details': monthly_details
    }
    return render(request, 'management/statistics.html', context)


def sugarPage(request):
    return render(request, "management/sugar.html")

def create_sugar_entry(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)

        id = int(id)
        sugar = data.get('sugar')
        measured = data.get('measured')
        entry_date = data.get('entry_date')
        entry_time = data.get('entry_time')
        notes = data.get('notes')
        entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
        entry_time = datetime.strptime(entry_time, '%H:%M:%S').time()
        
        # print(sugar,measured,entry_date,entry_time,notes)
        # Assuming you have a logged-in user
        #  = request.user
        # user =        
        # entry_date = entry_date
        user = get_object_or_404(User, pk=id) 
        print(user)
        # Create BSEntry object
        bs_entry = BSEntry.objects.create(
            user=user,
            sugar=sugar,
            measured=measured,
            entry_date=entry_date,
            entry_time=entry_time,
            notes=notes
        )
        
        # Return a JSON response indicating success
        return JsonResponse({'message': 'Data saved successfully!'})
    
    # Handle other request methods or errors here
    return JsonResponse({'error': 'Invalid request method'})

def mediPage(request):
    return render(request,"management/medication.html")

def add_medication(request):
    if request.method == 'POST':
        medication_text = request.POST.get('medication_text')
        unit = request.POST.get('unit')
        dosage = request.POST.get('dosage')
        medication_date = request.POST.get('medication_date')
        medication_time = request.POST.get('medication_time')
        notes = request.POST.get('notes')
        
        # Assuming you have user object accessible in request.user
        # user = request.user
        user = get_object_or_404(User, pk=5)
        
        # Create Medication object and save to database
        medication = Medication.objects.create(
            user=user,
            medication_text=medication_text,
            unit=unit,
            dosage=dosage,
            medication_date=medication_date,
            medication_time=medication_time,
            notes=notes
        )

        print(medication_date, medication_text, unit, dosage, medication_time, notes)
        return render(request, "management/index.html")
    return JsonResponse({'error': 'Invalid request method'})

def weightPage(request):
    return render(request,"management/weight.html")

@csrf_exempt
def add_weight(request):
    if request.method == 'POST':
        weight = request.POST.get('weight')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        notes = request.POST.get('notes')
        user = get_object_or_404(User, pk=5)

        weight_entry = WeightEntry.objects.create(
            user = user,
            weight=weight,
            entry_date=date_str, # Assuming date format
            entry_time=time_str,  # Assuming time format
            notes=notes,
        )
        print(date_str, time_str, notes)
        # Save the object and return a success response
        weight_entry.save()
        return render(request, 'management/weight.html')
    else:
        # Handle other HTTP methods (e.g., return an error for unsupported methods)
        return JsonResponse({'message': 'Invalid request method'}, status=405)
    
def signin(request):
    return render(request,'management/signin.html')

def signup(request):
    return render(request, 'management/signup.html')

@csrf_exempt
def signInCheck(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(name=username)
            # print(password, user.password, user.userid)
            if (password == user.password):

                return JsonResponse({'status': 'success', 'message': 'Login successful', 'id':  user.userid})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid password'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User does not exist'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create a new User object and save it
        new_user = User(name=username, email=email, password=password)
        new_user.save()

        # Optionally, you can return a JSON response or redirect to a success page
        return render(request,'management/signin.html')

    # Handle GET requests or other cases if needed
    return JsonResponse({'error': 'Invalid request method'})

def first(request):
    return redirect("/signin/")

def about_page(request):
    return render(request, "about.html")