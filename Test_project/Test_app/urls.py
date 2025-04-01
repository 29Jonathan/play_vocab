from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.VocabDetailView.as_view(), name='vocab-detail'),
    path('add/', views.add_vocab, name='add_vocab'),
    path('edit/<int:pk>/', views.VocabUpdateView.as_view(), name='edit_vocab'),
    path('word_scramble/', views.word_scramble, name='word_scramble'),
    path('check_answer/', views.check_answer, name='check_answer'),
    path('dictionary/', views.dictionary, name='dictionary'),
    # path('authors/', views.AuthorListView.as_view(), name='authors'),
    # path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

