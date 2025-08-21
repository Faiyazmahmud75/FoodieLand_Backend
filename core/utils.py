from django.conf import settings
from django.core.mail import send_mail

def send_email(subject, message, recipient_list, html_message=None):
	send_mail(
		subject=subject,
		message=message,
		from_email=settings.DEFAULT_FROM_EMAIL,
		recipient_list=recipient_list,
		fail_silently=False,
		html_message=html_message
	) 