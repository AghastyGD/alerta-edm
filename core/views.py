from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from itertools import groupby
from operator import attrgetter

from .scraper import PowerOutageScraper
from .models import PowerOutage

class RunScraping(View):
    def get(self, request, *args, **kwargs):
        try:
            scraper = PowerOutageScraper()  
            scraper.scrape()  
            return JsonResponse({'status': 'success', 'message': 'Scraping completed successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

class PowerOutageList(ListView):
    model = PowerOutage
    template_name = 'core/power_outage_list.html'
    context_object_name = 'future_outages'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()

        future_outages = PowerOutage.objects.filter(date__gte=today).order_by('date')
        past_outages = PowerOutage.objects.filter(date__lt=today).order_by('-date')[:5]

        grouped_future_outages = []
        for date, group in groupby(future_outages, key=attrgetter('date')):
            grouped_future_outages.append({
                'date': date,
                'outages': list(group)
            })

        context.update({
            'future_outages': grouped_future_outages,
            'past_outages': past_outages,
            'today': today,
        })

        return context


class PowerOutageDetail(DetailView):
    model = PowerOutage
    template_name = 'core/power_outage_detail.html'
    context_object_name = 'outage'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
