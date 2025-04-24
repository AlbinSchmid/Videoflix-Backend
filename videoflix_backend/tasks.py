from django.utils.timezone import now
import os
    

def backup_database():
    timestamp = now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)
    filepath = os.path.join(backup_dir, f'backup_{timestamp}.json')
    os.system(f'python manage.py dumpdata --natural-foreign --natural-primary --exclude auth.permission --exclude contenttypes > {filepath}')
    print(f'[✓] Backup saved to {filepath}')