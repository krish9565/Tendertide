from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tender
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from google.genai import Client, types
from .models import ContactMessage


# Your API URL for Gemini (if you still need it, but we'll use the google.genai Client now)
API_KEY = "YOUR GEMINI_API_KEY_HERE"


@csrf_exempt
def chatbot_api(request):
    
    # print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    if request.method == "POST":
        try:
            # Parse the incoming request data
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if user_message:
                # Initialize the Google Gen AI Client
                client = Client(api_key=API_KEY)

                # Specify the model and contents
                model = "gemini-2.0-flash"
                contents = [
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=user_message),  # Use user input here
                        ],
                    ),
                ]

                # Configuration for generating content
                generate_content_config = types.GenerateContentConfig(
                    temperature=1,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                    response_mime_type="text/plain",
                )

                # Call the API and get the response from the stream
                bot_reply = ""
                for chunk in client.models.generate_content_stream(
                    model=model,
                    contents=contents,
                    config=generate_content_config,
                ):
                    bot_reply += chunk.text  # Append the text from each chunk

                if bot_reply:
                    return JsonResponse({"reply": bot_reply})
                else:
                    return JsonResponse({"reply": "Sorry, there was no response."})

            return JsonResponse({"error": "No message provided"}, status=400)
        except Exception as e:
            # Catch any exceptions and return an error response
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)


def home(request):
    # Fetch the most recent tenders (assuming `publication_date` is in a sortable date format)
    recent_tenders = Tender.objects.all().order_by('publication_date')[:5]

    return render(request, 'tenders/home.html', {'recent_tenders': recent_tenders})

# def home(request):
#     # recent_tenders = Tender.objects.filter(status='active').order_by('-created_at')[:5]
#     return render(request, 'tenders/home.html')#, {'recent_tenders': recent_tenders})

def about(request):
    return render(request, 'about.html')

# def contact(request):
#     return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            # Save to MongoDB
            ContactMessage.objects.create(name=name, email=email, message=message)
            return JsonResponse({"success": True})  # Return JSON response
        
    return render(request, "contact.html")

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')


@login_required
def tender_list(request):
    # Get all tenders from the database
    query = request.GET.get('q', '')
    tenders = Tender.objects.all()
    if query:
        tenders = tenders.filter(tender_title__icontains=query)
    
    paginator = Paginator(tenders, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'tenders/tender_list.html', {'page_obj': page_obj})

# @login_required
# def tender_list(request):
#     tenders = Tender.objects.filter(status='active').order_by('-created_at')
#     return render(request, 'tenders/tender_list.html', {'tenders': tenders})

# @login_required
# def tender_list(request):
#     # Filter tenders by status
#     tenders = Tender.objects.filter(status='active').order_by('-created_at')

#     # Apply filters if any filter is selected in the GET request
#     tender_type = request.GET.get('type')
#     if tender_type:
#         tenders = tenders.filter(type=tender_type)

#     # Paginate the tenders
#     paginator = Paginator(tenders, 5)  # Show 5 tenders per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'tenders/tender_list.html', {'page_obj': page_obj})


@login_required
def tender_detail(request, pk):
    tender = get_object_or_404(Tender, pk=pk)
    return render(request, 'tenders/tender_detail.html', {'tender': tender})

@login_required
def create_tender(request):
    if not (request.user.is_superuser or request.user.is_company()):
        messages.error(request, 'You do not have permission to create tenders.')
        return redirect('tenders:tender_list')

    if request.method == 'POST':
        tender = Tender(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            type=request.POST.get('type'),
            category=request.POST.get('category'),
            deadline=datetime.strptime(request.POST.get('deadline'), '%Y-%m-%d'),
            value=float(request.POST.get('value', 0)),
            location=request.POST.get('location'),
            requirements=request.POST.get('requirements'),
            scope=request.POST.get('scope'),
            author=request.user
        )
        tender.save()
        messages.success(request, 'Tender created successfully!')
        return redirect('tenders:tender_list')
    return render(request, 'tenders/create_tender.html')

@login_required
def toggle_favorite(request, pk):
    if request.method == 'POST':
        tender = get_object_or_404(Tender, pk=pk)
        user = request.user
        if tender in user.favorite_tenders.all():
            user.favorite_tenders.remove(tender)
            messages.success(request, 'Removed from favorites!')
        else:
            user.favorite_tenders.add(tender)
            messages.success(request, 'Added to favorites!')
    return redirect('tenders:tender_detail', pk=pk)

def news(request):
    """View for displaying business news."""
    return render(request, 'news.html')