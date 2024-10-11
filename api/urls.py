from django.urls import path
from rest_framework import permissions
from .views import PowerOutageList, PowerOutageDetail, PowerOutagesByState
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(openapi.Info(
    title="Power Outage API",
    default_version='v1',
    description='Welcome to the Alerta EDM API Documentation',
),  public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('power-outages/', PowerOutageList.as_view(), name='power_outages'),
    path('power-outage/<int:pk>/', PowerOutageDetail.as_view(), name='power_outage_detail'),
    path('power-outages/<slug:slug>/', PowerOutagesByState.as_view(),  name='power_outages_by_province'),
    
]
