from rest_framework.views import APIView, status
from rest_framework.decorators import api_view, permission_classes, action, authentication_classes
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ReviewSerializer, BookingSerializer, ListingSerializer, PaymentSerializer
from .models import Listing, Booking, Review, Payment
from .tasks import send_booking_confirmation_email
import os
import requests

# Create your views here.

class ListingViewset(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewset(viewsets.ModelViewSet):

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        booking_id = response.data.get('id')
        booking = Booking.objects.get(id=booking_id)
        amount = booking.price  # Adjust field name if needed
        user_email = booking.user.email

        # 2. Trigger email asynchronously
        send_booking_confirmation_email.delay(user_email, booking_id)
        
        # Initiate payment
        payload = {
            "amount": str(amount),
            "currency": "ETB",
            "email": user_email,
            "tx_ref": f"booking_{booking_id}_{booking.user.id}",
            "return_url": "https://yourdomain.com/payment/verify/",  # Change to your frontend URL
        }
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        chapa_response = requests.post(CHAPA_BASE_URL, json=payload, headers=headers)
        data = chapa_response.json()
        if data.get("status") == "success":
            payment = Payment.objects.create(
                booking=booking,
                amount=amount,
                transaction_id=data["data"]["tx_ref"],
                status="Pending"
            )
            response.data["payment_checkout_url"] = data["data"]["checkout_url"]
            response.data["payment_id"] = payment.id
        else:
            response.data["payment_error"] = data.get("message", "Payment initiation failed")
        return response


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer




CHAPA_BASE_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"
CHAPA_SECRET_KEY = os.environ.get("CHAPA_SECRET_KEY")

class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=["post"])
    def initiate(self, request):
        booking_id = request.data.get("booking_id")
        amount = request.data.get("amount")
        user_email = request.data.get("email")
        booking = Booking.objects.get(id=booking_id)
        payload = {
            "amount": str(amount),
            "currency": "ETB",
            "email": user_email,
            "tx_ref": f"booking_{booking_id}_{booking.user.id}",
            "return_url": "https://yourdomain.com/payment/verify/",  # Change to your frontend URL
        }
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        response = requests.post(CHAPA_BASE_URL, json=payload, headers=headers)
        data = response.json()
        if data.get("status") == "success":
            payment = Payment.objects.create(
                booking=booking,
                amount=amount,
                transaction_id=data["data"]["tx_ref"],
                status="Pending"
            )
            return Response({
                "checkout_url": data["data"]["checkout_url"],
                "payment_id": payment.id
            }, status=status.HTTP_201_CREATED)
        return Response({"error": data.get("message", "Payment initiation failed")}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def verify(self, request):
        payment_id = request.data.get("payment_id")
        payment = Payment.objects.get(id=payment_id)
        tx_ref = payment.transaction_id
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        response = requests.get(f"{CHAPA_VERIFY_URL}{tx_ref}", headers=headers)
        data = response.json()
        if data.get("status") == "success" and data["data"]["status"] == "success":
            payment.status = "Completed"
            payment.save()
            # TODO: Trigger Celery email task here
            return Response({"status": "Completed"}, status=status.HTTP_200_OK)
        else:
            payment.status = "Failed"
            payment.save()
            return Response({"status": "Failed", "detail": data.get("message")}, status=status.HTTP_400_BAD_REQUEST)


