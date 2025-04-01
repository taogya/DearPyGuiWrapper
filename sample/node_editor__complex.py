import logging.config
from typing import Self, cast

import dearpygui_wrapper as dpg

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG'
    }

})

logger = logging.getLogger('dgp_wrapper')


class OutputNode(dpg.Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.OUTPUT)
                 .add(dpg.InputText(width=100, height=25, multiline=True, callback=self.callback))
                 )

    def callback(self, sender, app_data: str, user_data):
        editor: dpg.NodeEditor = self.parent
        attr = editor.get_nodeattr_from_object(sender)
        attr.update_linked_object()


class InputNode(dpg.Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.INPUT)
                 .add(dpg.InputText(width=100, height=25, multiline=True, readonly=True))
                 )


class ConvertermNode(dpg.Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.INPUT)
                 .add(dpg.InputText(width=100, height=25, multiline=True, callback=self.input_callback))
                 )
        self.add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.OUTPUT)
                 .add(dpg.InputText(width=100, height=25, multiline=True, callback=self.output_callback))
                 )

    def input_callback(self, sender, app_data: str, user_data):
        editor: dpg.NodeEditor = self.parent
        node = editor.get_node_from_object(sender)
        values: list[str] = [cast(dpg.ValueObject, obj).value
                             for attr in node.input_attrs
                             for _, obj in attr]
        for attr in node.output_attrs:
            attr\
                .set_values(['.'.join(map(lambda s: s.replace('\n', '.'), values))])\
                .update_linked_object()

    def output_callback(self, sender, app_data: str, user_data):
        editor: dpg.NodeEditor = self.parent
        attr = editor.get_nodeattr_from_object(sender)
        attr.update_linked_object()


class MyWindow(dpg.Window):
    primary = True

    def build(self, **kwargs) -> Self:
        super().build(**kwargs)

        self.editor = dpg.NodeEditor()\
            .add(dpg.Node(pos=[600, 0])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.STATIC)
                      .add(dpg.Button(label='print_objects', callback=lambda: self.editor.print_objects(logger.debug)))
                      .add(dpg.Button(label='print node', callback=lambda: self.editor.print_node(logger.debug)))
                      .add(dpg.Button(label='add output', callback=lambda: self.editor.add(OutputNode(pos=[0, 0])).build()))
                      .add(dpg.Button(label='add converter', callback=lambda: self.editor.add(ConvertermNode(pos=[0, 0])).build()))
                      .add(dpg.Button(label='add input', callback=lambda: self.editor.add(InputNode(pos=[0, 0])).build()))
                      )
                 )\
            .add(OutputNode(pos=[0, 0]))\
            .add(OutputNode(pos=[0, 150]))\
            .add(ConvertermNode(pos=[200, 0]))\
            .add(ConvertermNode(pos=[200, 150]))\
            .add(InputNode(pos=[400, 0]))\
            .add(InputNode(pos=[400, 100]))\
            .build(parent=self)

        return self


def main():
    dpg.ViewPort(title='Node Editor', width=800, height=400)\
        .add(MyWindow())\
        .build()


if __name__ == '__main__':
    main()
