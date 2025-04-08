from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.VocabDetailView.as_view(), name='vocab-detail'),
    path('add/', views.add_vocab, name='add_vocab'),
    path('edit/<int:pk>/', views.VocabUpdateView.as_view(), name='edit_vocab'),
    path('word_scramble/', views.word_scramble, name='word_scramble'),
    path('check_answer/', views.check_answer, name='check_answer'),
    path('dictionary/', views.dictionary, name='dictionary'),
]


urlpatterns += [
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Logout
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Sign-up
    path('signup/', views.signup, name='signup'),
]

urlpatterns += [
    path('export/csv/', views.export_vocab_csv, name='export_vocab_csv'),
    path('export/pdf/', views.export_vocab_pdf, name='export_vocab_pdf'),
]