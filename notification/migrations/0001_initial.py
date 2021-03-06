# Generated by Django 3.0.6 on 2021-05-24 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('INDIVIDUAL', 'INDIVIDUAL'), ('ENTITY', 'ENTITY')], max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('message', models.TextField()),
                ('extra_id', models.CharField(blank=True, max_length=20, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-create_date'],
            },
        ),
    ]
