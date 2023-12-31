# Generated by Django 4.2.4 on 2023-08-10 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retina', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='cf_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='cf_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='cws_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='cws_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='cws_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='he_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='he_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='he_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='ma_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='ma_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='ma_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='nvd_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='nvd_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='nvd_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='nve_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='nve_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='nve_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='rh_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='rh_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='rh_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='sh_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='sh_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='sh_y',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='vh_r',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='vh_x',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='vh_y',
        ),
        migrations.AddField(
            model_name='patient',
            name='url',
            field=models.CharField(default='', max_length=500),
        ),
    ]
