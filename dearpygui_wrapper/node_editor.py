import logging
from enum import IntEnum
from typing import Any, Callable, Self, cast

from dearpygui_wrapper import DpgTag, dpg
from dearpygui_wrapper.base import Container, Manager, Object, ValueObject

logger = logging.getLogger('dgp_wrapper')


class NodeAttributeType(IntEnum):
    STATIC = dpg.mvNode_Attr_Static
    INPUT = dpg.mvNode_Attr_Input
    OUTPUT = dpg.mvNode_Attr_Output


class NodeAttribute(Container):
    is_instance = True
    generator = staticmethod(dpg.add_node_attribute)

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
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'indent': indent, 'parent': parent, 'before': before, 'show': show, 'filter_key': filter_key, 'tracked': tracked, 'track_offset': track_offset, 'attribute_type': attribute_type, 'shape': shape, 'category': category}
        super().__init__(**kwargs)
        self.links: list[DpgTag] = []

    def add(self, obj: Object, manager: dict[DpgTag, Object] | None = None) -> Self:
        """ Add object to the attribute.

        Args:
            obj (Object): object to add.
            manager (dict[DpgTag, Object] | None, optional): tag manager. Defaults to None.

        Raises:
            ValueError: If the attribute already has an object.

        Returns:
            Self: own instance.
        """
        if self.objects:
            raise ValueError(f'{self.__class__.__name__} can have only one object.')

        super().add(obj, manager=manager)
        if manager is not None:
            manager[self.tag] = obj

        return self

    def add_link(self, link_id: DpgTag) -> Self:
        """ Add link to the attribute.

        Args:
            link_id (DpgTag): link id.

        Returns:
            Self: own instance.
        """
        self.links.append(link_id)

        return self

    def remove_link(self, link_id: DpgTag) -> Self:
        """ Remove link from the attribute.

        Args:
            link_id (DpgTag): link id.

        Returns:
            Self: own instance.
        """
        self.links.remove(link_id)

        return self

    def exists_link(self, link_id: DpgTag) -> bool:
        """ Check if the link exists in the attribute.

        Args:
            link_id (DpgTag): link id.

        Returns:
            bool: True if the link exists, False otherwise.
        """
        return link_id in self.links

    @property
    def object(self) -> ValueObject:
        """ Get object of the attribute.

        Raises:
            ValueError: If the attribute has no object.

        Returns:
            ValueObject: object of the attribute.
        """
        if not self.objects:
            raise ValueError(f'{self.__class__.__name__} has no object.')

        return cast(ValueObject, self.objects[0])


class Link(Object):
    is_instance = True
    generator = staticmethod(dpg.add_node_link)

    def __init__(self, attr_1: DpgTag, attr_2: DpgTag, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, parent: DpgTag = 0, show: bool = True):
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
        args = (attr_1, attr_2)
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'parent': parent, 'show': show}
        super().__init__(*args, **kwargs)

    def build(self, parent: Object, manager: dict[DpgTag, Object], *args, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (Object): parent object.
            manager (dict[DpgTag, Object]): tag manager.

        Returns:
            Self: own instance.
        """
        super().build(parent, *args, manager=manager, **kwargs)
        self.in_attr = cast(NodeAttribute, manager[self.args[0]])
        self.out_attr = cast(NodeAttribute, manager[self.args[1]])

        return self

    def update(self, app_data: Any) -> Self:
        """ Update the link.

        Args:
            app_data (Any): data.

        Returns:
            Self: own instance.
        """
        self.out_attr.object.value = app_data

        return self


class Node(Container):
    is_instance = True
    generator = staticmethod(dpg.add_node)

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


class NodeEditor(Manager):
    is_instance = True
    generator = staticmethod(dpg.add_node_editor)

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
        kwargs.update({'callback': callback or self.__link_callback})
        kwargs.update({'delink_callback': delink_callback or self.__delink_callback})
        super().__init__(**kwargs)

    def __link_callback(self, sener: DpgTag, app_data: tuple[DpgTag, DpgTag]):
        """ Callback for link.

        Args:
            sener (DpgTag): own tag.
            app_data (tuple[DpgTag, DpgTag]): input attr tag and output attr tag.
        """
        in_attr: NodeAttribute = cast(NodeAttribute, self.manager[app_data[0]])
        parent = self.manager[sener]
        link = Link(*app_data)\
            .build(parent, manager=self.manager)\
            .update(in_attr.object.value)
        in_attr.add_link(link.tag)

    def __delink_callback(self, sender: DpgTag, app_data: DpgTag):
        """ Callback for delink.

        Args:
            sender (DpgTag): own tag.
            app_data (DpgTag): link tag.
        """
        dpg.delete_item(app_data)
        del self.manager[app_data]
        for attr in self.manager.values():
            if isinstance(attr, NodeAttribute) and attr.exists_link(app_data):
                attr.remove_link(app_data)
                break

    def update_links(self, sender: DpgTag, app_data: Any) -> Self:
        """ Update links.

        Args:
            sender (DpgTag): value object tag.
            app_data (Any): data.

        Returns:
            Self: own instance.
        """
        attr = cast(NodeAttribute, self.manager[sender].parent)
        for link_id in attr.links:
            link = cast(Link, self.manager[link_id])
            link.update(app_data)
        return self

    def clear_selected_links(self):
        """ Clear selected links in the node editor.
        """
        dpg.clear_selected_links(self.tag)

    def clear_selected_nodes(self):
        """ Clear selected nodes in the node editor
        """
        dpg.clear_selected_nodes(self.tag)

    def get_selected_links(self) -> list[Link]:
        """ Get selected links in the node editor.

        Returns:
            list[Link]: Selected links.
        """
        link_ids = cast(list[DpgTag], dpg.get_selected_links(self.tag))
        return [cast(Link, self.manager[link_id]) for link_id in link_ids]

    def get_selected_nodes(self) -> list[Node]:
        """ Get selected nodes in the node editor.

        Returns:
            list[Node]: Selected nodes.
        """
        node_ids = cast(list[DpgTag], dpg.get_selected_nodes(self.tag))
        return [cast(Node, self.manager[node_id]) for node_id in node_ids]
