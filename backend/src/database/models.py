from tortoise import fields, models


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=100, null=True)
    is_admin = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class DataSets(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    directory_path = fields.CharField(max_length=255)
    user = fields.ForeignKeyField("models.Users", related_name="user_datasets")
    sample_count = fields.IntField()
    metadata = fields.JSONField(null=True)
    parent = fields.ForeignKeyField("models.DataSets", related_name="children", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Images(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    file_path = fields.CharField(max_length=255, unique=True)
    metadata = fields.JSONField(null=True)
    dataset = fields.ForeignKeyField("models.DataSets", related_name="dataset_images")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Models(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    user = fields.ForeignKeyField("models.Users", related_name="user_models")
    parent = fields.ForeignKeyField("models.Models", related_name="children", null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Trainings(models.Model):
    id = fields.IntField(pk=True)
    experiment_name = fields.CharField(max_length=255, unique=True)
    model = fields.ForeignKeyField("models.Models", related_name="model_trainings")
    dataset = fields.ForeignKeyField("models.DataSets", related_name="dataset_trainings")
    precision = fields.FloatField()
    recall = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
