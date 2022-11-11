# Generated by Django 4.0.5 on 2022-10-24 14:29

from django.apps.registry import Apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor

from ..models import Chain


def create_support_group(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    support_group, created = Group.objects.get_or_create(name="support")

    ct = ContentType.objects.get_for_model(Chain)
    warning_perm, created = Permission.objects.get_or_create(
        codename="change_only_warning", name="Can change only warning", content_type=ct
    )
    chain_perm, created = Permission.objects.get_or_create(
        codename="change_chain", name="Can change chain", content_type=ct
    )

    support_group.permissions.add(chain_perm)
    support_group.permissions.add(warning_perm.id)


class Migration(migrations.Migration):

    dependencies = [
        ("chains", "0036_alter_chain_transaction_service_uri_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chain",
            name="warning",
            field=models.TextField(blank=True, max_length=511, null=True),
        ),
        migrations.AlterModelOptions(
            name="chain",
            options={
                "permissions": [("change_only_warning", "Can change only warning")]
            },
        ),
        migrations.RunPython(create_support_group, migrations.RunPython.noop),
    ]
