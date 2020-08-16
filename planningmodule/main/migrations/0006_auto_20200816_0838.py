# Generated by Django 3.1 on 2020-08-16 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200816_0052'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество человек в группе')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course', verbose_name='Учебная программа')),
            ],
            options={
                'verbose_name': 'Группа',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.AlterField(
            model_name='coursetheme',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.course', verbose_name='Учебная программа'),
        ),
        migrations.AlterField(
            model_name='coursetheme',
            name='hours',
            field=models.FloatField(verbose_name='Количество часов'),
        ),
        migrations.AlterField(
            model_name='coursetheme',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.theme', verbose_name='Тема'),
        ),
        migrations.AlterField(
            model_name='day',
            name='shifts',
            field=models.BinaryField(editable=True, max_length=4, verbose_name='Смены'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='courses',
            field=models.ManyToManyField(to='main.Course', verbose_name='Учебные дисциплины'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='shifts',
            field=models.BinaryField(blank=True, editable=True, max_length=4, null=True, verbose_name='В какие смены может работать (для сменного графика)'),
        ),
        migrations.CreateModel(
            name='GroupTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours_left', models.FloatField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.group')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.theme')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.group', verbose_name='Группа'),
        ),
    ]
