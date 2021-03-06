# Generated by Django 3.1 on 2020-08-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20200816_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursetheme',
            name='hours',
        ),
        migrations.RemoveField(
            model_name='coursetheme',
            name='theme_type',
        ),
        migrations.RemoveField(
            model_name='grouptheme',
            name='hours_left',
        ),
        migrations.AddField(
            model_name='coursetheme',
            name='p_hours',
            field=models.FloatField(default=0, verbose_name='Количество часов практики'),
        ),
        migrations.AddField(
            model_name='coursetheme',
            name='t_hours',
            field=models.FloatField(default=0, verbose_name='Количество часов теории'),
        ),
        migrations.AddField(
            model_name='grouptheme',
            name='p_hours_left',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='grouptheme',
            name='t_hours_left',
            field=models.FloatField(null=True),
        ),
    ]
