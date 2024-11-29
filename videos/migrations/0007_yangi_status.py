# Generated by Django 5.1.1 on 2024-11-11 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_yangi'),
    ]

    operations = [
        migrations.AddField(
            model_name='yangi',
            name='status',
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='DF', max_length=2),
        ),
    ]