from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lawyer, Consultation, LawCategory, Message
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


# ---------------- HOME ----------------

def home(request):
    return render(request, "home.html")


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            return render(request, "register.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("/dashboard/")

    return render(request, "register.html")


# ---------------- LOGIN ----------------

def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:

            login(request, user)
            return redirect("/dashboard/")

        else:

            return render(request, "login.html", {
                "error": "Invalid login"
            })

    return render(request, "login.html")


# ---------------- DASHBOARD ----------------

def dashboard(request):

    laws = LawCategory.objects.all()

    return render(request, "dashboard.html", {
        "laws": laws
    })


# ---------------- LAWYERS ----------------

def lawyers_by_category(request, category_id):

    category = LawCategory.objects.get(id=category_id)

    lawyers = Lawyer.objects.filter(specialization=category)

    return render(request, "lawyers.html", {
        "category": category,
        "lawyers": lawyers
    })


# ---------------- CONSULTATION ----------------

def consult_lawyer(request, lawyer_id):

    lawyer = Lawyer.objects.get(id=lawyer_id)

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        issue = request.POST.get("issue")

        consult = Consultation.objects.create(
            name=name,
            email=email,
            issue=issue,
            lawyer=lawyer
        )

        return redirect(f"/chat/{consult.id}/")

    return render(request, "consult.html", {"lawyer": lawyer})
# ---------------- CHATBOT PAGE ----------------

def chatbot(request):
    return render(request, "chatbot.html")


# ---------------- LOGOUT ----------------

def logout_user(request):
    logout(request)
    return redirect("/")


# ---------------- FALLBACK LEGAL AI ----------------

def fallback_legal_response(question):

    q = question.lower()

    if "divorce" in q or "marriage" in q:
        return """Here are some steps you can take:

1. File a divorce petition in family court.
2. Gather marriage documents and evidence.
3. Attempt mediation if required.
4. Consult a Family Lawyer."""

    elif "property" in q or "land" in q:
        return """Steps you can take:

1. Gather ownership documents.
2. Send a legal notice to the person occupying the property.
3. File a civil suit for possession if necessary.
4. Consult a Property Lawyer."""

    elif "cyber" in q or "hack" in q or "online fraud" in q:
        return """Steps you should take:

1. Immediately change passwords.
2. File a complaint at cybercrime.gov.in.
3. Report to your nearest cyber police station.
4. Consult a Cyber Crime Lawyer."""

    elif "consumer" in q or "product" in q:
        return """You can take these steps:

1. Contact the seller for resolution.
2. File complaint on consumerhelpline.gov.in.
3. Approach consumer court if necessary.
4. Consult a Consumer Lawyer."""

    elif "crime" in q or "police" in q: 
        return """Here are some steps you can take: 
1. Report the crime to the police immediately.
2. Gather any evidence related to the crime.    
3. File a First Information Report (FIR) at the police station.
4. Consult a Criminal Lawyer for legal guidance."""

    elif "contract" in q or "agreement" in q:
        return """Steps you can take:
1. Review the contract terms carefully.
2. Attempt to resolve the issue through communication.
3. Consider mediation or arbitration if included in the contract.
4. Consult a Corporate Lawyer for advice."""

    else:
        return """Here are some general steps:

1. Gather relevant documents.
2. Understand the legal issue clearly.
3. Consult the appropriate lawyer.
4. Consider filing a complaint in the appropriate authority."""


# ---------------- GEMINI AI CHATBOT ----------------

@csrf_exempt
def ask_lexora(request):

    if request.method == "POST":

        question = request.POST.get("question")

        # default fallback
        answer = "Here are some legal steps you can consider."

        try:
            prompt = f"""
You are Lexora AI, a helpful legal assistant.

User question:
{question}

Provide clear legal guidance in steps and suggest the correct type of lawyer.
"""

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            answer = response.text

        except Exception as e:
             print("Gemini error:", e)
    answer = fallback_legal_response(question)

        # CATEGORY DETECTION (always runs)
    category = None
    q = question.lower()

    if "land" in q or "property" in q:
            category = "Property Law"

    elif "divorce" in q or "family" in q:
            category = "Family Law"

    elif "cyber" in q or "hack" in q:
            category = "Cyber Law"

    elif "crime" in q or "police" in q:
            category = "Criminal Law"

    elif "consumer" in q or "product" in q:
            category = "Consumer Law"

    elif "contract" in q or "agreement" in q:
            category = "Corporate Law"

    lawyers = []

    if category:
            try:
                law_category = LawCategory.objects.get(name=category)

                recommended = Lawyer.objects.filter(
                    specialization=law_category
                )[:3]

                for lawyer in recommended:
                    lawyers.append({
                        "name": lawyer.name,
                        "experience": lawyer.experience,
                        "location": lawyer.location,
                        "email": lawyer.email,
                        "phone": lawyer.phone
                    })

            except:
                pass

    return JsonResponse({
            "answer": answer,
            "lawyers": lawyers
        })

def consultation_chat(request, consultation_id):

    consultation = Consultation.objects.get(id=consultation_id)

    messages = Message.objects.filter(consultation=consultation)

    if request.method == "POST":

        text = request.POST.get("message")

        # save user message
        Message.objects.create(
            consultation=consultation,
            sender="user",
            message=text
        )

        # simulated lawyer reply
        Message.objects.create(
            consultation=consultation,
            sender="lawyer",
            message="Thank you for sharing your issue. I will review your case."
        )

        return redirect(f"/chat/{consultation_id}/")

    return render(request, "chat.html", {
        "consultation": consultation,
        "messages": messages
    })