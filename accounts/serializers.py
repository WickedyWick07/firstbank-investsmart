from rest_framework import serializers
from .models import Card
from .models import Transaction, Booking
from rest_framework.exceptions import ValidationError


class CardSerializer(serializers.ModelSerializer):
    card_type_display = serializers.CharField(source='get_card_type_display', read_only=True)
    account_type_display = serializers.CharField(source='get_account_type_display', read_only=True)
  

    class Meta:
        model = Card
        fields = ['id', 'card_number', 'expiration_date', 'cvv', 'card_type', 'card_type_display', 'account_type', 'account_type_display', 'is_active',
                  'balance', 'created_at', 'updated_at']
        read_only_fields = ['id', 'card_number', 'expiration_date', 'cvv', 'balance', 'created_at', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request context
        if Card.objects.filter(user=user).count() >= 3:
            raise ValidationError('A user cannot have more than 3 cards.')
        card = Card.objects.create(user=user, **validated_data)
        return card



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Booking
        fields = '__all__'

