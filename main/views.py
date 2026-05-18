from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lawyer, LawCategory, Message, Consultation, Review
from google import genai
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ChatSession, Lawyer
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Lawyer, LawCategory

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

        if user is not None:

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
    lawyers = Lawyer.objects.filter(category_id=category_id)

    location = request.GET.get("location")

    if location:
        lawyers = lawyers.filter(location__icontains=location)

    return render(request, "lawyers.html", {
        "lawyers": lawyers
    })

# ---------------- CONSULTATION ----------------

@login_required
def consult_lawyer(request, lawyer_id):

    lawyer = Lawyer.objects.get(id=lawyer_id)

    if request.method == "POST":

        issue = request.POST.get("issue")

        Consultation.objects.create(
            user=request.user,
            lawyer=lawyer,
            issue=issue
        )

        return redirect("request_success")

    return render(request, "consult.html", {"lawyer": lawyer})
# ---------------- CHATBOT PAGE ----------------

def chatbot(request):
    return render(request, "chatbot.html")


# ---------------- LOGOUT ----------------

def logout_user(request):

    if request.user.is_authenticated:

        try:
            lawyer = Lawyer.objects.get(user=request.user)
            lawyer.is_online = False
            lawyer.save()
        except:
            pass

    logout(request)

    return redirect("/")


# ---------------- FALLBACK LEGAL AI ----------------
def fallback_legal_response(question):

    q = question.lower()

    # 🔴 Criminal Law
    if any(word in q for word in ["crime", "fraud", "theft", "assault", "police"]):
        return """⚖️ Criminal Law Guidance:

1. Report the incident to the nearest police station.
2. File an FIR and keep a copy.
3. Collect all evidence (messages, documents, witnesses).
4. Avoid making statements without legal advice.

👉 Consult a Criminal Lawyer immediately."""

    # 🟢 Family Law
    elif any(word in q for word in ["divorce", "marriage", "custody", "alimony"]):
        return """👨‍👩‍👧 Family Law Guidance:

1. File a petition in family court.
2. Gather marriage and identity documents.
3. Consider mediation before legal action.
4. Prepare for custody or maintenance discussions.

👉 Consult a Family Lawyer for proper guidance."""

    # 🟡 Property Law
    elif any(word in q for word in ["property", "land", "ownership", "house"]):
        return """🏠 Property Law Guidance:

1. Verify ownership and legal documents.
2. Send a legal notice if dispute exists.
3. File a civil suit if required.
4. Avoid illegal possession conflicts.

👉 Consult a Property Lawyer to resolve the issue."""

    # 🔵 Civil Law
    elif any(word in q for word in ["dispute", "agreement", "money", "contract"]):
        return """📄 Civil Law Guidance:

1. Review agreements or documents carefully.
2. Attempt negotiation or mediation first.
3. Collect proof of transactions or agreements.
4. Proceed legally if dispute continues.

👉 Consult a Civil Lawyer for resolution."""

    # 🟣 Corporate Law
    elif any(word in q for word in ["company", "business", "corporate", "startup"]):
        return """🏢 Corporate Law Guidance:

1. Review contracts and company policies.
2. Ensure legal compliance of business operations.
3. Avoid signing unclear agreements.
4. Maintain proper documentation.

👉 Consult a Corporate Lawyer for business legal advice."""

    # 💻 Cyber Law
    elif any(word in q for word in ["hack", "cyber", "online fraud", "scam", "account"]):
        return """💻 Cyber Law Guidance:

1. Secure all accounts immediately.
2. Change passwords and enable 2FA.
3. Report at cybercrime.gov.in.
4. Keep screenshots and evidence.

👉 Consult a Cyber Law expert for legal action."""

    # 🧑‍🏭 Labor Law
    elif any(word in q for word in ["labor", "wages", "worker", "salary", "union"]):
        return """👷 Labor Law Guidance:

1. Check employment rights and policies.
2. Raise complaint with employer or authority.
3. Gather salary or work-related proof.
4. Approach labor court if needed.

👉 Consult a Labor Lawyer for assistance."""

    # 👔 Employee Law
    elif any(word in q for word in ["job", "salary", "termination", "harassment", "employee"]):
        return """👔 Employee Law Guidance:

1. Review your employment contract.
2. Document incidents (emails, messages).
3. Report workplace issues formally.
4. Take legal action if rights are violated.

👉 Consult an Employee Rights Lawyer."""

    # 🌱 Environmental Law
    elif any(word in q for word in ['pollution', 'environment', 'illegal construction','factory', 'waste']):
        return """🌱 Environmental Law Guidance:

1. Report violations to local authorities.
2. Collect evidence (photos, videos).
3. File complaint with pollution control board.
4. Follow legal environmental procedures.

👉 Consult an Environmental Lawyer."""

    # 💡 Intellectual Property Law
    elif any(word in q for word in ["copyright", "trademark", "patent", "idea", "logo"]):
        return """💡 Intellectual Property Guidance:

1. Register your work legally (copyright/trademark).
2. Avoid sharing ideas publicly without protection.
3. Keep proof of creation.
4. Take action against misuse.

👉 Consult an IP Lawyer to protect your rights."""

    # ⚪ Default fallback
    else:
        return """📌 General Legal Guidance:

1. Identify your legal issue clearly.
2. Gather all related documents.
3. Avoid taking action without legal advice.
4. Approach the correct legal authority.

👉 I recommend consulting a lawyer for proper assistance."""

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

