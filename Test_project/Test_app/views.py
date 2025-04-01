from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.views import generic
from .forms import VocabForm
from .models import Vocab
import random
import requests
from django.http import JsonResponse


def index(request):
    """View function for home page of site."""
    # Check if the reset parameter is present
    if 'reset' in request.GET:
        request.session['rounds_played'] = -1  # Reset the rounds played

    
    search_query = request.GET.get('search', '')  # Get the search term from the query parameters
    status_filter = request.GET.get('status', '')  # Get the status filter from the query parameters

    # Filter vocab based on search query and status
    vocab_list = Vocab.objects.all()
    if search_query:
        vocab_list = vocab_list.filter(word__icontains=search_query)
    if status_filter:
        vocab_list = vocab_list.filter(status=status_filter)


    num_vocabs = Vocab.objects.all().count()
    num_memerized = Vocab.objects.filter(status__exact='m').count()
    num_learning = Vocab.objects.filter(status__exact='l').count()
    num_forgot = Vocab.objects.filter(status__exact='f').count()

    context = {
        'vocab_list': vocab_list,
        'search_query': search_query,
        'status_filter': status_filter,
        'num_vocabs': num_vocabs,
        'num_memerized': num_memerized,
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
            form.save()  # Save the new vocab entry to the database
            return redirect('index')  # Redirect to the vocab list page (or any other page)
    else:
        form = VocabForm()

    return render(request, 'add_vocab.html', {'form': form})


def word_scramble(request):
    # Check if the user wants to reset the game
    if 'reset' in request.GET:
        request.session['rounds_played'] = 0  # Reset the rounds played
        return redirect('index')  # Redirect to the index page

    
    # Initialize or increment the round counter in the session
    if 'rounds_played' not in request.session:
        request.session['rounds_played'] = 0
    elif request.session['rounds_played'] >= 9:
        del request.session['rounds_played']  # Delete the counter
        return redirect('index')  # Redirect to the index page
    else:
        request.session['rounds_played'] += 1

    # Select a random word from the database
    vocab = random.choice(Vocab.objects.all())
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