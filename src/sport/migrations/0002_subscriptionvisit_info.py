# Generated by Django 4.1.2 on 2023-02-23 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sport", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscriptionvisit",
            name="info",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Комментарий"
            ),
        ),
    ]