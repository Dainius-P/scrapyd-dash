# Generated by Django 2.2.2 on 2019-07-02 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapyd_dash', '0007_auto_20190702_1257'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-create_datetime']},
        ),
        migrations.AlterField(
            model_name='task',
            name='finished_datetime',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_datetime',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]