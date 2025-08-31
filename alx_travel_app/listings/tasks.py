# listings/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation_email(customer_email, booking_id):
    subject = f"Booking Confirmation #{booking_id}"
    message = f"Your booking with ID {booking_id} has been confirmed."
    from_email = "noreply@alxtravel.com"
    recipient_list = [customer_email]

    send_mail(subject, message, from_email, recipient_list)
    return f"Email sent to {customer_email} for booking {booking_id}"
