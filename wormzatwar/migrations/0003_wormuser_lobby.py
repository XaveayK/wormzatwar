# Generated by Django 4.1.4 on 2023-02-03 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wormzatwar', '0002_lobby'),
    ]

    operations = [
        migrations.AddField(
            model_name='wormuser',
            name='lobby',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wormGenerals', to='wormzatwar.lobby'),
        ),
    ]
