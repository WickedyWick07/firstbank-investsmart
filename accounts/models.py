import random
from django.db import models
from django.conf import settings
from decimal import Decimal
from datetime import date, timedelta
from users.models import CustomUser
from django.core.exceptions import ValidationError



class Card(models.Model):
    CARD_TYPES = [
        ('VISA', 'Visa'),
        ('MASTERCARD', 'Mastercard'),
        ('DISCOVER', 'Discover'),
        ('AMEX', 'Amex'),
    ]

    ACCOUNT_TYPES = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Debit'),
        ('SAVINGS', 'Savings'),
        ('CHEQUE', 'Cheque'),
    ]

    INITIAL_DEPOSIT = Decimal('1000.00')

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True, editable=False)
    expiration_date = models.DateField(editable=False)
    cvv = models.CharField(max_length=3, editable=False)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=INITIAL_DEPOSIT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_card_type_display()} card ending in {self.card_number[-4:]}"

    def clean(self):
        super().clean()
        if Card.objects.filter(user=self.user).count() >= 3:
            raise ValidationError("A user cannot have more than 3 cards")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
            self.card_number = self.generate_card_number()
            self.expiration_date = self.generate_expiration_date()
            self.cvv = self.generate_cvv()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_card_number():
        while True:
            number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
            if not Card.objects.filter(card_number=number).exists():
                return number

    @staticmethod
    def generate_expiration_date():
        return date.today() + timedelta(days=365*3)
    
    @staticmethod
    def generate_cvv():
        return ''.join([str(random.randint(0, 9)) for _ in range(3)])


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.date}"
    
    
class Booking(models.Model):
    BANKER_CHOICES = [
        ('Jonathan Davies', 'Jonathan Davies'),
        ('Samantha Brooke', 'Samantha Brooke'),
        ('David Smith', 'David Smith'),
        ('Jim White', 'Jim White'),
        ('Simon Jordan', 'Simon Jordan')     
    ]

    banker_name = models.CharField(max_length=50, choices=BANKER_CHOICES)
    reason_for_booking = models.TextField(max_length=500)
    booking_date = models.DateField()

    def __str__(self):
        return f"{self.banker_name} has been booked for {self.booking_date}"

