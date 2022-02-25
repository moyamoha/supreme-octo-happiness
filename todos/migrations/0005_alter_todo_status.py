# Generated by Django 4.0.2 on 2022-02-25 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0004_rename_user_todo_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('NotStarted', 'NotStarted'), ('OnGoing', 'OnGoing'), ('Completed', 'Completed')], default='NotStarted', max_length=20),
        ),
    ]
