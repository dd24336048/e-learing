from django import template
from app01.models import OptionalTopicNumber2

register = template.Library()

@register.simple_tag
def get_optional_topic(selected_year):
    topic_number = f"{selected_year}-1"
    try:
        optional_topic = OptionalTopicNumber2.objects.get(topic_number=topic_number)
        return optional_topic.topic
    except OptionalTopicNumber2.DoesNotExist:
        return "Topic not found"
