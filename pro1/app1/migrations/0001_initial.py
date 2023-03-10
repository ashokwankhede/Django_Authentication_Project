# Generated by Django 4.1.4 on 2022-12-29 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employees",
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
                ("Uname", models.CharField(max_length=50)),
                ("Name", models.CharField(max_length=50)),
                ("Gender", models.CharField(max_length=50)),
                ("DOB", models.DateField()),
                ("Email", models.EmailField(max_length=254, unique=True)),
                ("Mobileno", models.CharField(max_length=10)),
                ("Dept", models.CharField(max_length=20)),
                ("Password", models.CharField(max_length=20)),
            ],
        ),
    ]
