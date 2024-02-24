# Generated by Django 4.1.7 on 2023-04-14 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Filters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sortby",
                    models.CharField(
                        choices=[
                            ("Relevance", "Relevance"),
                            ("Upload Date", "Upload Date"),
                        ],
                        max_length=24,
                    ),
                ),
                (
                    "features",
                    models.CharField(
                        choices=[
                            ("Live", "Live"),
                            ("Subtitles/CC", "Subtitles/CC"),
                            ("HD", "HD"),
                        ],
                        max_length=24,
                    ),
                ),
                (
                    "duration",
                    models.CharField(
                        choices=[
                            ("< 4min", "< 4min"),
                            ("4-20 min", "4-20 min"),
                            ("> 20min", "> 20min"),
                        ],
                        max_length=24,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("Video", "Video"),
                            ("Channel", "Channel"),
                            ("Playlist", "Playlist"),
                        ],
                        max_length=24,
                    ),
                ),
                (
                    "upload_date",
                    models.CharField(
                        choices=[
                            ("Last Hour", "Last Hour"),
                            ("Today", "Today"),
                            ("This Week", "This Week"),
                            ("This Month", "This Month"),
                            ("This Year", "This Year"),
                        ],
                        max_length=24,
                    ),
                ),
            ],
        ),
    ]