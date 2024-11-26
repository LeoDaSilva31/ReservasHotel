# Generated by Django 5.1.3 on 2024-11-18 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tipo de Habitación')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('capacity', models.IntegerField(verbose_name='Capacidad')),
            ],
            options={
                'verbose_name': 'Tipo de Habitación',
                'verbose_name_plural': 'Tipos de Habitaciones',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, unique=True, verbose_name='Número')),
                ('floor', models.IntegerField(verbose_name='Piso')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activa')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notas')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creada')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Actualizada')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rooms.roomtype', verbose_name='Tipo de Habitación')),
            ],
            options={
                'verbose_name': 'Habitación',
                'verbose_name_plural': 'Habitaciones',
                'ordering': ['number'],
            },
        ),
    ]
