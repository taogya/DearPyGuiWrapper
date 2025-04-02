import logging
from enum import IntEnum
from typing import Any, Callable, Iterator, Self, cast

from dearpygui_wrapper import (Container, DpgTag, Object, ValueObject, dpg_org,
                               get_tag)

logger = logging.getLogger('dgp_wrapper')


class NodeAttributeType(IntEnum):
    STATIC = dpg_org.mvNode_Attr_Static
    INPUT = dpg_org.mvNode_Attr_Input
    OUTPUT = dpg_org.mvNode_Attr_Output


class NodeAttribute(Container):
    is_instance = False
    generator = staticmethod(dpg_org.add_node_attribute)
    attribute_type: NodeAttributeType

    def __init__(self, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, indent: int = -1, parent: DpgTag = 0, before: DpgTag = 0, show: bool = True, filter_key: str = '', tracked: bool = False, track_offset: float = 0.5, shape: int = 1, category: str = 'general'):
        """	 Adds a node attribute to a node.

        Args:
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            indent (int, optional): Offsets the widget to the right the specified number multiplied by the indent style.
            parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
            before (Union[int, str], optional): This item will be displayed before the specified item in the parent.
            show (bool, optional): Attempt to render widget.
            filter_key (str, optional): Used by filter widget.
            tracked (bool, optional): Scroll tracking
            track_offset (float, optional): 0.0f:top, 0.5f:center, 1.0f:bottom
            shape (int, optional): Pin shape.
            category (str, optional): Category
            id (Union[int, str], optional): (deprecated)
        """
        self.attribute_type = self.attribute_type
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'indent': indent, 'parent': parent, 'before': before, 'show': show, 'filter_key': filter_key, 'tracked': tracked, 'track_offset': track_offset, 'attribute_type': self.attribute_type, 'shape': shape, 'category': category}
        super().__init__(**kwargs)

    def default_tag(self) -> DpgTag:
        return f'{self.__class__.__name__}({self.attribute_type.name})##{self.id}'

    def set_values(self, objects: list[Object], call_callback: bool = True) -> Self:
        raise NotImplementedError('set_values() not implemented')

    @property
    def node(self) -> 'Node':
        """ Get node of the attribute.

        Raises:
            ValueError: If the attribute has no node.

        Returns:
            Node: node of the attribute.
        """
        return self.parent


class LinkableNodeAttribute(NodeAttribute):

    def __init__(self, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, indent: int = -1, parent: DpgTag = 0, before: DpgTag = 0, show: bool = True, filter_key: str = '', tracked: bool = False, track_offset: float = 0.5, shape: int = 1, category: str = 'general'):
        """	 Adds a node attribute to a node.

        Args:
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            indent (int, optional): Offsets the widget to the right the specified number multiplied by the indent style.
            parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
            before (Union[int, str], optional): This item will be displayed before the specified item in the parent.
            show (bool, optional): Attempt to render widget.
            filter_key (str, optional): Used by filter widget.
            tracked (bool, optional): Scroll tracking
            track_offset (float, optional): 0.0f:top, 0.5f:center, 1.0f:bottom
            shape (int, optional): Pin shape.
            category (str, optional): Category
            id (Union[int, str], optional): (deprecated)
        """
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'indent': indent, 'parent': parent, 'before': before, 'show': show, 'filter_key': filter_key, 'tracked': tracked, 'track_offset': track_offset, 'shape': shape, 'category': category}
        super().__init__(**kwargs)
        self.links: dict[DpgTag, 'LinkableNodeAttribute'] = {}

    def __iter__(self) -> Iterator[ValueObject]:
        """ Iterate over the objects in the container.
        """
        return super().__iter__()

    def add_link(self, attr: 'LinkableNodeAttribute') -> Self:
        """ Add link to the attribute.

        Args:
            attr (LinkableNodeAttribute): attr object.

        Returns:
            Self: own instance.
        """
        self.links[attr.tag] = attr
        logger.debug(f'[{self.__class__.__name__}] Added {attr} to {self}')

        return self

    def remove_link(self, attr: 'LinkableNodeAttribute') -> Self:
        """ Remove link from the attribute.

        Args:
            attr (LinkableNodeAttribute): lattrink object.

        Returns:
            Self: own instance.
        """
        del self.links[attr.tag]
        logger.debug(f'[{self.__class__.__name__}] Removed {attr} from {self}')

        return self

    def set_values(self, objects: list[Object], call_callback: bool = True) -> Self:
        """ Set value of the object.

        Args:
            objects (list[Object]): objects to set value from.
            call_callback (bool, optional): call callback. Defaults to True.
        """
        for obj in self:
            obj.set_values(objects, call_callback=call_callback)

        return self

    def update_linked_object(self, call_callback: bool = True) -> Self:
        """ Update linked object.

        Args:
            call_callback (bool, optional): Call callback. Defaults to True.

        Returns:
            Self: own instance.
        """
        raise NotImplementedError('update_linked_object() not implemented')