from django.shortcuts import get_object_or_404

def consultation_chat(request, consultation_id):

    consultation = get_object_or_404(Consultation, id=consultation_id)

    # get or create chat session
    chat, created = ChatSession.objects.get_or_create(
        consultation=consultation
    )

    messages = Message.objects.filter(chat=chat).order_by("created_at")

    if request.method == "POST":
        text = request.POST.get("message")

        Message.objects.create(
            chat=chat,
            sender=request.user,
            text=text
        )

    return render(request, "chat.html", {
        "chat": chat,
        "messages": messages,
        "consultation": consultation
    })

from django.contrib.auth.models import User
from django.contrib import messages
from .models import Lawyer, LawCategory

def lawyer_register(request):

    categories = LawCategory.objects.all()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        experience = request.POST.get('experience')

        category_id = request.POST.get('category')
        category = LawCategory.objects.get(id=category_id)

        # ✅ create user
        user = User.objects.create_user(username=username, password=password, email=email)

        # ✅ create lawyer
        Lawyer.objects.create(
            user=user,   # ONLY if you added user field
            name=name,
            email=email,
            phone=phone,
            category=category,
            specialization=category.name,
            experience=experience,
            location=location
        )

        messages.success(request, "Registration successful!")
    
    return render(request, "lawyer_register.html", {"categories": categories})

def lawyer_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,username=username,password=password)

        if user:

            login(request,user)

            lawyer = Lawyer.objects.get(user=user)

            lawyer.is_online = True
            lawyer.save()

            return redirect("/lawyer/dashboard/")

    return render(request,"lawyer_login.html")

@login_required
def lawyer_dashboard(request):

    lawyer = Lawyer.objects.get(user=request.user)

    consultations = Consultation.objects.filter(lawyer=lawyer)
    
    return render(request,"lawyer_dashboard.html",{
        "lawyer":lawyer,
        "consultations":consultations
    })

def lawyer_profile(request, lawyer_id):

    lawyer = Lawyer.objects.get(id=lawyer_id)

    return render(request, "lawyer_profile.html", {
        "lawyer": lawyer
    })


@login_required


def request_success(request):
    return render(request,"success.html")
    return redirect("/request-success/")   


from .models import Message, ChatSession

def user_chats(request):

    chats = ChatSession.objects.filter(user=request.user)

    return render(request,"user_chats.html",{
        "chats":chats
    })

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from main.models import Lawyer

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 SET LAWYER ONLINE
            try:
                lawyer = Lawyer.objects.get(email=user.email)
                lawyer.is_online = True
                lawyer.save()
            except Lawyer.DoesNotExist:
                pass

            return redirect("dashboard")

        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

def add_review(request, lawyer_id):
    lawyer = Lawyer.objects.get(id=lawyer_id)

    rating = int(request.POST.get("rating"))
    comment = request.POST.get("comment")

    Review.objects.create(
        lawyer=lawyer,
        user=request.user,
        rating=rating,
        comment=comment
    )

    # 🔥 Update rating
    reviews = Review.objects.filter(lawyer=lawyer)
    total = sum([r.rating for r in reviews])
    lawyer.total_reviews = reviews.count()
    lawyer.rating = total / lawyer.total_reviews
    lawyer.save()

    return redirect('lawyer_profile', id=lawyer.id)

def send_message(request, chat_id):
    chat = ChatSession.objects.get(id=chat_id)

    text = request.POST.get("text")
    file = request.FILES.get("file")

    Message.objects.create(
        chat=chat,
        sender=request.user,
        text=text,
        file=file
    )

    return redirect('chat_page', chat_id=chat.id)

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import ChatSession

def start_chat(request, lawyer_id):
    from .models import ChatSession, Lawyer

    lawyer = Lawyer.objects.get(id=lawyer_id)

    chat = ChatSession.objects.create(
        user=request.user,
        lawyer=lawyer
    )

    return redirect('chat_page', chat.id)

from .models import Booking

def book_lawyer(request, lawyer_id):
    lawyer = Lawyer.objects.get(id=lawyer_id)

    booking = Booking.objects.create(
        user=request.user,
        lawyer=lawyer,
        amount=lawyer.consultation_fee
    )

    return redirect(f"/payment/{booking.id}/")

def payment_page(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":
        booking.is_paid = True
        booking.save()
        return redirect("/success/")

    return render(request, "payment.html", {"booking": booking})

from .models import Booking

def pay_lawyer(request, lawyer_id):
    lawyer = Lawyer.objects.get(id=lawyer_id)

    Booking.objects.create(
        user=request.user,
        lawyer=lawyer,
        amount=lawyer.consultation_fee,
        is_paid=True
    )

    return redirect('dashboard')

def chat_page(request, chat_id):
    from .models import Chat, Message

    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.method == "POST":
        text = request.POST.get("text")
        file = request.FILES.get("file")

        if text or file:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                text=text,
                file=file
            )

    return render(request, "chat.html", {
        "chat": chat,
        "messages": messages
    })