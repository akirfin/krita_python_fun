"""

Maps data_types to editors
by default JSON objects are supported, register more data types if needed.

Notes:
    - int / float separation
    - bytes special case.

"""

from collections import OrderedDict as oDict
try:
    from collections.abc import Mapping, Iterable
except:
    from collections import Mapping, Iterable

from .section import Section
# from .dict_editor import DictEditor
# from .list_editor import ListEditor


class DataEditorMapper(object):
    """
    Mapping of data_object to data_editor
    """
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance


    def __init__(self):
        self._registry = oDict()


    def register(self, data_type, data_editor_type):
        self._registry[data_type] = data_editor_type


    def create_editor(self, data, title=None):
        import layer_extra_properties.ui.data_editors.dict_editor as de
        import layer_extra_properties.ui.data_editors.list_editor as le

        data_type = type(data)
        data_editor_type = None

        if data_type in self._registry:
            data_editor_type = self._registry[data_type]
        elif issubclass(data_type, Mapping):
            # generic Mapping type
            data_editor_type = de.DictEditor
        elif issubclass(data_type, Iterable):
            # generic Iterable type
            data_editor_type = le.ListEditor

        if data_editor_type is not None:
            data_editor = data_editor_type()
            data_editor.data = data
            if title is not None:
                if isinstance(data_editor, Section):
                    data_editor.title = title
                data_editor.setObjectName(title)
            return data_editor

        raise RuntimeError("Unable to create editor for {data!r}".format(**locals()))


data_editor_mapper = DataEditorMapper.instance()
