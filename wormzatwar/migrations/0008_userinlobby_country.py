# Generated by Django 4.1.4 on 2023-02-13 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wormzatwar', '0007_lobby_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='userInLobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(choices=[('1', 'Red'), ('2', 'Blue'), ('3', 'Green')], max_length=10)),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wormzatwar.lobby')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gucci', models.IntegerField()),
                ('food', models.IntegerField()),
                ('occupyingForce', models.IntegerField()),
                ('troopGen', models.IntegerField()),
                ('lobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wormzatwar.lobby')),
                ('occupier', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
