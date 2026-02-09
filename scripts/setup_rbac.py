import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.dev')
django.setup()

from django.contrib.auth.models import User, Group

def setup_rbac():
    # 1. Create Groups
    groups = {
        'SKU_Manager': [], # Add SKU
        'Coil_In': [],     # Key-in
        'Coil_Out': [],    # Key-out
        'Adjuster': [],    # Key-adj (Edit/Delete)
        'Viewer': [],      # View
    }

    created_groups = {}
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        created_groups[group_name] = group
        if created:
            print(f"Created Group: {group_name}")
        else:
            print(f"Group exists: {group_name}")

    # 2. Create Users and Assign Groups
    users_config = [
        {
            'username': 'admin',
            'password': 'ADMIN123123',
            'groups': ['SKU_Manager', 'Coil_In', 'Coil_Out', 'Adjuster', 'Viewer'],
            'is_superuser': True,
            'is_staff': True
        },
        {
            'username': 'user1',
            'password': 'PWD123123',
            'groups': ['SKU_Manager', 'Coil_In', 'Coil_Out', 'Adjuster']
        },
        {
            'username': 'user2',
            'password': 'pass2233',
            'groups': ['Coil_In', 'Coil_Out']
        },
        {
            'username': 'user3',
            'password': 'ppp3344',
            'groups': ['Coil_Out']
        },
        {
            'username': 'view4',
            'password': 'vpass4545',
            'groups': ['Viewer']
        }
    ]

    for config in users_config:
        username = config['username']
        password = config['password']
        group_names = config['groups']

        # proper get_or_create for user to avoid resetting password if exists, or update it?
        # Requirement implies setting them up. I'll update password to match requirement.
        try:
            user = User.objects.get(username=username)
            print(f"Updating User: {username}")
        except User.DoesNotExist:
            user = User(username=username)
            print(f"Creating User: {username}")
        
        user.set_password(password)
        if config.get('is_superuser'):
            user.is_superuser = True
            print(f"Set {username} as Superuser")
        else:
            user.is_superuser = False
            
        if config.get('is_staff'):
            user.is_staff = True
            print(f"Set {username} as Staff")
        else:
            user.is_staff = False

        user.is_active = True
        user.save()

        # Assign groups
        user.groups.clear()
        for g_name in group_names:
            if g_name in created_groups:
                user.groups.add(created_groups[g_name])
        
        print(f"Assigned groups to {username}: {group_names}")

if __name__ == '__main__':
    setup_rbac()
