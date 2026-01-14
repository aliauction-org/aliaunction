import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/users/login/"
REGISTER_URL = f"{BASE_URL}/users/register/"

visited = set()
broken_links = []
errors = []

def is_internal(url):
    return url.startswith(BASE_URL) or url.startswith("/")

def crawl(url):
    if url in visited:
        return
    visited.add(url)
    
    # Normalize URL
    if url.startswith("/"):
        full_url = urljoin(BASE_URL, url)
    else:
        full_url = url
    
    print(f"Checking {full_url}...")
    
    try:
        response = requests.get(full_url, timeout=5)
        if response.status_code >= 400:
            broken_links.append(f"{full_url} (Status: {response.status_code})")
            return
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check all links
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href or href.startswith('#') or href.startswith('javascript'):
                continue
                
            full_href = urljoin(full_url, href)
            
            if is_internal(full_href):
                # Just check status for now, recurse if needed (limiting recursion for speed)
                if full_href not in visited and len(visited) < 50: 
                    crawl(full_href)
                elif full_href not in visited:
                     check_status(full_href)

    except Exception as e:
        errors.append(f"Error accessing {full_url}: {str(e)}")

def check_status(url):
    if url in visited: return
    visited.add(url)
    print(f"  Verifying {url}...")
    try:
        r = requests.head(url, timeout=5)
        if r.status_code >= 400:
            # Fallback to GET if HEAD fails (some servers deny HEAD)
            r = requests.get(url, timeout=5)
            if r.status_code >= 400:
                broken_links.append(f"{url} (Status: {r.status_code})")
    except Exception as e:
        errors.append(f"Error verifying {url}: {str(e)}")

print("Starting comprehensive frontend crawl...")

# Seed URLs
crawl(BASE_URL)
crawl(LOGIN_URL)
crawl(REGISTER_URL)
crawl(f"{BASE_URL}/auctions/create/") # Should redirect, verify it doesn't 500
crawl(f"{BASE_URL}/auctions/8/") # Check an auction detail page

print("\n--- Report ---")
if broken_links:
    print("Found Broken Links:")
    for link in broken_links:
        print(f" - {link}")
else:
    print("No broken links found.")

if errors:
    print("\nErrors encountered:")
    for err in errors:
        print(f" - {err}")
