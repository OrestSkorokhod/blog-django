# Generated by Django 2.1.5 on 2019-03-01 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190218_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=models.TextField(db_index=True, max_length=1000),
        ),
    ]