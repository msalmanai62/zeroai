# Generated by Django 4.2.10 on 2024-02-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('ai', models.CharField(max_length=10)),
                ('hu', models.CharField(max_length=10)),
            ],
        ),
    ]
