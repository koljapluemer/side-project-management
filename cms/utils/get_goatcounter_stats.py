import requests
from datetime import datetime, timedelta

def get_goatcounter_stats(goatcounter_id, api_key):
    """Fetch stats from GoatCounter API."""
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
        
        views_today = 0
        views_week = 0
        
        if data.get('hits'):
            stats = data['hits'][0]['stats']
            if stats:
                views_today = stats[-1]['daily']
                views_week = sum(day['daily'] for day in stats)
        
        print(f"Stats fetched successfully: Today: {views_today}, This Week: {views_week}")
        return {
            'views_today': views_today,
            'views_week': views_week
        }
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch stats: Network error - {str(e)}")
        return None
    except Exception as e:
        print(f"Failed to fetch stats: Unexpected error - {str(e)}")
        return None
