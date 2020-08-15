# Generated by Django 3.1 on 2020-08-15 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='possible_courses',
            field=models.ManyToManyField(to='main.Course', verbose_name='Подходит для программ'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='students_type',
            field=models.BooleanField(choices=[(False, 'Неавиационный персонал'), (True, 'Авиационный персонал')], null=True, verbose_name='Тип'),
        ),
    ]
