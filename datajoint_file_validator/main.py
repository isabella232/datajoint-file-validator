import yaml
from cerberus import schema_registry
from cerberus import rules_set_registry


def _example_registry_add():
    schema_registry.add('non-system user',
                        {'uid': {'min': 1000, 'max': 0xffff}})
    schema = {'sender': {'schema': 'non-system user',
                        'allow_unknown': True},
            'receiver': {'schema': 'non-system user',
                        'allow_unknown': True}}
    rules_set_registry.extend((('boolean', {'type': 'boolean'}),
                            ('booleans', {'valuesrules': 'boolean'})))
    schema = {'foo': 'booleans'}


def _example_schema_from_yaml():
    schema_text = '''
    name:
      type: string
    age:
      type: integer
      min: 10
    '''
    schema = yaml.safe_load(schema_text)
    document = {'name': 'Little Joe', 'age': 5}
    v.validate(document, schema)
    # False
    v.errors
    # {'age': ['min value is 10']}