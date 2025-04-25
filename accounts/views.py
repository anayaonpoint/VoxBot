from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile 
from .models import Journal
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
import google.generativeai as genai
import datetime

import os
import json

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def signIn(request):
 if request.method == 'POST':
  email = request.POST.get('email')
  password = request.POST.get('password')
  if not email or not password:
   messages.error(request, "Email and Password are required.")
   return redirect('login') 
  if not User.objects.filter(email=email).exists():
   messages.error(request, "Email does not exist. Please sign up.")
   return redirect('signup') # Redirect to the signup page
  
  # Authenticate the user
  user = authenticate(request, username=email, password=password)
  if user is not None:
   login(request, user)
   return redirect('home') # Replace 'home' with the name of your homepage
  else:
   messages.error(request, "Invalid email or password.")
   return redirect('login')
 
 return render(request, 'signIn.html') # Render the login page for GET requests

def contact(request):
 return render(request,"contact.html")

def logout(request):
 return render(request,"logout.html")

def signup(request):
 if request.method == "POST":
  name = request.POST.get("name")
  email = request.POST.get("email")
  password = request.POST.get("password")

  if UserProfile.objects.filter(email=email).exists():
   return render(request, "signup.html", {"error": "Email is already registered."})
  
  if name and email and password:
   hashed_password = make_password(password)
   user_profile = UserProfile(name=name, email=email, password=hashed_password)
   user_profile.save()
   messages.success(request, "Account created successfully! Please sign in.")
   return redirect("signIn")
  else:
   return render(request, "signup.html", {"error": "All fields are required."})

 return render(request, "signup.html")

def forgetPass(request):
 if request.method == "POST":
  email = request.POST.get("email")
  messages.success(request, "Password reset link sent.")
 return render(request, "forgetPass.html")

# Configure Google Generative AI API
genai.configure(api_key="AIzaSyAPldZJZc_8dZhqFOUlj7mA4ivTSCCPB4E")

def main(request):
 if request.method == "POST":
  text = request.POST.get("text")
  # Process the posted data (if necessary)
 return render(request, "main.html")

def get_ai_response(request):
 if request.method == "POST":
  try:
   # Parse the JSON data sent from the frontend
   data = json.loads(request.body)
   query = data.get("query", "").strip()

   if not query:
    return JsonResponse({"error": "No query received"}, status=400)

   # Initialize the model
   model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
  

   # Generate content using the correct method
   response = model.generate_content(query)

   # Extract the response text
   if response.text:
    return JsonResponse({"response": response.text})
   else:
    return JsonResponse({"error": "No response generated"}, status=400)

  except Exception as e:
   return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

 return JsonResponse({"error": "Invalid request method"}, status=405)

def process_query(request):
 if request.method == "POST":
  query = request.POST.get('query', '')
  # Process the query and generate a response
  response = f"This is the response to '{query}'"
  audio_url = "/static/audio/response.mp3" # Path to generated or predefined audio file

  return JsonResponse({
   "response": response,
   "audioUrl": audio_url
  })
 return JsonResponse({"error": "Invalid request"}, status=400)




def journal_page(request):
    return render(request, 'journal.html')
@csrf_exempt

def save_journal(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            mood = data.get('mood')
            Journal.objects.create(content=content, mood=mood)
            return JsonResponse({'message': 'Journal saved'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_journal_entries(request):
    entries = Journal.objects.all().order_by('-timestamp')
    data = [
        {
            'content': entry.content,
            'mood': entry.mood,
            'timestamp': entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for entry in entries
    ]
    return JsonResponse(data, safe=False)
 
def get_mood_data(request):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=7)

    # Filter journals for the past 7 days
    journal_entries = Journal.objects.filter(timestamp__date__gte=start_date)

    # Initialize mood count (convert all mood entries to lowercase)
    mood_count = {'happy': 0, 'sad': 0, 'neutral': 0}

    # Count the moods (ensure mood is case insensitive)
    for entry in journal_entries:
        mood = entry.mood.strip().lower()  # Normalize mood to lowercase
        if mood in mood_count:
            mood_count[mood] += 1

    # Return the mood data in JSON format
    return JsonResponse({
        'mood_data': mood_count,
        'labels': ['Happy', 'Sad', 'Neutral']
    })