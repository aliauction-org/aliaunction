from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = 'qa_admin'
email = 'qa_admin@example.com'
password = 'qa_password123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")
