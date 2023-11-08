# your_app/search_indexes.py

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.connections import connections

from .models import Employee


@registry.register_document
class EmployeeDocument(Document):
    class Index:
        name = 'employee'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    id = fields.IntegerField(attr='id')
    user = fields.ObjectField(properties={
        'username': fields.KeywordField(),
        'first_name': fields.KeywordField(),
        'last_name': fields.KeywordField()
    })
    department = fields.KeywordField()
    city = fields.KeywordField()
    phone_number = fields.ObjectField(properties={
        'national_number': fields.KeywordField()
    })
    address = fields.KeywordField()
    technologies_familiar_with = fields.ObjectField(properties={
        'name': fields.KeywordField()
    })   

    class Django:
        model = Employee
