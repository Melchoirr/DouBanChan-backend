# Generated by Django 4.1 on 2023-06-07 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "0010_alter_chat_c_father_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="p_tag",
            field=models.CharField(default="", max_length=255),
        ),
    ]
