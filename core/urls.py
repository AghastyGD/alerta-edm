from django.urls import path
from .views import (
    PowerOutageList, PowerOutageDetail, RunScraping
)

urlpatterns = [
    path('', PowerOutageList.as_view(), name='power_outage_list'),
    path('outage/<slug:slug>/', PowerOutageDetail.as_view(), name='power_outage_detail'),
    path('run-scraper/', RunScraping.as_view(), name='run_scraper'),
]
