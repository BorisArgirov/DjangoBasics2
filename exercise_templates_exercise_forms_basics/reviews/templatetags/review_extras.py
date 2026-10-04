from django import template

register = template.Library()


@register.filter
def stars(rating):
    """Display one asterisk for each whole rating point."""
    try:
        return "*" * max(0, int(rating))
    except (TypeError, ValueError, OverflowError):
        return ""
