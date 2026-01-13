from .utils import reserve_status

def reserve_context(request):
    return {
        "get_reserve_status": reserve_status
    }
  
