# Generated by Django 4.0.4 on 2022-05-16 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_alter_invitation_id_alter_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='team_to_user',
            field=models.CharField(max_length=30),
        ),
    ]
