# Generated by Django 4.2.4 on 2024-05-02 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0006_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]