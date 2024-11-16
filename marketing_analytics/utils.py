from django.utils.timezone import now
from datetime import timedelta
from .models import Cart

ABANDONMENT_THRESHOLD = timedelta(hours=24)  # Define abandonment threshold

def get_cart_abandonment_rate():
    """
    Calculate the cart abandonment rate.
    """
    time_threshold = now() - ABANDONMENT_THRESHOLD

    # Total carts created within the threshold
    total_carts = Cart.objects.filter(created_at__gte=time_threshold).count()

    # Abandoned carts (not checked out and inactive for the threshold period)
    abandoned_carts = Cart.objects.filter(
        is_checked_out=False,
        updated_at__lte=time_threshold
    ).count()

    if total_carts == 0:
        return 0  # Avoid division by zero

    return (abandoned_carts / total_carts) * 100
