from django.db import models
import uuid
from django.core.exceptions import ValidationError
import datetime

filters = (
        (0, 'no'),
        (1, 'lofi'),
        (2, 'brooklyn'),
        (3, 'gingham'),
        (4, 'valencia'),
        (5, 'willow')
    )


EMAILS = ('gmail.com', 'yahoo.com', 'hotmail.com', 'aol.com', 'hotmail.co.uk', 'hotmail.fr', 
          'msn.com', 'yahoo.fr', 'wanadoo.fr', 'orange.fr', 'comcast.net', 'yahoo.co.uk', 
          'yahoo.com.br', 'yahoo.co.in', 'live.com', 'rediffmail.com', 'free.fr', 'gmx.de', 
          'web.de', 'yandex.ru', 'ymail.com', 'libero.it', 'outlook.com', 'uol.com.br', 
          'bol.com.br', 'mail.ru', 'cox.net', 'hotmail.it', 'sbcglobal.net', 'sfr.fr', 
          'live.fr', 'verizon.net', 'live.co.uk', 'googlemail.com', 'yahoo.es', 'ig.com.br', 
          'live.nl', 'bigpond.com', 'terra.com.br', 'yahoo.it', 'neuf.fr', 'yahoo.de', 
          'alice.it', 'rocketmail.com', 'att.net', 'laposte.net', 'facebook.com', 'bellsouth.net', 
          'yahoo.in', 'hotmail.es')



class MailExistsValidation:
    def __init__(self):
        self.mails: tuple = EMAILS

    def __call__(self, context: str):
        is_email = False
        for mail in self.mails:
            if mail not in context:
                is_email = True
        if not is_email:
            raise ValidationError(
                    '''
                    Введите настоящую почту.
                    ''',
                    code='mail_exception',
                    params={'mails': self.mails, 'current_mail': mail}
                )



class NumberValidation:

    def __init__(self):
        self.fixed=11

    def __call__(self, context: str):
        if len(context)!=self.fixed:
            raise ValidationError(
                '''
                It should be 11 numbers and start with 8.
                ''',
                code='phone_exception',
                params={'current': context}
            )



class User(models.Model):

    def check_num(self):
        if self.phone[0] == '8':
            self.phone = self.phone.replace('8', '+7')
        
    def save(self, *args, **kwargs):
        self.check_num()
        super().save(*args, **kwargs)
    
    def number_validation(stroke: str):
        return NumberValidation()(context=stroke)
    
    def mail_validation(stroke: str):
        return MailExistsValidation()(context=stroke)
    


    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID'
    )
    email = models.CharField(
        max_length=50, db_index=True, verbose_name='Email', blank=False, validators=[mail_validation]
    )
    password = models.CharField(
        max_length=32, db_index=True, verbose_name='Пароль', blank=False
    )
    phone = models.CharField(
        max_length=12, verbose_name='Номер телефона', blank=False, validators=[number_validation]
    )
    full_name = models.CharField(
        max_length=64, verbose_name='Имя Фамилия', blank=False
    )
    info = models.CharField(
        max_length=512, verbose_name='Информация о себе', null=True, blank=True
    )
    kinds = (
        ('1', 'Admin'),
        ('2', 'User')
    )
    status = models.CharField(
        max_length=32, choices=kinds, blank=False, default=kinds[1], verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email',]
        
        
        
class Photo(models.Model):
    id = models.CharField(
        default=str(uuid.uuid4), primary_key=True, verbose_name='ID', max_length=128
    )
    source = models.CharField(
        max_length=100, verbose_name='Source', blank=False
    )
    
    user = models.CharField(
        max_length=32, blank=False, default='Anon'
    )
    
    filter = models.CharField(
        max_length=16, verbose_name='Filter', default=filters[0], choices=filters
    )
    likes = models.IntegerField(
        verbose_name='Likes', default=0
    )
    dislikes = models.IntegerField(
        verbose_name='Dislikes', default=0
    )
    text = models.TextField(
        max_length=1024, blank=True
    )
    datetime = models.DateTimeField(
        default=datetime.datetime.now()
    )
    
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
        ordering = ['text',]
        
            
class Comment(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, verbose_name='ID'
    )
    photo = models.CharField(
        max_length=32, blank=False
    )
    user = models.CharField(
        max_length=32, blank=False
    )
    text = models.TextField(
        max_length=1024, blank=False
    )
    datetime = models.DateTimeField(
        default=datetime.datetime.now()
    )
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['text',]