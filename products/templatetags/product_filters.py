from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def filter_by_rating(reviews, rating):
    """
    Filter reviews by a specific rating
    """
    return [review for review in reviews if review.rating == int(rating)]

@register.filter
def percentage(count, total):
    """
    Calculate percentage
    """
    if total == 0:
        return 0
    return int(count / total * 100)

@register.filter
def product_avg_rating(product):
    """
    Get average rating for a product
    """
    return product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] 