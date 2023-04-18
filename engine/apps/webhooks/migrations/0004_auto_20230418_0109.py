# Generated by Django 3.2.18 on 2023-04-18 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0003_auto_20230412_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webhook',
            name='trigger_type',
            field=models.IntegerField(choices=[(0, 'Escalation step'), (1, 'Firing'), (2, 'Acknowledged'), (3, 'Resolved'), (4, 'Silenced'), (5, 'Unsilenced'), (6, 'Unresolved'), (7, 'Unacknowledged')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='webhookresponse',
            name='trigger_type',
            field=models.IntegerField(choices=[(0, 'Escalation step'), (1, 'Firing'), (2, 'Acknowledged'), (3, 'Resolved'), (4, 'Silenced'), (5, 'Unsilenced'), (6, 'Unresolved'), (7, 'Unacknowledged')]),
        ),
    ]
