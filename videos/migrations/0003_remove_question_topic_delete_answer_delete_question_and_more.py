# Generated by Django 5.1.1 on 2024-11-06 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_question_topic_answer_question_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='topic',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]