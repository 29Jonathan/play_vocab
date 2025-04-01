from django.db import models
from django.urls import reverse # Used in get_absolute_url() to get URL for specified ID

class Vocab(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    word = models.CharField(max_length=20)
    
    CATEGORY = (
        ('n', 'Noun'),
        ('v', 'Verb'),
        ('adj', 'Adjective'),
        ('adv', 'Adverb'),
        ('prep', 'Preposition'),
        ('conj', 'Conjunction'),
        ('pron', 'Pronoun'),
        ('int', 'Interjection')
    )
    category = models.CharField(
        max_length=4,
        choices=CATEGORY,
        null=True,
        blank=True,
        help_text='Word Class',
    )  
      
    STATUS = (
        ('m', 'memorized'),
        ('l', 'learning'),
        ('f', 'forgot')
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default='l',
        help_text='Study Status',
    )    
    
    meaning = models.CharField('Meaning', null=True, blank=True, max_length=200)
    
    example = models.CharField('Example', null=True, blank=True, max_length=200)

    created_at = models.DateField(auto_now_add=True, help_text='The date the vocab was created.', null=True, blank=True)

    
    def __str__(self):
        """String for representing the Model object."""
        return self.word
    
    def get_absolute_url(self):
        """Returns the url to access a particular vocab instance."""
        return reverse('vocab-detail', args=[str(self.id)])
    
    def get_full_category_name(self):
        return dict(self.CATEGORY)[self.category]\
            
    def get_full_status_name(self):
        return dict(self.STATUS)[self.status]
        
