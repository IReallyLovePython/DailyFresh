# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('status', models.SmallIntegerField(default=1, choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], verbose_name='订单状态')),
            ],
            options={
                'verbose_name': '测试模型',
                'db_table': 'df_test',
                'verbose_name_plural': '测试模型',
            },
        ),
    ]
