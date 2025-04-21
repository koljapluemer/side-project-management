import requests
from datetime import datetime, timedelta
from django.utils import timezone
from cms.models import PageViewDay

def get_goatcounter_stats(goatcounter_id, api_key, project):
    """Fetch stats from GoatCounter API and store in PageViewDay model."""
    if not goatcounter_id or not api_key:
        print("Missing GoatCounter ID or API key")
        return None
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    url = f'https://{goatcounter_id}.goatcounter.com/api/v0/stats/hits'
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch stats: HTTP {response.status_code}")
            return None
            
        data = response.json()
        print("API Response:", data)  # Debug print
        
        views_today = 0
        
        if data.get('hits'):
            stats = data['hits'][0]['stats']
            if stats:
                # Process each day's stats
                for day_stats in stats:
                    # The field is called 'day' in the API response
                    date = datetime.strptime(day_stats['day'], '%Y-%m-%d').date()
                    views = day_stats['daily']
                    
                    # Update or create PageViewDay entry
                    page_view, created = PageViewDay.objects.update_or_create(
                        date=date,
                        project=project,
                        defaults={'views': views}
                    )
                    
                    print(f"Updated PageViewDay for {date}: {views} views")
                    
                    # Store today's views for return value
                    if date == timezone.now().date():
                        views_today = views
        
        return {
            'views_today': views_today
        }
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch stats: Network error - {str(e)}")
        return None
    except Exception as e:
        print(f"Failed to fetch stats: Unexpected error - {str(e)}")
        print(f"Error details: {str(e)}")
        return None
