from django.core.exceptions import FieldError, FullResultSet
from django.db.models.sql.compiler import (  # noqa
    SQLCompiler,
    SQLDeleteCompiler,
    SQLInsertCompiler,
    SQLUpdateCompiler as BaseUpdateCompiler,
    SQLAggregateCompiler
)


def no_quote_name(name):
    return name

class SQLUpdateCompiler(BaseUpdateCompiler):
    def as_sql(self):
        """
        Creates the SQL for this query. Returns the SQL string and list of
        parameters.
        """
        self.pre_sql_setup()
        if not self.query.values:
            return '', ()
        table = self.query.base_table
        qn = self.quote_name_unless_alias
        result = ['UPDATE %s SET' % qn(table)]
        values, update_params = [], []
        for field, model, val in self.query.values:
            field_qn = qn
            name = field.column
            if hasattr(val, 'alter_name'):
                name = val.alter_name(name, field_qn)
                field_qn = no_quote_name
                val = val.value
            if hasattr(val, 'resolve_expression'):
                val = val.resolve_expression(
                    self.query, allow_joins=False, for_save=True
                )
                if val.contains_aggregate:
                    raise FieldError(
                        "Aggregate functions are not allowed in this query "
                        "(%s=%r)." % (field.name, val)
                    )
                if val.contains_over_clause:
                    raise FieldError(
                        "Window expressions are not allowed in this query "
                        "(%s=%r)." % (field.name, val)
                    )
            elif hasattr(val, 'prepare_database_save'):
                if field.remote_field:
                    val = val.prepare_database_save(field)
                else:
                    raise TypeError(
                        "Tried to update field %s with a model instance, %r. "
                        "Use a value compatible with %s."
                        % (field, val, field.__class__.__name__)
                    )
            val = field.get_db_prep_save(val, connection=self.connection)

            # Getting the placeholder for the field.
            if hasattr(field, 'get_placeholder'):
                placeholder = field.get_placeholder(val, self, self.connection)
            else:
                placeholder = '%s'
            if hasattr(val, 'as_sql'):
                    sql, params = self.compile(val)
                    values.append('%s = %s' % (field_qn(name), placeholder % sql))
                    update_params.extend(params)
            elif val is not None:
                values.append('%s = %s' % (field_qn(name), placeholder))
                update_params.append(val)
            else:
                values.append('%s = NULL' % field_qn(name))
        if not values:
            return '', ()
        result.append(', '.join(values))
        try:
            where, params = self.compile(self.query.where)
        except FullResultSet:
            params = []
        else:
            result.append("WHERE %s" % where)
        return ' '.join(result), tuple(update_params + params)