class StaticNodeAttribute(NodeAttribute):
    is_instance = True
    attribute_type = NodeAttributeType.STATIC


class InputNodeAttribute(LinkableNodeAttribute):
    is_instance = True
    attribute_type = NodeAttributeType.INPUT

    def update_linked_object(self, call_callback: bool = True) -> Self:
        """ Update linked object.

        Args:
            call_callback (bool, optional): Call callback. Defaults to True.

        Returns:
            Self: own instance.
        """
        # attr is OutputNodeAttribute
        values = [obj
                  for attr in self.links.values()
                  for obj in attr]
        self.set_values(values, call_callback=call_callback)

        logger.debug(f'[{self.__class__.__name__}] Updated linked object {self}')
        return self


class OutputNodeAttribute(LinkableNodeAttribute):
    is_instance = True
    attribute_type = NodeAttributeType.OUTPUT

    def update_linked_object(self, call_callback: bool = True) -> Self:
        """ Update linked object.

        Args:
            call_callback (bool, optional): Call callback. Defaults to True.

        Returns:
            Self: own instance.
        """
        # attr is InputNodeAttribute
        for attr in self.links.values():
            attr.update_linked_object(call_callback=call_callback)

        logger.debug(f'[{self.__class__.__name__}] Updated linked object {self}')
        return self


