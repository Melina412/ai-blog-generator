from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import os
import json
import assemblyai as aai
import openai
from pytube import YouTube
from dotenv import load_dotenv
load_dotenv()
from .models import BlogPost

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@csrf_exempt # kann man für development machen
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('req body:', request.body)
            yt_link = data['link'] # 'link' ist der name der json property beim fetch -- JSON.stringify({ link: youtubeLink }) 
           
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data send'}, status=400)
        
        # get yt title
        title = yt_title(yt_link)
        print('title', title)

        # get transcript with assemblyAI
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': 'Failed to get transcript'}, status=500)

        # generate blog with openAI
        blog_content = generate_blog_from_transcription(transcription)
        print('blog content: ', blog_content)
        if not blog_content:
             return JsonResponse({'error': 'Failed to generate blog article'}, status=500)

        # save blog article to database
        new_blog_article = BlogPost.objects.create(
            user = request.user,
            youtube_title = title,
            youtube_link = yt_link,
            generated_content = blog_content,
        )
        new_blog_article.save()

        # return blog article as a response
        # print('blog_content: ', blog_content)
        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def yt_title(link):
    print('getting yt title...')
    yt = YouTube(link)    
    title = yt.title
    return title

def download_audio(link):
    print('downloading audio...')
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file) # out_file speichern
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file


def get_transcription(link):
    print('getting transcription...')
    audio_file = download_audio(link)
    aai_key = os.getenv('AAI_API_KEY')
    # print('aai_key', aai_key)
    aai.settings.api_key = aai_key

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    # print('transcript.text: ', transcript.text)
    return transcript.text

def generate_blog_from_transcription(transcription):
    print('generating blog article...')
    openai.api_key = os.getenv('OPENAI_API_KEY')


    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but do not make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"

    # Completions ist eine legacy methode, in zukunft soll man dafür chat completions nutzen
    response = openai.completions.create(
        # model='text-davinci-003', model ist deprecated
        model='gpt-3.5-turbo-instruct', # vergleichbares model kompatibel mit legacy completions
        prompt=prompt,
        max_tokens=1000
    )

    generated_content = response.choices[0].text.strip()

    # print(' generated_content: ',  generated_content)
    return generated_content
    
def blog_list(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, 'blog-list.html', {'blog_articles': blog_articles})

def blog_details(request, pk):
    blog_article_detail = BlogPost.objects.get(id=pk)
    if request.user == blog_article_detail.user:
        return render(request, 'blog-details.html', {'blog_article_detail': blog_article_detail})
    else:
        return redirect('/')
    

def user_login(request): # das kann nicht nur login heißen wegen der auth login von django
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            error_message = 'invalid username or password'
            return render(request, 'login.html', {'error_message':error_message})

    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        if password == repeatPassword:
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                error_message = 'Error creating account'
        else: 
            error_message = 'password does not match'
            return render(request, 'signup.html', {'error_message':error_message})

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')
