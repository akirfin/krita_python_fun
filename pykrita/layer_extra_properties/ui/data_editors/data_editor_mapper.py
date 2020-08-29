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

from .abc_editor_container import AbcEditorContainer


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


    def __len__(self):
        return len(self._registry)


    def __iter__(self):
        for k_v in self._registry.items():
            yield k_v


    def register(self, data_type, editor_type):
        self._registry[data_type] = editor_type


    def create_editor(self, data, title=None):
        import layer_extra_properties.ui.data_editors.dict_editor as de
        import layer_extra_properties.ui.data_editors.list_editor as le

        data_type = type(data)
        editor_type = None

        if data_type in self._registry:
            editor_type = self._registry[data_type]
        elif issubclass(data_type, Mapping):
            # generic Mapping type
            editor_type = de.DictEditor
        elif issubclass(data_type, Iterable):
            # generic Iterable type
            editor_type = le.ListEditor

        if editor_type is not None:
            data_editor = editor_type()
            data_editor.data = data
            if title is not None:
                if isinstance(data_editor, AbcEditorContainer):
                    data_editor.title = title
                data_editor.setObjectName(title)
            return data_editor

        raise RuntimeError("Unable to create editor for {data!r}".format(**locals()))


data_editor_mapper = DataEditorMapper.instance()
