# Generated by Django 2.2.3 on 2019-07-16 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]