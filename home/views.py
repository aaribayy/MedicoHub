from django.shortcuts import render, HttpResponse, redirect
from home.models import Feedback, Prediction
from django.contrib.auth.decorators import  login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import numpy as np



@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')

# Create your views here.
def index(request):
    # context={'variable':'this is sent'}
    return render(request, 'index.html')
    # return HttpResponse('This is home page')

def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request, 'contact.html')

from django.contrib.auth.hashers import check_password

# def Login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('pass')

#         try:
#             user = Register.objects.get(uname=username)
#             if check_password(password, user.password):
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     print("Login successful!")  # Debug statement
#                     return redirect('index')  # Redirect to index page after successful login
#                 else:
#                     print("User is None after authentication!")  # Debug statement
#             else:
#                 print("Password incorrect!")  # Debug statement
#         except Register.DoesNotExist:
#             print("User does not exist!")  # Debug statement
#             return HttpResponse("Username or Password is incorrect!!!")

#     return render(request, 'Login.html')




def SignUp(request):
    context = {}
    if request.method == 'POST':
        uname = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
            context['password_error'] = "Your password and confirm password are not the same!"
            context['username'] = uname
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email
        elif User.objects.filter(email=email).exists():
            context['email_error'] = "Email already exists, please choose another one."
            context['username'] = uname
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email
        elif User.objects.filter(username=uname).exists():
            context['username_error'] = "Username already exists, please choose another one."
            context['username'] = uname
            context['first_name'] = first_name
            context['last_name'] = last_name
            context['email'] = email
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.first_name = first_name
            my_user.last_name = last_name
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html', context)

@login_required(login_url='login')
def change_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        new_username = request.POST.get('new_username')
        user.username = new_username
        user.save()
        return redirect('/profile')
    return render(request, 'edit.html')


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def Login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            # Determine which field has the error
            context['username'] = username  # Keep the entered username
            if not authenticate(request, username=username, password=None):
                context['username_error'] = True
                context['password_error'] = True
    
    return render(request, 'login.html', context)
# def Login(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('/')
#         else:
#             return HttpResponse ("Username or Password is incorrect!!!")
#     return render (request,'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('home')


import os
import pickle
import numpy as np
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Define the absolute path to the model file
model_path = os.path.join(settings.BASE_DIR, 'svc.pkl')

# Load the trained model and data files
try:
    svc = pickle.load(open(model_path, 'rb'))
except FileNotFoundError:
    svc = None

sym_des = pd.read_csv(os.path.join(settings.BASE_DIR, "datasets/symtoms_df.csv"))
precautions = pd.read_csv(os.path.join(settings.BASE_DIR, "datasets/precautions_df.csv"))
workout = pd.read_csv(os.path.join(settings.BASE_DIR, "datasets/workout_df.csv"))
description = pd.read_csv(os.path.join(settings.BASE_DIR, "datasets/description.csv"))
medications = pd.read_csv(os.path.join(settings.BASE_DIR, 'datasets/medications.csv'))
diets = pd.read_csv(os.path.join(settings.BASE_DIR, "datasets/diets.csv"))

symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}

def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis]['workout']
    return desc, pre, med, die, wrkout

@login_required(login_url='login')
def services(request):
    context = {}
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        user_symptoms = [s.strip() for s in symptoms.split(',')]
        user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
        predicted_disease = get_predicted_value(user_symptoms)

        desc, pre, med, die, wrkout = helper(predicted_disease)
        if request.user.is_authenticated:
            user_id = request.user.id
            print(user_id)  
        context = {
            'user_symptoms' : user_symptoms,
            'predicted_disease': predicted_disease,
            'description': desc,
            'precautions': pre,
            'medications': med,
            'diets': die,
            'workout': wrkout,'user_id': user_id, 
        }
        save_prediction(user_id, pre,med,wrkout,die, symptoms,request)
    return render(request, 'services.html', context)
    # return render(request, 'services.html')


    # if request.user.is_authenticated:
    #     user_id = request.user.id
    #     print(user_id)  # Print user ID for debugging
    #     # Your services logic here
    #     return render(request, 'services.html', {'user_id': user_id})
    # else:
    #     return HttpResponse("You are not logged in!")



from textblob import TextBlob

def get_sentiment(text):
    
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    print(polarity)
    if polarity > 0.8:
        return 'strongly positive'
    elif 0.6 < polarity <= 0.8:
        return 'positive'
    elif -0.2 <= polarity <= 0.2:
        return 'neutral'
    elif -0.8 <= polarity < -0.6:
        return 'negative'
    elif polarity < -0.8:
        return 'strongly negative'
   

@login_required(login_url='login')
def feedback(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user = request.user
        sentiment = get_sentiment(message)
        try:
            feedback = Feedback.objects.create(user=user, subject=subject, message=message, analysis=sentiment)
            messages.success(request, 'Feedback sent successfully!')
        except Exception as e:            
            messages.error(request, f'Error: {e}')
        return redirect('/')  
    return render(request, 'feedback.html')



# def save(user_id, pre, med, wo, d):
#     try:
#         pred = Prediction.objects.create(user_id=user_id, Precautions=pre, Medications=med, workout=wo, diet=d)
#         # messages.success(request, 'Predicted successfully!')
#     except Exception as e:
#         messages.error(request, f'Error: {e}')
#     return render(request, 'services.html')
def save_prediction(user_id, pre, med, wo, d, s, request):
    try:
        pred = Prediction.objects.create(user_id=user_id, Precautions=pre, Medications=med, workout=wo, diet=d, symptoms=s)
        messages.success(request, 'Predicted successfully!')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return render(request, 'services.html')


@login_required(login_url='login')
def user_profile(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'user.html', {'predictions': predictions})


@login_required(login_url='login')
def chatbot(request):
    return render(request, 'chatbot.html')


