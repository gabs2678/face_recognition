# Generated by Django 5.0.3 on 2024-03-13 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MissingPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('last_seen', models.DateTimeField()),
                ('image', models.ImageField(upload_to='missing_persons/')),
            ],
        ),
    ]
