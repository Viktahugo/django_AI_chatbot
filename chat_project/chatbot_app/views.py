# Create your views here. 
import os
import google.generativeai as genai
from django.shortcuts import render
from django.http import HttpResponseServerError,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  #For simplicity, but CSRF protection is important in production
def chat_view(request):
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        return HttpResponseServerError("GOOGLE_API_KEY not set")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        if request.method == 'POST':
            data = json.loads(request.body) #Get data from the request
            user_message = data.get('message', '')  # Access message from data
            if user_message:
                try:
                    response = model.generate_content(user_message)
                    bot_response = response.text
                except Exception as e:
                    bot_response = f"Error generating response: {e}"
            else:
                bot_response = "Please enter a message."
            return json_response({'response': bot_response})
        else:
            return render(request, 'chatbot_app/chat.html')

    except Exception as e:
        return HttpResponseServerError(f"An error occurred: {e}")

def json_response(data, status=200):
    return HttpResponse(json.dumps(data), content_type='application/json', status=status)