# Generated by Django 4.2.4 on 2024-02-16 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0010_alter_article_pub_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile", name="bio", field=models.TextField(blank=True),
        ),
    ]