class Link(Object):
    is_instance = True
    generator = staticmethod(dpg_org.add_node_link)

    def __init__(self, attr_1: LinkableNodeAttribute, attr_2: LinkableNodeAttribute, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, parent: DpgTag = 0, show: bool = True):
        """	 Adds a node link between 2 node attributes.

        Args:
            attr_1 (Union[int, str]):
            attr_2 (Union[int, str]):
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
            show (bool, optional): Attempt to render widget.
            id (Union[int, str], optional): (deprecated)
        """
        self.output_attr = attr_1
        self.input_attr = attr_2
        args = (self.output_attr.tag, self.input_attr.tag)
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'parent': parent, 'show': show}
        super().__init__(*args, **kwargs)

    def build(self, parent: 'NodeEditor | None' = None, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (NodeEditor | None, optional): parent object. Defaults to None.

        Returns:
            Self: own instance.
        """
        super().build(parent=parent, **kwargs)
        self.output_attr.add_link(self.input_attr)
        self.input_attr.add_link(self.output_attr)

        logger.debug(f'[{self.__class__.__name__}] Linked {self.output_attr} to {self.input_attr} of {self}')
        return self

    def delete(self):
        """ Delete the link.
        """
        super().delete()
        self.output_attr.remove_link(self.input_attr)
        self.input_attr.remove_link(self.output_attr)

        logger.debug(f'[{self.__class__.__name__}] Deleted {self} from {self.output_attr} and {self.input_attr}')


class Node(Container):
    is_instance = True
    generator = staticmethod(dpg_org.add_node)

    def __init__(self, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, parent: DpgTag = 0, before: DpgTag = 0, payload_type: str = '$$DPG_PAYLOAD', drag_callback: Callable | None = None, drop_callback: Callable | None = None, show: bool = True, pos: list[int] | tuple[int, ...] = [], filter_key: str = '', delay_search: bool = False, tracked: bool = False, track_offset: float = 0.5, draggable: bool = True):
        """	 Adds a node to a node editor.

        Args:
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
            before (Union[int, str], optional): This item will be displayed before the specified item in the parent.
            payload_type (str, optional): Sender string type must be the same as the target for the target to run the payload_callback.
            drag_callback (Callable, optional): Registers a drag callback for drag and drop.
            drop_callback (Callable, optional): Registers a drop callback for drag and drop.
            show (bool, optional): Attempt to render widget.
            pos (Union[List[int], Tuple[int, ...]], optional): Places the item relative to window coordinates, [0,0] is top left.
            filter_key (str, optional): Used by filter widget.
            delay_search (bool, optional): Delays searching container for specified items until the end of the app. Possible optimization when a container has many children that are not accessed often.
            tracked (bool, optional): Scroll tracking
            track_offset (float, optional): 0.0f:top, 0.5f:center, 1.0f:bottom
            draggable (bool, optional): Allow node to be draggable.
            id (Union[int, str], optional): (deprecated)
        """
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'parent': parent, 'before': before, 'payload_type': payload_type, 'drag_callback': drag_callback, 'drop_callback': drop_callback, 'show': show, 'pos': pos, 'filter_key': filter_key, 'delay_search': delay_search, 'tracked': tracked, 'track_offset': track_offset, 'draggable': draggable}
        super().__init__(**kwargs)

    def build(self, parent: 'NodeEditor | None' = None, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (NodeEditor | None, optional): parent object. Defaults to None.

        Returns:
            Self: own instance.
        """
        super().build(parent=parent, **kwargs)

        def delete(sender, app_data, user_data: DpgTag):
            self.delete()
            dpg_org.configure_item(user_data, show=False)

        with dpg_org.popup(self.tag, mousebutton=dpg_org.mvMouseButton_Right) as tag:
            dpg_org.add_button(label="delete", callback=delete, user_data=tag)
        return self

    def delete(self, *args, **kwargs):
        """ Delete the container.
        """
        parent: NodeEditor = cast(NodeEditor, self.parent)
        links = [
            link
            for link in parent.links
            if (link.output_attr.node.tag == self.tag or link.input_attr.node.tag == self.tag)
        ]
        for link in links:
            parent.delink_callback(parent.tag, link.tag)
        super().delete(*args, **kwargs)
        del parent[self.tag]

    @property
    def statics(self) -> list[StaticNodeAttribute]:
        """ Get static attributes of the node.

        Returns:
            list[StaticNodeAttribute]: static attributes.
        """
        return [attr
                for attr in self
                if isinstance(attr, StaticNodeAttribute)]

    @property
    def inputs(self) -> list[InputNodeAttribute]:
        """ Get input attributes of the node.

        Returns:
            list[InputNodeAttribute]: input attributes.
        """
        return [attr
                for attr in self
                if isinstance(attr, InputNodeAttribute)]

    @property
    def outputs(self) -> list[OutputNodeAttribute]:
        """ Get output attributes of the node.

        Returns:
            list[OutputNodeAttribute]: output attributes.
        """
        return [attr
                for attr in self
                if isinstance(attr, OutputNodeAttribute)]

    @property
    def attrs(self) -> list[NodeAttribute]:
        """ Get all attributes of the node.

        Returns:
            list[NodeAttribute]: all attributes.
        """
        return [attr
                for attr in self
                if isinstance(attr, NodeAttribute)]


class NodeEditor(Container):
    is_instance = True
    generator = staticmethod(dpg_org.add_node_editor)

    def __init__(self, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, width: int = 0, height: int = 0, parent: DpgTag = 0, before: DpgTag = 0, callback: Callable | None = None, show: bool = True, filter_key: str = '', delay_search: bool = False, tracked: bool = False, track_offset: float = 0.5, delink_callback: Callable | None = None, menubar: bool = False, minimap: bool = False, minimap_location: int = 2):
        """	 Adds a node editor.

        Args:
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            width (int, optional): Width of the item.
            height (int, optional): Height of the item.
            parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
            before (Union[int, str], optional): This item will be displayed before the specified item in the parent.
            callback (Callable, optional): Registers a callback.
            show (bool, optional): Attempt to render widget.
            filter_key (str, optional): Used by filter widget.
            delay_search (bool, optional): Delays searching container for specified items until the end of the app. Possible optimization when a container has many children that are not accessed often.
            tracked (bool, optional): Scroll tracking
            track_offset (float, optional): 0.0f:top, 0.5f:center, 1.0f:bottom
            delink_callback (Callable, optional): Callback ran when a link is detached.
            menubar (bool, optional): Shows or hides the menubar.
            minimap (bool, optional): Shows or hides the Minimap. New in 1.6.
            minimap_location (int, optional): mvNodeMiniMap_Location_* constants. New in 1.6.
            id (Union[int, str], optional): (deprecated)
        """
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'width': width, 'height': height, 'parent': parent, 'before': before, 'callback': callback, 'show': show, 'filter_key': filter_key, 'delay_search': delay_search, 'tracked': tracked, 'track_offset': track_offset, 'delink_callback': delink_callback, 'menubar': menubar, 'minimap': minimap, 'minimap_location': minimap_location}
        kwargs.update({'callback': callback or self.link_callback})
        kwargs.update({'delink_callback': delink_callback or self.delink_callback})
        super().__init__(**kwargs)

    def __loop_check(self, attrs: list[LinkableNodeAttribute], target: Node):
        for attr in attrs:
            if attr.node == target:
                raise ValueError
            self.__loop_check([a
                               for attr in attr.node.inputs
                               for a in attr.links.values()], target)

    def link_callback(self, sender: DpgTag, app_data: tuple[DpgTag, DpgTag]):
        """ Callback for link.

        Args:
            sender (DpgTag): own tag.
            app_data (tuple[DpgTag, DpgTag]): input attr tag and output attr tag.
        """
        # fix https://github.com/hoffstadt/DearPyGui/issues/2122
        sender = get_tag(sender)
        app_data_attrs: tuple[LinkableNodeAttribute] = (self[get_tag(app_data[0])], self[get_tag(app_data[1])])

        try:
            self.__loop_check([app_data_attrs[0]], app_data_attrs[1].node)
        except ValueError:
            logger.warning(f'[{self.__class__.__name__}] Loop link detected: {app_data_attrs[0]} -> {app_data_attrs[1]}')
            return

        link = Link(*app_data_attrs).build(parent=self)
        self[link.tag] = link

        link.output_attr.update_linked_object(call_callback=True)
        link.input_attr.update_linked_object(call_callback=True)

        logger.debug(f'[{self.__class__.__name__}] Linked {link.output_attr} to {link.input_attr} in {self}')

    def delink_callback(self, sender: DpgTag, app_data: DpgTag):
        """ Callback for delink.

        Args:
            sender (DpgTag): own tag.
            app_data (DpgTag): link tag.
        """
        # fix https://github.com/hoffstadt/DearPyGui/issues/2122
        sender = get_tag(sender)
        app_data = get_tag(app_data)

        link: Link = self[app_data]
        link.delete()
        del self[link.tag]

        link.output_attr.update_linked_object(call_callback=True)
        link.input_attr.update_linked_object(call_callback=True)

        logger.debug(f'[{self.__class__.__name__}] Delinked {link.output_attr} from {link.input_attr} in {self}')

    def clear_selected_links(self):
        """ Clear selected links in the node editor.
        """
        dpg_org.clear_selected_links(self.tag)

    def clear_selected_nodes(self):
        """ Clear selected nodes in the node editor
        """
        dpg_org.clear_selected_nodes(self.tag)

    def get_selected_links(self) -> list[Link]:
        """ Get selected links in the node editor.

        Returns:
            list[Link]: Selected links.
        """
        return [self[link_id] for link_id in dpg_org.get_selected_links(self.tag)]

    def get_selected_nodes(self) -> list[Node]:
        """ Get selected nodes in the node editor.

        Returns:
            list[Node]: Selected nodes.
        """
        return [self[node_id] for node_id in dpg_org.get_selected_nodes(self.tag)]

    def get_nodeattr_from_object(self, tag: DpgTag) -> NodeAttribute:
        """ Get node attribute from object tag.

        Args:
            tag (DpgTag): object tag.

        Returns:
            NodeAttribute: node attribute object.
        """
        return self[tag].parent

    def get_node_from_object(self, tag: DpgTag) -> Node:
        """ Get node from object tag.

        Args:
            tag (DpgTag): object tag.

        Returns:
            Node: node object.
        """
        return self.get_nodeattr_from_object(tag).node

    def print_objects(self, print_func=print):
        """ Print node editor objects.
        """
        super().print(print_func)
        for obj in self:
            obj.print(print_func)

    def print_node(self, print_func=print):
        """ Print node editor tree.
        """
        print_func('# Node tree #####')
        print_func(f'{self}')
        for node in self.nodes:
            print_func(f'    {node}')
            for attr in node.attrs:
                print_func(f'        {attr}')
                for obj in attr:
                    print_func(f'            {obj}')
        print_func('# Link tree #####')
        print_func(f'{self}')
        for link in self.links:
            print_func(f'    {link}')
            print_func(f'        {link.output_attr} -> {link.input_attr}')

    @property
    def nodes(self) -> list[Node]:
        """ Get nodes of the node editor.

        Returns:
            list[Node]: nodes.
        """
        return [obj
                for obj in self
                if isinstance(obj, Node)]

    @property
    def links(self) -> list[Link]:
        """ Get links of the node editor.

        Returns:
            list[Link]: links.
        """
        return [obj
                for obj in self
                if isinstance(obj, Link)]
