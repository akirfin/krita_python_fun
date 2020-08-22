

Access = namedtuple("Access", (
        "attribute_getter,"
        "attribute_setter,"
        "attribute_changed,"
        "field_getter,"
        "field_setter,"
        "field_changed"))


class AttributeWidgetMapper(QObject):
    def __init__(self, parent=None):
        super(AttributeWidgetMapper, self).__init__(parent=parent)
        self.setObjectName("attribute_widget_mapper")
        self._lock = False
        self._mapping = list()


    def clear(self):
        while self._mappings:
            access, partial_attribute, partial_field = self._mappings.pop()
            access.attribute_changed.disconnect(partial_attribute)
            access.field_changed.disconnect(partial_field)


    def add(self, access):
        partial_attribute = partial(
                self.on_change,
                getter=access.field_getter,
                setter=access.attribute_setter)
        partial_field = partial(
                self.on_change,
                getter=access.attribute_getter,
                setter=access.field_setter)
        access.attribute_changed.connect(partial_attribute)
        access.field_changed.connect(partial_field)
        self._mapping.append((access, partial_attribute, partial_field))


    def on_change(self, getter, setter):
        if not self._lock:
            self._lock = True
            try:
                setter(getter())
            finally:
                self._lock = False


class LayerPropertiesTemplate(QWidget):
    def __init__(self, parent=None):
        super(LayerAttributesEditor, self).__init__(parent=parent)
        self.setObjectName("layer_attributes_editor")
        self._node = None
        self._mapper = AttributeWidgetMapper()
        self.create_ui()


    def create_ui(self):
        pass

    def get_node(self):
        return self._node

    @Slot(Node)
    def set_node(self, new_node):
        old_node = self.get_node()
        if new_node != old_node:
            self._mapper.clear()
            self._node = new_node
            self.build_mapping()
            self.node_changed.emit(self.get_node())


    def build_mapping(self):
        node = self._node
        mapper = self._mapper

        mapper.add(Access(
                node.name, node.setName, node.nameChanged,
                self._name.text, self._name.setText, self._name.textChanged))
        mapper.add(Access(
                node.colorLabel, node.setColorLabel, node.colorLabelChanged,
                self._color_label.color, self._color_label.setColor, self._color_label.colorChanged))
        mapper.add(Access(
                node.opacity, node.setOpacity, node.opacityChanged,
                self._opacity.value, self._opacity.setValue, self._opacity.valueChanged))
        mapper.add(Access(
                node.blendMode, node.setBlendMode, node.blendModeChanged,
                self._blend_mode.value, self._blend_mode.setValue, self._blend_mode.valueChanged))

        mapper.add_mapping(self._locked, partial(node.setLocked))
        mapper.add_mapping(self._visible, partial(node.setVisible))
        mapper.add_mapping(self._inherit_alpha, partial(node.setInheritAlpha))
        mapper.add_mapping(self._alpha_lock, partial(node.setAlphaLock))

        mapper.add_mapping(self._red, partial(node.setActiveChannelRed))
        mapper.add_mapping(self._green, partial(node.setActiveChannelGreen))
        mapper.add_mapping(self._blue, partial(node.setActiveChannelBlue))
        mapper.add_mapping(self._alpha, partial(node.setActiveChannelAplha))
