import logging
from enum import IntEnum
from typing import Any, Callable, Self, cast

from dearpygui_wrapper import (Container, DpgTag, Object, ValueObject, dpg_org,
                               get_tag)

logger = logging.getLogger('dgp_wrapper')


class NodeAttributeType(IntEnum):
    STATIC = dpg_org.mvNode_Attr_Static
    INPUT = dpg_org.mvNode_Attr_Input
    OUTPUT = dpg_org.mvNode_Attr_Output


class NodeAttribute(Container):
    is_instance = True
    generator = staticmethod(dpg_org.add_node_attribute)

    def __init__(self, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, indent: int = -1, parent: DpgTag = 0, before: DpgTag = 0, show: bool = True, filter_key: str = '', tracked: bool = False, track_offset: float = 0.5, attribute_type: int = 0, shape: int = 1, category: str = 'general'):
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
            attribute_type (int, optional): mvNode_Attr_Input, mvNode_Attr_Output, or mvNode_Attr_Static.
            shape (int, optional): Pin shape.
            category (str, optional): Category
            id (Union[int, str], optional): (deprecated)
        """
        self.attribute_type = NodeAttributeType(attribute_type)
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'indent': indent, 'parent': parent, 'before': before, 'show': show, 'filter_key': filter_key, 'tracked': tracked, 'track_offset': track_offset, 'attribute_type': attribute_type, 'shape': shape, 'category': category}
        super().__init__(**kwargs)
        self.links: dict[DpgTag, NodeAttribute] = {}

    def __getitem__(self, key: DpgTag) -> ValueObject:
        return super().__getitem__(key)

    def default_tag(self) -> DpgTag:
        return f'{self.__class__.__name__}({self.attribute_type.name})##{self.id}'

    def add_link(self, link: 'Link') -> Self:
        """ Add link to the attribute.

        Args:
            link (Link): link object.

        Returns:
            Self: own instance.
        """
        match self.attribute_type:
            case NodeAttributeType.INPUT:
                self.links[link.tag] = link.out_attr
                logger.debug(f'[{self.__class__.__name__}] Added {link.out_attr} of {link} to {self}')
            case NodeAttributeType.OUTPUT:
                self.links[link.tag] = link.in_attr
                logger.debug(f'[{self.__class__.__name__}] Added {link.in_attr} of {link} to {self}')
            case _:
                pass

        return self

    def remove_link(self, link: 'Link') -> Self:
        """ Remove link from the attribute.

        Args:
            link (Link): link object.

        Returns:
            Self: own instance.
        """
        del self.links[link.tag]
        logger.debug(f'[{self.__class__.__name__}] Removed {link} from {self}')

        return self

    def set_values(self, values: list[Any], call_callback: bool = True) -> Self:
        """ Set value of the object.

        Args:
            values (list[Any]): value to set.
            call_callback (bool, optional): call callback. Defaults to True.
        """
        for _, obj in self:
            cast(ValueObject, obj).set_values(values, call_callback=call_callback)

        return self

    def update_linked_object(self, call_callback: bool = True) -> Self:
        """ Update linked object.

        Args:
            call_callback (bool, optional): Call callback. Defaults to True.

        Returns:
            Self: own instance.
        """
        match self.attribute_type:
            case NodeAttributeType.INPUT:
                values = [cast(ValueObject, obj).value
                          for attr in self.links.values()
                          for _, obj in attr]
                self.set_values(values, call_callback=call_callback)
            case NodeAttributeType.OUTPUT:
                for attr in self.links.values():
                    attr.update_linked_object(call_callback=call_callback)
            case _:
                pass

        logger.debug(f'[{self.__class__.__name__}] Updated linked object {self}')
        return self

    @property
    def node(self) -> 'Node':
        """ Get node of the attribute.

        Raises:
            ValueError: If the attribute has no node.

        Returns:
            Node: node of the attribute.
        """
        return self.parent


class Link(Object):
    is_instance = True
    generator = staticmethod(dpg_org.add_node_link)

    def __init__(self, attr_1: NodeAttribute, attr_2: NodeAttribute, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, parent: DpgTag = 0, show: bool = True):
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
        self.out_attr = attr_1
        self.in_attr = attr_2
        args = (self.out_attr.tag, self.in_attr.tag)
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'parent': parent, 'show': show}
        super().__init__(*args, **kwargs)

    def delete(self):
        """ Delete the link.
        """
        super().delete()
        self.out_attr.remove_link(self)
        self.in_attr.remove_link(self)

        logger.debug(f'[{self.__class__.__name__}] Deleted {self} from {self.out_attr} and {self.in_attr}')

    def build(self, parent: 'NodeEditor', *args, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (Object): parent object.

        Returns:
            Self: own instance.
        """
        super().build(parent, *args, **kwargs)
        self.out_attr.add_link(self)
        self.in_attr.add_link(self)

        logger.debug(f'[{self.__class__.__name__}] Linked {self.out_attr} to {self.in_attr} of {self}')
        return self


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

    def delete(self, *args, **kwargs):
        """ Delete the container.
        """
        parent: NodeEditor = cast(NodeEditor, self.parent)
        links = [
            link
            for _, link in parent
            if isinstance(link, Link) and (link.out_attr.node.tag == self.tag or link.in_attr.node.tag == self.tag)
        ]
        for link in links:
            parent.delink_callback(parent.tag, link.tag)
        super().delete(*args, **kwargs)
        del parent[self.tag]

    def build(self, parent: 'NodeEditor', *args, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (Object): parent object.

        Returns:
            Self: own instance.
        """
        super().build(parent, *args, **kwargs)

        def delete(sender, app_data, user_data: DpgTag):
            self.delete()
            dpg_org.configure_item(user_data, show=False)

        with dpg_org.popup(self.tag, mousebutton=dpg_org.mvMouseButton_Right) as tag:
            dpg_org.add_button(label="delete", callback=delete, user_data=tag)
        return self

    def __getitem__(self, key: DpgTag) -> NodeAttribute:
        return super().__getitem__(key)


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

    def __getitem__(self, key: DpgTag) -> Node:
        return super().__getitem__(key)

    def __loop_check(self, attrs: list[NodeAttribute], target: NodeAttribute):
        for attr in attrs:
            parent: Node = attr.parent
            if parent == target.node:
                raise ValueError
            input_attrs = [a
                           for _, a in parent
                           if isinstance(a, NodeAttribute)
                           and a.attribute_type == NodeAttributeType.INPUT
                           and len(a.links)]
            linked_attrs = [la
                            for a in input_attrs
                            for la in a.links.values()]
            self.__loop_check(linked_attrs, target)

    def link_callback(self, sender: DpgTag, app_data: tuple[DpgTag, DpgTag]):
        """ Callback for link.

        Args:
            sender (DpgTag): own tag.
            app_data (tuple[DpgTag, DpgTag]): input attr tag and output attr tag.
        """
        # fix https://github.com/hoffstadt/DearPyGui/issues/2122
        sender = get_tag(sender)
        app_data_attrs: tuple[NodeAttribute] = (self[get_tag(app_data[0])], self[get_tag(app_data[1])])

        try:
            self.__loop_check([app_data_attrs[0]], app_data_attrs[1])
        except ValueError:
            logger.warning(f'[{self.__class__.__name__}] Loop link detected: {app_data_attrs[0]} -> {app_data_attrs[1]}')
            return

        link = Link(*app_data_attrs).build(self)
        self[link.tag] = link

        link.out_attr.update_linked_object(call_callback=True)
        link.in_attr.update_linked_object(call_callback=True)

        logger.debug(f'[{self.__class__.__name__}] Linked {link.out_attr} to {link.in_attr} in {self}')

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

        link.out_attr.update_linked_object(call_callback=True)
        link.in_attr.update_linked_object(call_callback=True)

        logger.debug(f'[{self.__class__.__name__}] Delinked {link.out_attr} from {link.in_attr} in {self}')

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

    def print_all(self, print_func=print):
        """ Print all node editor tree.
        """
        print_func('# NodeEditor objects #####')
        for tag, obj in self:
            print_func(f'    {tag}: {obj}')
        print_func('# Node objects #####')
        for _, obj in self:
            if isinstance(obj, Node):
                for tag, o in obj:
                    print_func(f'    {tag}: {o}')
        print_func('# NodeAttribute objects #####')
        for _, obj in self:
            if isinstance(obj, NodeAttribute):
                for tag, o in obj:
                    print_func(f'    {tag}: {o}')

    def print_node(self, print_func=print):
        """ Print node editor tree.
        """
        print_func('# Node tree #####')
        print_func(f'{self}')
        for _, node in self:
            if isinstance(node, Node):
                print_func(f'    {node}')
                for _, attr in node:
                    if isinstance(attr, NodeAttribute):
                        print_func(f'        {attr}')
                        for _, obj in attr:
                            if isinstance(obj, ValueObject):
                                print_func(f'            {obj}')
        print_func('# Link tree #####')
        print_func(f'{self}')
        for _, link in self:
            if isinstance(link, Link):
                print_func(f'    {link}')
                print_func(f'        {link.out_attr} -> {link.in_attr}')
