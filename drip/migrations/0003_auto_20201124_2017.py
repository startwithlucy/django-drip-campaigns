# Generated by Django 3.0.7 on 2020-11-24 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drip', '0002_querysetrule_rule_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='querysetrule',
            name='rule_type',
            field=models.CharField(choices=[('or', 'Or'), ('and', 'And')], default='and', max_length=3),
        ),
    ]