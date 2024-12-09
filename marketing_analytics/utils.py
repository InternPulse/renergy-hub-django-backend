from .models import Cart

def calculate_cart_abandonment_rate():
    total_carts = Cart.objects.count()  # Total carts
    purchased_carts = Cart.objects.filter(is_purchased=True).count()  # Carts converted to orders
    abandoned_carts = total_carts - purchased_carts  # Remaining carts

    # Calculate abandonment rate
    abandonment_rate = (abandoned_carts / total_carts * 100) if total_carts > 0 else 0

    return {
        'total_carts': total_carts,
        'purchased_carts': purchased_carts,
        'abandoned_carts': abandoned_carts,
        'abandonment_rate': abandonment_rate,
    }
