from rest_framework import generics, views
from rest_framework.response import Response
from .serializers import PowerOutageSerializer
from core.models import PowerOutage
from datetime import datetime

# PowerOutage List API View
class PowerOutageList(generics.ListAPIView):
    """
    Endpoint to list all power outages
    """
    queryset = PowerOutage.objects.all()
    serializer_class = PowerOutageSerializer
    
    def get_queryset(self):
        """
        Filter outages by date
        """
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date and end_date:
            return PowerOutage.objects.filter(date__range=[start_date, end_date])
        else:
            return PowerOutage.objects.all()
    

class PowerOutageDetail(generics.RetrieveAPIView):
    """
    Endpoint to retrieve power outage details
    """
    queryset = PowerOutage.objects.all()
    serializer_class = PowerOutageSerializer


# PowerOutage by State API View
class PowerOutagesByState(views.APIView):

    def get(self, request, slug, *args, **kwargs):
        """
        Endpoint to filter scheduled outages by state and optionally by date.
        """
        power_outages = PowerOutage.objects.filter(slug__startswith=slug)
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if start_date and end_date:
            power_outages = power_outages.filter(date__range=[start_date, end_date])
            
        if not power_outages.exists():
            return Response({"error": "No power outages found for this state."}, status=404)
        
        # group by date
        outages_by_date = {}
        
        for outage in power_outages:
            date = outage.date
            if date not in outages_by_date:
                outages_by_date[date] = []
            outages_by_date[date].append({
                "area": outage.area,
                "affected_zone": outage.affected_zone,
                "start_time": outage.start_time.strftime('%H:%M'),
                "end_time": outage.end_time.strftime('%H:%M'),
            })

        response_data = {
            "province": power_outages.first().state,
            "total_outages": len(power_outages),
            "outages": [{"date": date, "locations": locations} for date, locations in outages_by_date.items()]
        }

        return Response(response_data)