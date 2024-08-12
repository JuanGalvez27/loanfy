# Generated by Django 5.0.8 on 2024-08-11 22:23

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="Customer ID",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "external_id",
                    models.CharField(
                        help_text="External Customer ID", max_length=60, unique=True
                    ),
                ),
                (
                    "status",
                    models.SmallIntegerField(
                        choices=[(1, "Active"), (2, "Inactive")],
                        default=1,
                        help_text="Status of the customer",
                    ),
                ),
                (
                    "score",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Amount that can be used to apply for loans",
                        max_digits=12,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
