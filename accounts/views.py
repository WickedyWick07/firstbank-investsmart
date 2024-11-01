from rest_framework import status 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from .models import Card, Transaction, Booking
from .serializers import CardSerializer, TransactionSerializer, BookingSerializer
from django.contrib.auth import get_user_model


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def card_list(request):
    if request.method == 'GET':
        cards = Card.objects.filter(user=request.user)
        serializer = CardSerializer(cards, many=True )
        return Response(serializer.data)

    elif request.method == 'POST':

        if Card.objects.filter(user=request.user).count() >= 3:
            return Response({'detail':'A user cannot have more than 3 cards'})
        serializer = CardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            print(f"User ID from request: {request.user.id}")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def card_detail(request, id):
    try: 
        card = Card.objects.get(pk=id, user=request.user)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CardSerializer(card)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_card_active(request, pk):
    try:
        card = Card.objects.get(pk=pk, user=request.user)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    card.is_active = not card.is_active
    card.save()
    return Response({'status': 'card updated', 'is_active': card.is_active})

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def card_balance(request, pk):
    try: 
        card = Card.objects.get(pk=pk, user=request.user)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    return Response({'balance': card.balance})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    card_id = request.data.get('card_id')
    amount = request.data.get('amount')

    try:
        card = Card.objects.get(id=card_id, user=request.user)  # Ensure the card belongs to the authenticated user
        card.balance += amount
        card.save()

        # Create a corresponding transaction
        Transaction.objects.create(card=card, amount=amount, transaction_type='deposit')

        return Response({'message': 'Deposit successful', 'new_balance': card.balance}, status=status.HTTP_200_OK)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    card_id = request.data.get('card_id')
    amount = request.data.get('amount')

    try:
        card = Card.objects.get(id=card_id, user=request.user)  # Ensure the card belongs to the authenticated user

        if card.balance >= amount:
            card.balance -= amount
            card.save()

            # Create a corresponding transaction
            Transaction.objects.create(card=card, amount=amount, transaction_type='withdrawal')

            return Response({'message': 'Withdrawal successful', 'new_balance': card.balance}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
    except Card.DoesNotExist:
        return Response({'error': 'Card not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request, card_id=None):
    try:
        # Fetch transactions filtered by card if card_id is provided
        if card_id:
            transactions = Transaction.objects.filter(card__id=card_id, card__user=request.user)
        else:
            # Fetch all transactions for all cards of the user
            transactions = Transaction.objects.filter(card__user=request.user)

        if not transactions.exists():
            return Response({'error': 'No transactions found'}, status=404)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    except Exception as e: 
        return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(card, amount, transaction_type):
    # Assume `card` is a Card instance and amount is a positive number.
    transaction = Transaction(card=card, amount=amount, transaction_type=transaction_type)
    transaction.save()
    return transaction


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_transactions(user):
    transactions = Transaction.objects.filter(card__user=user)  # Fetch all transactions for the user's cards
    return transactions


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

