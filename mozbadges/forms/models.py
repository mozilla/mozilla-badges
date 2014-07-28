from itertools import groupby

from django.forms.models import ModelChoiceIterator, ModelChoiceField


class GroupedModelChoiceField(ModelChoiceField):

    def __init__(self, queryset, group_by, group_label=None, *args, **kwargs):
        """
        group_by is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(queryset, *args, **kwargs)
        self.group_by = group_by

        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)

    choices = property(_get_choices, ModelChoiceField._set_choices)


class GroupedModelChoiceIterator(ModelChoiceIterator):

    def _get_row_grouping(self, row, group_by):
        group_by = self.field.group_by
        value = getattr(row, group_by)

        if value is None or not hasattr(row, 'get_%s_display' % group_by):
            return value

        if not value:
            return None

        display = getattr(row, 'get_%s_display' % group_by)
        return display()

    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (self.field.group_label(group), [
                     self.choice(ch) for ch in choices])
                    for group, choices in groupby(
                        self.queryset.all(),
                        key=lambda row: self._get_row_grouping(row, self.field.group_by))
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for group, choices in groupby(
                    self.queryset.all(),
                    key=lambda row: self._get_row_grouping(row, self.field.group_by)):
                if group is None:
                    for ch in choices:
                        yield self.choice(ch)
                else:
                    yield (
                        self.field.group_label(group),
                        [self.choice(ch) for ch in choices])
