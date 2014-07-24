from django.core.serializers import python, register_serializer


class Serializer(python.Serializer):
    def start_object(self, obj):
        super(Serializer, self).start_object(obj)
        if hasattr(obj, '__public__'):
            # Little hack to prevent serializer from picking up fields we don't want
            self._selected_fields = self.selected_fields
            self.selected_fields = obj.__public__.keys()

    def end_object(self, obj):
        if hasattr(self, '_selected_fields'):
            self.selected_fields = self._selected_fields
            del self._selected_fields

        if hasattr(obj, '__public__'):
            current = self._current
            data = {}
            for attr, alias in obj.__public__.iteritems():
                if attr in current:
                    data[alias] = current[attr]
                elif hasattr(obj, attr):
                    attribute = getattr(obj, attr)
                    if callable(attribute):
                        data[alias] = attribute()
                    else:
                        data[alias] = attribute
            self._current = data

        super(Serializer, self).end_object(obj)

    def get_dump_object(self, obj):
        return self._current


register_serializer('public', 'mozbadges.utils.serializers.public')
