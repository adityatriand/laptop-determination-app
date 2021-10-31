# Generated by Django 3.2.8 on 2021-10-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Laptops',
            fields=[
                ('id_laptop', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(blank=True, max_length=9, null=True)),
                ('product', models.CharField(blank=True, max_length=45, null=True)),
                ('cpu', models.FloatField(blank=True, null=True)),
                ('ram', models.FloatField(blank=True, null=True)),
                ('harga', models.IntegerField(blank=True, null=True)),
                ('hdd', models.FloatField(blank=True, null=True)),
                ('ssd', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'laptops',
                'managed': False,
            },
        ),
    ]