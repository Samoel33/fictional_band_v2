# Generated by Django 4.2.20 on 2025-04-25 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0008_bookings_description_bookings_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='event_image',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
        migrations.AlterField(
            model_name='upcomingevent',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]
