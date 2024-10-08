# Generated by Django 5.0.8 on 2024-08-11 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loans", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="taken_at",
            field=models.DateTimeField(
                blank=True, help_text="Date when the loan is activated", null=True
            ),
        ),
    ]
