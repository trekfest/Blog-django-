# Generated by Django 4.2.4 on 2024-02-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0012_category_article_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
