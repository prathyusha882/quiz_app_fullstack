import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentSerializer

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            data = request.data
            amount = data.get('amount')  # Amount in cents
            currency = data.get('currency', 'usd')
            description = data.get('description', 'Quiz App Payment')
            
            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                description=description,
                metadata={
                    'user_id': request.user.id,
                    'user_email': request.user.email,
                }
            )
            
            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                amount=amount / 100,  # Convert from cents to dollars
                currency=currency,
                description=description,
                payment_method='stripe',
                status='pending',
                external_id=intent.id
            )
            
            return Response({
                'client_secret': intent.client_secret,
                'payment_id': payment.id,
                'amount': amount,
                'currency': currency
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class PaymentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

class PaymentConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            
            # Confirm payment with Stripe
            intent = stripe.PaymentIntent.retrieve(payment.external_id)
            
            if intent.status == 'succeeded':
                payment.status = 'completed'
                payment.save()
                return Response({'status': 'Payment confirmed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Payment not successful'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentRefundView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            
            # Create refund in Stripe
            refund = stripe.Refund.create(
                payment_intent=payment.external_id
            )
            
            payment.status = 'refunded'
            payment.save()
            
            return Response({'status': 'Payment refunded'}, status=status.HTTP_200_OK)
            
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StripeWebhookView(APIView):
    permission_classes = []
    
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return Response({'error': 'Invalid payload'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response({'error': 'Invalid signature'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            # Update payment status
            try:
                payment = Payment.objects.get(external_id=payment_intent['id'])
                payment.status = 'completed'
                payment.save()
            except Payment.DoesNotExist:
                pass
                
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            # Update payment status
            try:
                payment = Payment.objects.get(external_id=payment_intent['id'])
                payment.status = 'failed'
                payment.save()
            except Payment.DoesNotExist:
                pass
        
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

class PayPalWebhookView(APIView):
    permission_classes = []
    
    def post(self, request):
        # PayPal webhook implementation would go here
        return Response({"message": "PayPal webhook endpoint"}, status=status.HTTP_200_OK) 