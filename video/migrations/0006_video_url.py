# Generated by Django 4.2.4 on 2024-05-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_video_public_or_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
