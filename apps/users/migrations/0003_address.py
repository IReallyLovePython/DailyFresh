# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_delete_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
                ('delete', models.BooleanField(verbose_name='是否删除', default=False)),
                ('receiver_name', models.CharField(verbose_name='收件人', max_length=20)),
                ('receiver_mobile', models.CharField(verbose_name='联系电话', max_length=11)),
                ('detail_addr', models.CharField(verbose_name='详细地址', max_length=256)),
                ('zip_code', models.CharField(verbose_name='邮政编码', max_length=6, null=True)),
                ('is_default', models.BooleanField(verbose_name='默认地址', default=False)),
                ('user', models.ForeignKey(verbose_name='所属用户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'df_address',
            },
        ),
    ]
