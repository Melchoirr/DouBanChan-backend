# Generated by Django 4.1 on 2023-06-07 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("models", "0014_alter_user_u_authority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="m_description",
            field=models.TextField(default=""),
        ),
    ]