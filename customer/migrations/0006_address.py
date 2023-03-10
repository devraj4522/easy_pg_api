# Generated by Django 4.0.8 on 2023-01-01 13:34

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', shortuuid.django_fields.ShortUUIDField(alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ', editable=False, length=8, max_length=8, prefix='', primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=6)),
                ('locality', models.CharField(blank=True, max_length=200, null=True)),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='customer.hostel')),
            ],
            options={
                'db_table': 'addresses',
            },
        ),
    ]
