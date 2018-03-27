import json
from django.db.models import Transform
from django.db.models.lookups import Lookup
from django.utils import six

from jsonfield import JSONField as OriginalJSONField


class JSONField(OriginalJSONField):
    """
    This overrides the json field in the django-jsonfield project to add transforms and custom lookups which don't have
    an implementation in that project.
    """
    def get_transform(self, name):
        transform = super(JSONField, self).get_transform(name)
        if transform:
            return transform

        # if no transform is defined, assume it is a JSON key lookup ex: obj__field1__lookup='foo'
        return KeyTransformFactory(name)


class JSONHasKey(Lookup):
    """
    A mysql 5.6 implementation for the has_key operator substituting the native operator with an INSTR function call.
    This basically looks for the key name's existence as a substring in the text blob json field.
    """
    lookup_name = 'has_key'

    def get_prep_lookup(self):
        if not isinstance(self.rhs, six.text_type):
            raise ValueError(
                "JSONField's 'has_key' lookup only works with {} values"
                .format(six.text_type.__name__)
            )
        return super(JSONHasKey, self).get_prep_lookup()

    def as_sql(self, qn, connection):
        # the lhs looks like jsonfield__has_key='keyname'
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)

        # we're only interested in a single key name
        key_name = rhs % rhs_params[0]
        # key would usually be of the form "key": so look strictly for that
        # the key_name here already contains quotes so just append the colon
        return "INSTR({}, CONCAT(%s, \":\")) != 0".format(lhs), [key_name]


class JSONExactLookup(Lookup):
    """
    A mysql 5.6 implementation of an exact JSON field lookup using the INSTR function call.
    The filter would look like jsonfield__key=value. Note that this simply looks for the existence of the
    value, not of the field and value, opting to use the pattern : <value>.
    """
    lookup_name = 'exact'

    def as_sql(self, compiler, connection):
        json_field_alias, json_field_params = self.lhs.lhs.as_sql(compiler, connection)

        return "(INSTR({}, CONCAT(\": \" , %s)) != 0)".format(json_field_alias), [self.rhs]


class JSONContainsLookup(Lookup):
    """
    A mysql 5.6 implementation of a contains JSON field lookup using the like function call.
    The filter would look like jsonfield__contains=value. Note that this implementation tries to
    determine if both the field and the value exist but doesn't correlate them.
    """
    lookup_name = 'contains'

    def as_sql(self, compiler, connection):

        lhs, lparams = self.process_lhs(compiler, connection)
        key_transform = lhs % lparams
        rhs, rparams = self.process_rhs(compiler, connection)
        value_lookup = rhs % rparams[0]

        json_field_alias, json_field_params = self.lhs.lhs.as_sql(compiler, connection)

        # field contains key && field contains value
        return "({0} AND (INSTR({1}, %s) != 0))".format(key_transform, json_field_alias), [value_lookup.strip("\"")]


JSONField.register_lookup(JSONHasKey)
JSONField.register_lookup(JSONExactLookup)
JSONField.register_lookup(JSONContainsLookup)


class KeyTransform(Transform):
    """
    A mysql 5.6 implementation of key transforms using the INSTR function. The transform would usually be in the
    form obj__field1__lookup='foo' where field1 is the transform representing a key lookup in the JSON object, followed
    by one of the usual lookup operators.
    Note that this implementation doesn't support nested key lookups so can only do a 1 level deep lookup.
    """

    def __init__(self, key_name, *args, **kwargs):
        self.key_name = key_name
        super(KeyTransform, self).__init__(*args, **kwargs)

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)

        # the lookup for a transform in this case would be the key
        lookup = self.key_name

        return "(INSTR(%s, CONCAT('%s', \"\\\":\")) != 0)", (lhs, lookup)


class KeyTransformFactory(object):

    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, *args, **kwargs):
        return KeyTransform(self.key_name, *args, **kwargs)
