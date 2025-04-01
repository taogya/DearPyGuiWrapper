import logging.config
from typing import Self

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
                 .add(dpg.InputText(width=100, height=25, multiline=True, callback=self.input_callback))
                 )

    def input_callback(self, sender, app_data: str, user_data):
        editor: dpg.NodeEditor = self.parent
        attr = editor.get_nodeattr_from_object(sender)
        attr.update_linked_object()


class InputNode(dpg.Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.INPUT)
                 .add(dpg.InputText(width=100, height=25, multiline=True, readonly=True))
                 )


class MyWindow(dpg.Window):
    primary = True

    def build(self, **kwargs) -> Self:
        super().build(**kwargs)

        def input_callback(sender, app_data: str, user_data):
            attr = self.editor.get_nodeattr_from_object(sender)
            attr.update_linked_object()

        self.editor = dpg.NodeEditor()\
            .add(dpg.Node(pos=[0, 0])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.STATIC)
                      .add(dpg.Button(label='print_objects', callback=lambda: self.editor.print_objects(logger.debug)))
                      .add(dpg.Button(label='print node', callback=lambda: self.editor.print_node(logger.debug)))
                      .add(dpg.Button(label='add output', callback=lambda: self.editor.add(OutputNode(pos=[0, 0])).build()))
                      .add(dpg.Button(label='add input', callback=lambda: self.editor.add(InputNode(pos=[0, 0])).build()))
                      )
                 )\
            .add(OutputNode(pos=[0, 100]))\
            .add(InputNode(pos=[200, 100]))\
            .build(parent=self)

        self.editor.print_node(logger.debug)
        return self


def main():
    dpg.ViewPort(title='Node Editor', width=800, height=400)\
        .add(MyWindow())\
        .build()


if __name__ == '__main__':
    main()
