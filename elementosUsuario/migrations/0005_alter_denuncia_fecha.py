# Generated by Django 5.1.3 on 2024-11-10 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elementosUsuario', '0004_denuncia_ciudad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denuncia',
            name='fecha',
            field=models.DateField(default=None),
        ),
    ]
