# Generated by Django 4.1 on 2023-05-21 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0009_remove_media_m_json_media_m_actor_media_m_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='u_texts',
            field=models.ManyToManyField(related_name='t_users', to='models.text'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='c_description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='group',
            name='g_description',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_actor',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_author',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_description',
            field=models.TextField(default='', max_length=65535),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_director',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_episode_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_genre',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_rate',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='media',
            name='m_region',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='report',
            name='r_text',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.DO_NOTHING, to='models.text'),
        ),
        migrations.AlterField(
            model_name='text',
            name='t_topic',
            field=models.CharField(default='', max_length=255),
        ),
    ]
