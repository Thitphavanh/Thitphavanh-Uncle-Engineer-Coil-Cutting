import os
import sys
import django
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.dev')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS += ['testserver', '127.0.0.1', 'localhost']

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from coil.models import CoilIn
from coil.views import index, coilin_list, CoilInCreateView, CoilInDetailView

def test_rbac():
    print("Verifying RBAC implementation...")
    
    # Get users
    user1 = User.objects.get(username='user1') # Admin/All
    user2 = User.objects.get(username='user2') # Key-in
    user3 = User.objects.get(username='user3') # Key-out
    view4 = User.objects.get(username='view4') # Viewer
    
    client = Client()
    
    # 1. Test View Access (Views that should be restricted)
    print("\n--- Testing View Access ---")
    
    # Coil In Create (Only Coil_In: user1, user2)
    url = reverse('coil:coilin_create')
    print(f"Testing {url} (Requires Coil_In)")
    
    client.force_login(view4)
    resp = client.get(url)
    print(f"Viewer (view4): {resp.status_code} (Expected 302/403)")
    
    client.force_login(user3)
    resp = client.get(url)
    print(f"Coil Out (user3): {resp.status_code} (Expected 302/403)")
    
    client.force_login(user2)
    resp = client.get(url)
    print(f"Coil In (user2): {resp.status_code} (Expected 200)")
    
    client.force_login(user1)
    resp = client.get(url)
    print(f"Admin (user1): {resp.status_code} (Expected 200)")

    # Coil Out Create (Only Coil_Out: user1, user2, user3)
    url = reverse('coil:coilout_create')
    print(f"\nTesting {url} (Requires Coil_Out)")
    
    client.force_login(view4)
    resp = client.get(url)
    print(f"Viewer (view4): {resp.status_code} (Expected 302/403)")
    
    client.force_login(user3)
    resp = client.get(url)
    print(f"Coil Out (user3): {resp.status_code} (Expected 200)")

    # 2. Test Template Visibility (Check for button text)
    print("\n--- Testing Template Visibility ---")
    
    # Index Page - "Create SKU" (Only SKU_Manager: user1)
    url = reverse('coil:index')
    print(f"Testing {url} for 'Create SKU' button")
    
    client.force_login(view4)
    resp = client.get(url)
    if b'skuModal' in resp.content and b'hidden' not in resp.content: # Button reveals modal? No, check for button HTML
        # Button HTML: <button id="openSkuModal" ...
        has_button = b'id="openSkuModal"' in resp.content
        print(f"Viewer (view4): Has button? {has_button} (Expected False)")
    else:
        has_button = b'id="openSkuModal"' in resp.content
        print(f"Viewer (view4): Has button? {has_button} (Expected False)")

    client.force_login(user1)
    resp = client.get(url)
    has_button = b'id="openSkuModal"' in resp.content
    print(f"Admin (user1): Has button? {has_button} (Expected True)")

    # Coil In List - "New Coil In" (Only Coil_In: user1, user2)
    url = reverse('coil:coilin_list') # Wait, I didn't add button to coilin_list? 
    # Ah, I decided NOT to add it to coilin_list because it wasn't there.
    # But I updated coilout_list. Let's test coilout_list.
    
    url = reverse('coil:coilout_list')
    print(f"\nTesting {url} for 'New Coil Out' button")
    
    client.force_login(view4)
    resp = client.get(url)
    has_button = b'href="/coilout/create/"' in resp.content # Check URL in href
    print(f"Viewer (view4): Has button? {has_button} (Expected False)")
    
    client.force_login(user3)
    resp = client.get(url)
    has_button = b'coilout/create/' in resp.content
    print(f"Coil Out (user3): Has button? {has_button} (Expected True)")

    # 3. Test Login/Logout
    print("\n--- Testing Login/Logout ---")
    client.logout()
    
    # Login Page
    url = reverse('login')
    resp = client.get(url)
    print(f"Login Page: {resp.status_code} (Expected 200)")
    
    # Protected Page Redirect
    url = reverse('coil:coilin_create')
    resp = client.get(url)
    print(f"Access Protected Redirect: {resp.status_code} (Expected 302)")
    if resp.status_code == 302:
        print(f"Redirect URL: {resp.url} (Expected /login/?next=/coilin/create/)")

if __name__ == '__main__':
    test_rbac()
