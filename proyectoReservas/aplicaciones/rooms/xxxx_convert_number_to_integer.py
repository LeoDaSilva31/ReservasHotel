from django.db import migrations

def convert_number_to_int(apps, schema_editor):
    Room = apps.get_model('rooms', 'Room')
    for room in Room.objects.all():
        try:
            room.number = int(room.number)
            room.save()
        except ValueError:
            print(f"Error converting room number: {room.number}")

class Migration(migrations.Migration):

    dependencies = [
        ('rooms', 'previous_migration'),
    ]

    operations = [
        migrations.RunPython(convert_number_to_int),
    ]