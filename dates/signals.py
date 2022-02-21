import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from dates.models import Follower


@receiver(post_save, sender=Follower)
def notify_users(sender, instance, **kwargs):
    """Inform users about match"""
    user_1 = instance.user_1
    user_2 = instance.user_2
    followers = Follower.objects.filter(user_2=user_1)
    for user in followers:
        if user.user_1 == user_2 and user.user_2 == user_1:
            send_matching_letters(user_1, user_2)


def send_matching_letters(user_1, user_2):
    """Sending mail to matching users"""

    subject = 'Hey, you have a new mail!'
    from_email = os.getenv('DEFAULT_FROM_EMAIL')

    for user in (user_1, user_2):
        if user == user_1:
            text = f'Вы понравились {user_2.first_name}! Почта участника: {user_2.email}'
        else:
            text = f'Вы понравились {user_1.first_name}! Почта участника: {user_1.email}'

        send_mail(
            subject=subject,
            message=text,
            from_email=from_email,
            recipient_list=[user.email]
        )
