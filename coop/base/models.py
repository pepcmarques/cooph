from django.db import models


class Cooperative(models.Model):
    cooperative_name = models.CharField(max_length=60, unique=True, null=False)

    class Meta:
        ordering = ['cooperative_name']

    def set_cooperative_name(self, name):
        self.cooperative_name = name

    def __str__(self):
        return self.cooperative_name


class Unit(models.Model):
    unit_number = models.CharField(max_length=5, unique=False)
    cooperative_id = models.ForeignKey(Cooperative, on_delete=models.CASCADE, related_name='cooperative_id')

    class Meta:
        ordering = ['cooperative_id', 'unit_number']

    def __str__(self):
        return self.unit_number
