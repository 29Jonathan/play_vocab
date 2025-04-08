from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.views import generic
from .forms import VocabForm
from .models import Vocab
import random
import requests
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import login


def index(request):
    """View function for home page of site."""
    # Check if the reset parameter is present
    if 'reset' in request.GET:
        request.session['rounds_played'] = -1  # Reset the rounds played

    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    status_filter = request.GET.get('status', '')  # Get the status filter from the query parameters

    # Filter vocab based on the logged-in user
    if request.user.is_authenticated:
        vocab_list = Vocab.objects.filter(user=request.user)  # Show only vocab entries for the logged-in user
    else:
        vocab_list = Vocab.objects.none()  # Return an empty queryset for unauthenticated users

    # Further filter vocab based on search query and status
    if search_query:
        vocab_list = vocab_list.filter(word__icontains=search_query)
    if status_filter:
        vocab_list = vocab_list.filter(status=status_filter)

    # Count vocab entries for the logged-in user
    num_vocabs = vocab_list.count()
    num_memorized = vocab_list.filter(status__exact='m').count()
    num_learning = vocab_list.filter(status__exact='l').count()
    num_forgot = vocab_list.filter(status__exact='f').count()

    context = {
        'vocab_list': vocab_list,
        'search_query': search_query,
        'status_filter': status_filter,
        'num_vocabs': num_vocabs,
        'num_memorized': num_memorized,
        'num_learning': num_learning,
        'num_forgot': num_forgot,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class VocabDetailView(generic.DetailView):
    model = Vocab


class VocabUpdateView(UpdateView):
    model = Vocab
    form_class = VocabForm
    template_name = 'edit_vocab.html'

    def get_success_url(self):
        return reverse('index')  # Redirect to the index page after editing
    
    
def add_vocab(request):
    if request.method == 'POST':
        form = VocabForm(request.POST)
        if form.is_valid():
            vocab = form.save(commit=False)
            vocab.user = request.user  # Associate the vocab entry with the logged-in user
            vocab.save()
            return redirect('index')  # Redirect to the vocab list page (or any other page)
    else:
        form = VocabForm()

    return render(request, 'add_vocab.html', {'form': form})


def word_scramble(request):
    # Check if the user wants to reset the game
    if 'reset' in request.GET:
        request.session['rounds_played'] = 0  # Reset the rounds played
        return redirect('index')  # Redirect to the index page

    # Ensure the user is logged in
    if not request.user.is_authenticated:
        request.session['alert_message'] = "Please Login!"
        return redirect('index')  # Redirect to the index page for unauthenticated users

    # Initialize or increment the round counter in the session
    if 'rounds_played' not in request.session:
        request.session['rounds_played'] = 0
    elif request.session['rounds_played'] >= 9:
        del request.session['rounds_played']  # Delete the counter
        return redirect('index')  # Redirect to the index page
    else:
        request.session['rounds_played'] += 1

    # Select a random word from the logged-in user's vocab
    vocab_list = Vocab.objects.filter(user=request.user)
    if not vocab_list.exists():
        return redirect('index')  # Redirect if no vocab entries exist for the user

    vocab = random.choice(vocab_list)
    selected_word = vocab.word
    scrambled_word = ''.join(random.sample(selected_word, len(selected_word)))

    # Store the selected word in the session
    request.session['selected_word'] = selected_word

    context = {
        'vocab': vocab,
        'scrambled_word': scrambled_word,
        'rounds_left': 10 - request.session['rounds_played'],  # Show remaining rounds
    }
    return render(request, 'word_scramble.html', context)


def check_answer(request):
    if request.method == 'POST':
        user_input = request.POST.get('userInput', '').strip()
        selected_word = request.session.get('selected_word', '')

        # Compare the user's input with the selected word
        if user_input.lower() == selected_word.lower():
            return JsonResponse({'correct': True, 'selected_word': selected_word})
        else:
            return JsonResponse({'correct': False, 'selected_word': selected_word})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def dictionary(request):
    """View function for dictionary page."""
    dictionary_query = request.GET.get('search_dictionary', '')
    
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{dictionary_query}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        word = data['word']
        phonetics = data.get('phonetics', [])
        meanings = data.get('meanings', [])
        definitions = []
        for meaning in meanings:
            part_of_speech = meaning.get('partOfSpeech', '')
            definition_list = meaning.get('definitions', [])
            for definition in definition_list:
                definitions.append({
                    'partOfSpeech': part_of_speech,
                    'definition': definition.get('definition', ''),
                    'example': definition.get('example', ''),
                })
    else:
        return redirect('index')
        
    context = {
        'word': word,
        'phonetics': phonetics,
        'definitions': definitions,
    }
    
    return render(request, 'dictionary.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after sign-up
            return redirect('index')  # Redirect to the home page or another page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})






