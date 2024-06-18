# Generated by Django 5.0.5 on 2024-06-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lion",
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
                ("no", models.TextField()),
                ("company_Name", models.TextField()),
                ("area", models.CharField(max_length=10)),
                ("title", models.TextField()),
                ("url", models.TextField()),
                ("trip_type", models.TextField()),
                ("fromDate", models.TextField()),
                ("trip_number", models.TextField()),
                ("group_total", models.TextField()),
                ("saleable", models.TextField()),
                ("after_saleable", models.TextField()),
                ("group_state", models.TextField()),
                ("traffic_information", models.TextField()),
                ("trip_information", models.TextField()),
                ("total_Date", models.IntegerField(null=True)),
                ("price", models.IntegerField()),
                ("hotel", models.TextField()),
            ],
            options={
                "db_table": "Lion",
            },
        ),
        migrations.CreateModel(
            name="Lion_save",
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
                ("no", models.TextField()),
                ("company_Name", models.TextField()),
                ("area", models.CharField(max_length=10)),
                ("title", models.TextField(blank=True, null=True)),
                ("url", models.TextField()),
                ("trip_type", models.TextField()),
                ("fromDate", models.TextField()),
                ("trip_number", models.TextField()),
                ("group_total", models.TextField()),
                ("saleable", models.TextField()),
                ("after_saleable", models.TextField()),
                ("group_state", models.TextField()),
                ("traffic_information", models.TextField()),
                ("trip_information", models.TextField()),
                ("total_Date", models.IntegerField(null=True)),
                ("price", models.IntegerField()),
                ("hotel", models.TextField()),
            ],
            options={
                "db_table": "Lion_save",
            },
        ),
        migrations.CreateModel(
            name="Trip",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("travel_company", models.TextField()),
                ("area", models.TextField()),
                ("title", models.TextField()),
                ("price", models.IntegerField(null=True)),
                ("date", models.TextField()),
                ("departure_city", models.TextField()),
                ("duration", models.IntegerField(null=True)),
                ("remaining_quota", models.TextField()),
                ("tour_schedule", models.TextField()),
                ("url", models.TextField()),
            ],
            options={
                "db_table": "Trip",
            },
        ),
    ]
