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


class MyWindow(dpg.Window):
    primary = True

    def build(self, *args, **kwargs) -> Self:
        super().build(*args, **kwargs)

        def input_callback(sender, app_data: str, user_data):
            attr = self.editor.get_nodeattr_from_object(sender)
            attr.update_linked_object()

        def convert_input_callback(sender, app_data: str, user_data):
            node = self.editor.get_node_from_object(sender)
            out_attr: dpg.NodeAttribute = next(filter(lambda kv: isinstance(kv[1], dpg.NodeAttribute)
                                                      and kv[1].attribute_type == dpg.NodeAttributeType.OUTPUT, node))[1]
            in_attr: dpg.NodeAttribute = next(filter(lambda kv: isinstance(kv[1], dpg.NodeAttribute)
                                                     and kv[1].attribute_type == dpg.NodeAttributeType.INPUT, node))[1]
            values: list[str] = [cast(dpg.ValueObject, obj).value for _, obj in in_attr]
            out_attr.set_values(['.'.join(map(lambda s: s.replace('\n', '.'), values))])
            out_attr.update_linked_object()

        self.editor = dpg.NodeEditor()\
            .add(dpg.Node(pos=[0, 0])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.STATIC)
                      .add(dpg.Button(label='print node', callback=lambda: self.editor.print_node(logger.debug)))
                      .add(dpg.Button(label='print all', callback=lambda: self.editor.print_all(logger.debug)))
                      )
                 )\
            .add(dpg.Node(pos=[0, 100])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.OUTPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=input_callback))
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=input_callback))
                      )
                 )\
            .add(dpg.Node(pos=[0, 250])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.OUTPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=input_callback))
                      )
                 )\
            .add(dpg.Node(pos=[200, 100])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.INPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=convert_input_callback))
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=convert_input_callback))
                      )
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.OUTPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=input_callback))
                      )
                 )\
            .add(dpg.Node(pos=[200, 250])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.INPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=convert_input_callback))
                      )
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.OUTPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=input_callback))
                      .add(dpg.InputText(width=100, height=25, multiline=True, callback=input_callback))
                      )
                 )\
            .add(dpg.Node(pos=[400, 100])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.INPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True)))
                 )\
            .add(dpg.Node(pos=[400, 200])
                 .add(dpg.NodeAttribute(attribute_type=dpg.NodeAttributeType.INPUT)
                      .add(dpg.InputText(width=100, height=25, multiline=True)))
                 )\
            .build(self, *args, **kwargs)

        self.editor.print_node(logger.debug)
        return self


def main():
    dpg.ViewPort(title='Node Editor', width=800, height=400)\
        .add(MyWindow())\
        .build()


if __name__ == '__main__':
    main()
