# Generated by Django 3.0.7 on 2020-06-13 14:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


def set_frisbeer_rules(apps, schema_editor):
    GameRules = apps.get_model('frisbeer', 'GameRules')

    frisbeer_rules = GameRules(name='Frisbeer',
                               min_players=6,
                               max_players=6,
                               min_rounds=2,
                               max_rounds=3)
    frisbeer_rules.save()

    Season = apps.get_model('frisbeer', 'Season')
    Game = apps.get_model('frisbeer', 'Game')

    Season.objects.filter(game_rules__isnull=True).update(game_rules=frisbeer_rules)
    Game.objects.filter(rules__isnull=True).update(rules=frisbeer_rules)


def unset_rules(apps, schem_editor):
    Season = apps.get_model('frisbeer', 'Season')
    Game = apps.get_model('frisbeer', 'Game')

    Season.objects.all().update(game_rules=None)
    Game.objects.all().update(rules=None)


class Migration(migrations.Migration):

    dependencies = [
        ('frisbeer', '0031_auto_20190630_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('min_players', models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('max_players', models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('min_rounds', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(0)])),
                ('max_rounds', models.IntegerField(default=3, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frisbeer.Location'),
        ),
        migrations.AlterField(
            model_name='game',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frisbeer.Season'),
        ),
        migrations.AddField(
            model_name='game',
            name='rules',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frisbeer.GameRules'),
        ),
        migrations.AddField(
            model_name='season',
            name='game_rules',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frisbeer.GameRules'),
        ),
        migrations.RunPython(
            set_frisbeer_rules,
            unset_rules
        )
    ]
