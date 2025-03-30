import logging
from typing import Any, Callable

from dearpygui_wrapper import DpgTag, dpg_org
from dearpygui_wrapper.base import Object

logger = logging.getLogger('dgp_wrapper')


class Button(Object):
    is_instance = True
    generator = staticmethod(dpg_org.add_button)

    def __init__(self, *, label: str = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, width: int = 0, height: int = 0, indent: int = -1, parent: DpgTag = 0, before: DpgTag = 0, payload_type: str = '$$DPG_PAYLOAD', callback: Callable | None = None, drag_callback: Callable | None = None, drop_callback: Callable = None, show: bool = True, enabled: bool = True, pos: list[int] | tuple[int, ...] = [], filter_key: str = '', tracked: bool = False, track_offset: float = 0.5, small: bool = False, arrow: bool = False, direction: int = 0, repeat: bool = False):
        """	 Adds a button.

        Args:
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            width (int, optional): Width of the item.
            height (int, optional): Height of the item.
            indent (int, optional): Offsets the widget to the right the specified number multiplied by the indent style.
            parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
            before (Union[int, str], optional): This item will be displayed before the specified item in the parent.
            payload_type (str, optional): Sender string type must be the same as the target for the target to run the payload_callback.
            callback (Callable, optional): Registers a callback.
            drag_callback (Callable, optional): Registers a drag callback for drag and drop.
            drop_callback (Callable, optional): Registers a drop callback for drag and drop.
            show (bool, optional): Attempt to render widget.
            enabled (bool, optional): Turns off functionality of widget and applies the disabled theme.
            pos (Union[List[int], Tuple[int, ...]], optional): Places the item relative to window coordinates, [0,0] is top left.
            filter_key (str, optional): Used by filter widget.
            tracked (bool, optional): Scroll tracking
            track_offset (float, optional): 0.0f:top, 0.5f:center, 1.0f:bottom
            small (bool, optional): Shrinks the size of the button to the text of the label it contains. Useful for embedding in text.
            arrow (bool, optional): Displays an arrow in place of the text string. This requires the direction keyword.
            direction (int, optional): Sets the cardinal direction for the arrow by using constants mvDir_Left, mvDir_Up, mvDir_Down, mvDir_Right, mvDir_None. Arrow keyword must be set to True.
            repeat (bool, optional): Hold to continuosly repeat the click.
            id (Union[int, str], optional): (deprecated)
        Returns:
            Union[int, str]
        """
        args = tuple()
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'width': width, 'height': height, 'indent': indent, 'parent': parent, 'before': before, 'payload_type': payload_type, 'callback': callback, 'drag_callback': drag_callback, 'drop_callback': drop_callback, 'show': show, 'enabled': enabled, 'pos': pos, 'filter_key': filter_key, 'tracked': tracked, 'track_offset': track_offset, 'small': small, 'arrow': arrow, 'direction': direction, 'repeat': repeat}
        super().__init__(*args, **kwargs)
