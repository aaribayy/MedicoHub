# from django.contrib import admin
# from home.models import SignUp, Register, Feedback, Prediction

# # Register your models here.
# admin.site.register(SignUp)
# admin.site.register(Register)
# admin.site.register(Feedback)
# admin.site.register(Prediction)


# from django.utils.html import format_html

# @admin.register(Feedback)
# class FeedbackAdmin(admin.ModelAdmin):
#     list_display = ('user', 'subject', 'analysis', 'created_at')

#     def changelist_view(self, request, extra_context=None):
#         # Aggregate feedback data
#         queryset = self.get_queryset(request)
#         sentiment_counts = queryset.values('analysis').annotate(count=models.Count('analysis'))

#         sentiment_data = {
#             'strongly positive': 0,
#             'positive': 0,
#             'neutral': 0,
#             'negative': 0,
#             'strongly negative': 0
#         }

#         for entry in sentiment_counts:
#             sentiment_data[entry['analysis']] = entry['count']

#         extra_context = extra_context or {}
#         extra_context['sentiment_data'] = sentiment_data

#         return super().changelist_view(request, extra_context=extra_context)

from django.contrib import admin
from home.models import SignUp, Register, Feedback, Prediction
from django.db.models import Count

# Register your models here.
admin.site.register(SignUp)
admin.site.register(Register)
admin.site.register(Prediction)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'analysis', 'created_at')

    def changelist_view(self, request, extra_context=None):
        # Aggregate feedback data
        queryset = self.get_queryset(request)
        sentiment_counts = queryset.values('analysis').annotate(count=Count('analysis'))

        sentiment_data = {
            'strongly positive': 0,
            'positive': 0,
            'neutral': 0,
            'negative': 0,
            'strongly negative': 0
        }

        for entry in sentiment_counts:
            sentiment_data[entry['analysis']] = entry['count']

        extra_context = extra_context or {}
        extra_context['sentiment_data'] = sentiment_data

        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Feedback, FeedbackAdmin)
