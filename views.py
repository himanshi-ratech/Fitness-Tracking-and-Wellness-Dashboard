from django.shortcuts import render, redirect, get_object_or_404
from fitstore.models import * 
from fitstore.forms import *
from django.http import HttpResponse 
from django.contrib import messages

# Create your views here.
def splash_page(request):
    # you can pass context if you want (e.g., brand text, image path)
    return render(request, 'splash_page.html')


import re
def signup(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        email = request.GET.get('email')
        password = request.GET.get('password')
        confirm = request.GET.get('confirm')

        if name and email and password and confirm:
            if password != confirm:
                return render(request, 'signup.html', {'error': 'Passwords do not match'})

            if not email.endswith("@gmail.com"):
                return render(request, 'signup.html', {'error': 'Enter valid username/email'})
            
            Register.objects.create(name=name, email=email, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('signup')

    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Register.objects.filter(email=email, password=password).first()
        if user:
            request.session['email'] = user.email
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def classes(request):
    return render(request, 'classes.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save to database
        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            return redirect('contact')  # redirect to avoid resubmission

    return render(request, 'contact.html')

def comment(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        
    if name and email and comment:
        Comment.objects.create(name= name, email=email,comment=comment)
    
    return redirect(request.META.get('HTTP_REFERER', '/'))

def gallery(request):
    return render(request, 'gallery.html')

def blog(request):
    return render(request, 'blog.html')

def details(request):
    return render(request, 'blog-details.html')
def blog_two(request):
    return render(request, 'blog2.html')
def blog_three(request):
    return render(request,'blog3.html')

def new(request):
    return render(request, 'new.html')


def fitness_result(request):
    return render(request, 'fitness_result.html')


import pandas as pd
import matplotlib.pyplot as plt
import io, base64, os
from django.shortcuts import render
from django.conf import settings

# ---- Helper function to calculate metrics ----
def calculate_metrics(row):
    calorie_balance = row['total_calories_intake_est'] - row['calories_burned']
    hydration_score = min(10, row['water_intake_liters'] / 3 * 10)
    sleep_score = min(10, (row['sleep_hours'] / 8) * 10)
    intensity_score = min(10, row['avg_heart_rate_bpm'] / 18)
    nutrition_score = min(10, (row['protein_intake_g'] / 
                               (row['carb_intake_g'] + row['fat_intake_g'] + 1)) * 10)
    fitness_score = round((0.25 * sleep_score + 0.25 * intensity_score +
                           0.25 * hydration_score + 0.25 * nutrition_score), 2)
    return pd.Series([calorie_balance, fitness_score])


# ---- View 1: Fitness Dashboard ----
def fitness_dashboard(request):
    df = pd.read_csv("C:\\Users\\DELL\\Desktop\\Fitness\\fit\\myfile\\user1_daily_fitness_180days.csv")

    # Add computed columns
    df[['calorie_balance', 'computed_fitness_score']] = df.apply(calculate_metrics, axis=1)

    latest = df.iloc[-1]
    return render(request, 'index.html', {'data': latest})


# ---- View 2: Summary ----
def fitness_summary(request):
    df = pd.read_csv("C:\\Users\\DELL\\Desktop\\Fitness\\fit\\myfile\\user1_daily_fitness_180days.csv")

    df[['calorie_balance', 'computed_fitness_score']] = df.apply(calculate_metrics, axis=1)
    summary_stats = df.describe().loc[['count', 'mean', 'min', 'max']]

    # Convert to HTML table
    summary_html = summary_stats.to_html(classes='table table-bordered', float_format="%.2f")
    
    return render(request, 'user_summary.html', {'tables': summary_html})

''''numeric_df = df.select_dtypes(include='number')

    # Get full summary
    summary = numeric_df.describe()

    # ✅ Keep only count, mean, min, max
    summary = summary.loc[['count', 'mean', 'min', 'max']]

    # Convert to HTML table
    summary_html = summary.to_html(classes='table table-bordered', float_format='{:,.2f}'.format)'''



# ---- View 3: Chart ----
def fitness_chart(request):
    df = pd.read_csv("C:\\Users\\DELL\\Desktop\\Fitness\\fit\\myfile\\user1_daily_fitness_180days.csv")

    df[['calorie_balance', 'computed_fitness_score']] = df.apply(calculate_metrics, axis=1)

    # Create the chart
    plt.figure(figsize=(8, 4))
    plt.plot(df['date'], df['computed_fitness_score'], marker='o', label='Fitness Score')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('Fitness Progress Over Time')
    plt.tight_layout()

    # Convert chart to base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render(request, 'chart.html', {'chart_url': chart_url})

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # ✅ Use Agg backend to avoid GUI issues
import matplotlib.pyplot as plt
import io, base64
from django.shortcuts import render
from datetime import datetime

def fitness_chart(request):
    # ✅ Load your CSV file (keep absolute path or use BASE_DIR if needed)
    df = pd.read_csv(r"C:\Users\DELL\Desktop\Fitness\fit\myfile\user1_daily_fitness_180days.csv")
    df = df.head(20) 
    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
    
    # ✅ Format date as "DD-MM"
    df['short_date'] = df['date'].dt.strftime('%d-%m')
    # ✅ Select numeric columns for line charts
    columns_to_plot = [
        'bmi', 'sleep_hours', 'workout_duration_mins',
        'steps_walked', 'water_intake_liters', 'protein_intake_g',
        'carb_intake_g', 'fat_intake_g', 'avg_heart_rate_bpm',
        'calories_burned', 'fitness_score', 'total_calories_intake_est'
    ]

    charts = {}

    # ✅ Generate line chart for each column
    for col in columns_to_plot:
        plt.figure(figsize=(6, 3))
        plt.plot(df['short_date'], df[col], marker='o', linestyle='-', color='royalblue')
        plt.title(f"{col.replace('_', ' ').title()} Over Time")
        plt.xlabel("Date (DD-MM)")
        plt.ylabel(col.replace('_', ' ').title())
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.xticks(rotation=90)
        plt.tight_layout()

        # ✅ Convert to Base64 image string
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        charts[col] = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close()

    return render(request, 'all_chart.html', {'charts': charts})



def user_dashboard(request):
    # 1️⃣ Check if user is logged in
    user = request.session.get('email')
    if not user:
        return redirect('login')  # adjust to your login page name

    # 2️⃣ Get the logged-in user from Register model
    user = get_object_or_404(Register, email=user)

    if request.method == 'POST':
        selected_date = request.POST.get('fitness_date')
        formatted_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        
        weight = float(request.POST['weight_kg'])
        height = float(request.POST['height_cm'])
        sleep_hours = float(request.POST['sleep_hours'])
        water = float(request.POST['water_intake_liters'])
        workout = float(request.POST['workout_duration_mins'])
        steps = float(request.POST['steps_walked'])
        burned = float(request.POST['calories_burned'])
        intake = float(request.POST['total_calories_intake_est'])
        heart_rate = float(request.POST['avg_heart_rate_bpm'])
        protein = float(request.POST['protein_intake_g'])
        carbs = float(request.POST['carb_intake_g'])
        fats = float(request.POST['fat_intake_g'])

        # --- Calculations ---

        calorie_balance = intake - burned
        if calorie_balance >300:
            caloriebalance_status= "Weight Gain"
        elif calorie_balance < -300:
            caloriebalance_status="Energy deficit. Take Rest."
        else :
            caloriebalance_status="Balanced. Good work!"
        
        hydration_score = min(10, (water / 3) * 10)
        if water <1.5:
            hydration_status= "Drink more water"
        elif 1.5 <= water <= 4:
            hydration_status="Good!"
        else :
            hydration_status="Drink less water."
            
        sleep_score = min(10, (sleep_hours / 7) * 10)
        if sleep_hours <4:
            sleep_status= "Sleep more."
        elif 4 <= sleep_hours <= 8:
            sleep_status="Good!"
        else :
            sleep_status="Sleep Less."
            
        intensity_score = min(10, heart_rate / 18)   
        # if heart_rate < 60:
        #     intensity_status = "Low Intensity"
        # elif 60 <= heart_rate <= 100:
        #     intensity_status = "Normal Intensity"
        # else:
        #     intensity_status = "High Intensity"  
        # nutrition_score = min(10, (protein / (carbs + fats + 1)) * 10)
        # if nutrition_score <5:
        #     nutrition_status = "Increase Protien or Reduce Fat/Cabs"
        # else:
        #     nutrition_status = "Balanced Diet"
        protein_score = min(10, protein/100 * 10)   # ideal 100g = score 10
        carb_score    = min(10, carbs/250 * 10)     # ideal 250g = score 10
        fat_score     = min(10, fats/70 * 10)       # ideal 70g = score 10

        nutrition_score = round((protein_score + carb_score + fat_score) / 3, 1)

        if nutrition_score < 3:
            nutrition_status = "Very Poor Nutrition Balance"
            

        elif nutrition_score < 5:
            nutrition_status = "Needs Improvement"
            

        elif nutrition_score < 7.5:
            nutrition_status = "Moderately Balanced"
            

        else:
            nutrition_status = "Balanced Diet"
            
            
        steps_score = min(10, (steps / 10000) * 10)
        if steps < 3000:
            steps_status = "Walk more. Low activity level."
        else:
            steps_status = "Good Job!"

        workout_score = min(10, (workout / 60) * 10)
        if workout <15:
            workout_status = "Increase workout time."
        else:
            workout_status = "Good Job!"
            
        height_m = height / 100
        if height_m == 0:
            bmi = 0
            bmi_status = "Invalid height"

        
        bmi = round(weight / (height_m ** 2), 2)
        if bmi < 18.5:
            bmi_status = "Underweight"
        elif 18.5 <= bmi < 25:
            bmi_status = "Normal weight"
        elif 25 <= bmi < 30:
            bmi_status = "Overweight"
        else:
            bmi_status = "Obese"

        burned_score = min(10, (burned / 700) * 10)
        

        fitness_score = round((0.15 * sleep_score + 0.10 * steps_score +
                               0.15 * workout_score + 0.10 * hydration_score +
                               0.10 * nutrition_score + 0.15 * intensity_score+ 0.10* bmi+ 0.15*burned_score), 2)
        
        FitnessRecord.objects.create(
            user=user,
            date=formatted_date,
            weight_kg=weight,
            height_cm=height,
            sleep_hours=sleep_hours,
            water_intake_liters=water,
            workout_duration_mins=workout,
            steps_walked=steps,
            calories_burned=burned,
            total_calories_intake_est=intake,
            avg_heart_rate_bpm=heart_rate,
            protein_intake_g=protein,
            carb_intake_g=carbs,
            fat_intake_g=fats,

            bmi=bmi,
            bmi_status=bmi_status,
            calorie_balance=calorie_balance,
            caloriebalance_status=caloriebalance_status,
            hydration_score=hydration_score,
            hydration_status=hydration_status,
            sleep_score=sleep_score,
            sleep_status=sleep_status,
            nutrition_score=nutrition_score,
            nutrition_status=nutrition_status,
            steps_score=steps_score,
            steps_status=steps_status,
            workout_score=workout_score,
            workout_status=workout_status,
            fitness_score=fitness_score,
        )
        
        context = {
            'user_email': user.email,
            'selected_date': formatted_date,
            'fitness_score': fitness_score,
            'bmi': bmi,
            'bmi_status': bmi_status,
            'calorie_balance': calorie_balance,
            'caloriebalance_status':caloriebalance_status,
            'hydration_score': hydration_score,
            'hydration_status':hydration_status,
            'sleep_score': sleep_score,
            'sleep_status':sleep_status,
            'nutrition_score': nutrition_score,
            'nutrition_status':nutrition_status,
            'steps_score': steps_score,
            'steps_status':steps_status,
            'workout_score': workout_score,
            'workout_status':workout_status,
        }
        return render(request, 'fitness_result.html', context)
        
    return render(request, 'user_dashboard.html', {'user_email': user.email})





def user_fitness(request):
    score = None
    message = None
    detail = None

    if request.method == "POST":
        action = request.POST.get('action')

        # 💤 Sleep
        if action == "sleep":
            sleep_hours = float(request.POST.get('sleep_hours'))
            score = min(10, (sleep_hours / 8) * 10)
            message = f"Sleep Score: {score:.2f} / 10"
            if sleep_hours < 6:
                detail = "😴 You need more rest! Try to sleep at least 7–8 hours daily."
            elif 6 <= sleep_hours <= 8:
                detail = "✅ Great! You’re getting a healthy amount of sleep."
            else:
                detail = "⚠️ Oversleeping may cause tiredness. Keep it around 7–8 hours."

        # 💧 Water
        elif action == "water":
            water = float(request.POST.get('water_intake_liters'))
            score = min(10, (water / 3) * 10)
            message = f"Hydration Score: {score:.2f} / 10"
            if water < 2:
                detail = "🚰 Increase your water intake — aim for 2.5–3 liters per day."
            else:
                detail = "✅ Good hydration maintained!"

        # ❤️ Heart Rate
        elif action == "heart":
            heart = float(request.POST.get('avg_heart_rate_bpm'))
            score = min(10, heart / 18)
            message = f"Heart Intensity Score: {score:.2f} / 10"
            if heart < 60:
                detail = "🩺 Your heart rate is low — consult a trainer or doctor if you feel weak."
            elif 60 <= heart <= 100:
                detail = "✅ Normal resting heart rate range."
            else:
                detail = "⚠️ High heart rate — ensure you’re not overtraining."

        # 🔥 Calories Burned
        elif action == "calories":
            calories = float(request.POST.get('calories_burned'))
            score = min(10, calories / 500 * 10)
            message = f"Calories Burned Score: {score:.2f} / 10"
            if calories < 300:
                detail = "🏃 Try to increase your activity level — aim for at least 300–500 kcal/day."
            else:
                detail = "✅ Good calorie burn maintained!"

        # ⚖️ BMI
        elif action == "bmi":
            weight = float(request.POST.get('weight_kg'))
            height = float(request.POST.get('height_cm')) / 100
            bmi = weight / (height ** 2)
            message = f"Your BMI: {bmi:.2f}"
            if bmi < 18.5:
                score = 6
                detail = "⚠️ Underweight — increase protein and balanced diet intake."
            elif 18.5 <= bmi <= 24.9:
                score = 10
                detail = "✅ Healthy BMI range. Maintain your diet and activity."
            elif 25 <= bmi <= 29.9:
                score = 7
                detail = "⚠️ Overweight — include regular exercise and a calorie deficit diet."
            else:
                score = 5
                detail = "🚨 Obese — consult a health professional for a proper plan."

    context = {
        "score": score,
        "message": message,
        "detail": detail,
    }
    return render(request, "user_fitness.html", context)

def plan(request):
    return render(request, 'fitness_plan_strategies.html')

def diet(request):
    return render(request, 'nutrition_diet.html')
def mindset(request):
    return render(request, 'mindset.html')

def workout(request):
    return render(request, 'workout.html')

def weight_loss(request):
    return render(request, 'weight_loss.html')
def fat_burn(request):
    return render(request, 'fat_burn.html')

def yoga_flow(request):
    return render(request, 'yoga_flow.html')

def yoga(request):
    return render(request, 'yoga.html')

# def fitness_charts(request):
 
#     user = request.session.get('email')
#     if not user:
#         return redirect('login')  # adjust to your login page name

#     # 2️⃣ Get the logged-in user from Register model
#     user = get_object_or_404(Register, email=user)

#     # ✅ Get user object
#     user = Register.objects.filter(email=user).first()
#     if not user:
#         messages.error(request, "User not found.")
#         return redirect('login')

#     # ✅ Fetch all fitness records for this user
#     fitness_records = FitnessRecord.objects.filter(user_id=user.id).order_by('date')  # assuming you have a `date` field

#     # ✅ Convert queryset to list of dicts for Chart.js
#     data = []
#     for record in fitness_records:
#         data.append({
#             'day': record.date.strftime('%b %d, %Y'),
#             'fitness_score': record.fitness_score if hasattr(record, 'fitness_score') else 0,
#             # 'calories_out': record.calories_out if hasattr(record, 'calories_out') else 0,
#             'hydration_score': record.hydration_score if hasattr(record, 'hydration_score') else 0,
#             'sleep': record.sleep_score if hasattr(record, 'sleep_score') else 0,
#             'steps': record.steps_score if hasattr(record, 'steps_score') else 0,
#             'nutrition_score': record.nutrition_score if hasattr(record, 'nutrition_score') else 0,
#             'workout_score': record.workout_score if hasattr(record, 'workout_score') else 0,
#         })

#     # ✅ Calculate weekly/monthly summaries
#     if fitness_records.exists():
#         total_days = len(fitness_records)
#         weekly_data = {
#             'avg_fitness_score': sum([d['fitness_score'] for d in data]) / total_days,
#             'avg_steps': sum([d['steps'] for d in data]) / total_days,
#             'avg_sleep': sum([d['sleep'] for d in data]) / total_days,
#             'avg_score': sum([d['nutrition_score'] for d in data]) / total_days,
#             'avg_hydration': sum([d['hydration_score'] for d in data]) / total_days,
            
#         }
#         monthly_data = weekly_data  # you can later calculate from a month filter
#     else:
#         weekly_data = {'avg_fitness_score': 0, 'avg_steps': 0, 'avg_sleep': 0, 'avg_score': 0, 'avg_hydration': 0}
#         monthly_data = weekly_data

#     # ✅ Send data to template
#     return render(request, 'fitness_chart.html', {
#         'user_name': user.name,
#         'daily_data': data,
#         'weekly_data': weekly_data,
#         'monthly_data': monthly_data,
#     })
    
def fitness_charts(request):

    user_email = request.session.get('email')
    if not user_email:
        return redirect('login')

    user = get_object_or_404(Register, email=user_email)

    fitness_records = FitnessRecord.objects.filter(
        user_id=user.id
    ).order_by('date')

    data = []
    for rec in fitness_records:
        data.append({
            'day': rec.date.strftime('%b %d, %Y'),
            'fitness_score': rec.fitness_score or 0,
            'hydration_score': rec.hydration_score or 0,
            'sleep_score': rec.sleep_score or 0,
            'steps_score': rec.steps_score or 0,
            'nutrition_score': rec.nutrition_score or 0,
            'workout_score': rec.workout_score or 0,
        })

    # Weekly/monthly averages
    if data:
        total = len(data)
        weekly_data = {
            'avg_fitness_score': sum(d['fitness_score'] for d in data) / total,
            'avg_hydration': sum(d['hydration_score'] for d in data) / total,
            'avg_sleep': sum(d['sleep_score'] for d in data) / total,
            'avg_steps': sum(d['steps_score'] for d in data) / total,
            'avg_nutrition': sum(d['nutrition_score'] for d in data) / total,
            'avg_workout': sum(d['workout_score'] for d in data) / total,
        }
        monthly_data = weekly_data
    else:
        weekly_data = monthly_data = {
            'avg_fitness_score': 0,
            'avg_hydration': 0,
            'avg_sleep': 0,
            'avg_steps': 0,
            'avg_nutrition': 0,
            'avg_workout': 0,
        }

    return render(request, 'fitness_chart.html', {
        'daily_data': data,
        'weekly_data': weekly_data,
        'monthly_data': monthly_data,
    })

    
from django.conf import settings    
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils import timezone

# -------------------- CHATBOT VIEW --------------------

@csrf_exempt
def fitness_chatbot(request):
    # 1️⃣ Check login
    user_email = request.session.get('email')
    if not user_email:
        return redirect('login')

    user = Register.objects.filter(email=user_email).first()
    if not user:
        return redirect('login')

    # 2️⃣ Fetch last 7 days of fitness data
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)

    records = FitnessRecord.objects.filter(
        user=user,
        date__gte=seven_days_ago,
        date__lte=today
    ).order_by('date')

    if not records.exists():
        return render(request, "fitness_chatbot.html",
                      {"response": "No fitness data found for the last 7 days."})

    # Convert queryset → list of dicts
    records_list = []
    for r in records:
        records_list.append({
            "date": r.date.strftime('%Y-%m-%d'),
            "sleep_hours": r.sleep_hours,
            "water_intake": r.water_intake_liters,
            "steps": r.steps_walked,
            "calories_burned": r.calories_burned,
            "intake": r.total_calories_intake_est,
            "bmi": r.bmi,
            "fitness_score": r.fitness_score,
        })

    response_text = None

    # 3️⃣ Handle POST → send to Gemini
    if request.method == "POST":
        user_prompt = request.POST.get("prompt", "")

        # Gemini init
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Construct the message
        final_prompt = f"""
        You are a fitness assistant.

        Here is the user's last 7 days of data:
        {records_list}

        User question: {user_prompt}

        Give a clear, useful answer based on the data above.
        """

        gemini_response = model.generate_content(final_prompt)
        response_text = gemini_response.text.strip()

    return render(request, "fitness_chatbot.html", {
        "response": response_text,
        "records": records_list
    })