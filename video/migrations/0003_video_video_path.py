# Generated by Django 4.2 on 2023-08-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_remove_video_video_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_path',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
