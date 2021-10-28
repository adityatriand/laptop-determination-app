# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Laptops(models.Model):
    id_laptop = models.AutoField(primary_key=True)
    company = models.CharField(max_length=9, blank=True, null=True)
    product = models.CharField(max_length=45, blank=True, null=True)
    cpu = models.FloatField(blank=True, null=True)
    ram = models.FloatField(blank=True, null=True)
    harga = models.IntegerField(blank=True, null=True)
    hdd = models.FloatField(blank=True, null=True)
    ssd = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'laptops'