# Generated by Django 4.2.4 on 2023-09-01 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("fruit", "0004_fruitimg_fruittable"),
    ]

    operations = [
        migrations.AddField(
            model_name="fruitsugar",
            name="fruittable",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="fruit.fruittable",
            ),
        ),
    ]