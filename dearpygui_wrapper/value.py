import logging
from typing import Any, Callable

from dearpygui_wrapper import DpgTag, dpg_org
from dearpygui_wrapper.base import ValueObject

logger = logging.getLogger('dgp_wrapper')


class Text(ValueObject):
    is_instance = True
    generator = staticmethod(dpg_org.add_text)

    def __init__(self, default_value: str = '', *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, indent: int = -1, parent: DpgTag = 0, before: DpgTag = 0, source: DpgTag = 0, payload_type: str = '$$DPG_PAYLOAD', drag_callback: Callable | None = None, drop_callback: Callable | None = None, show: bool = True, pos: list[int] | tuple[int, ...] = [], filter_key: str = '', tracked: bool = False, track_offset: float = 0.5, wrap: int = -1, bullet: bool = False, color: list[int] | tuple[int, ...] = (-255, 0, 0, 255), show_label: bool = False):
        """	 Adds text. Text can have an optional label that will display to the right of the text.

        Args:
            default_value (str, optional):
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            indent (int, optional): Offsets the widget to the right the specified number multiplied by the indent style.
            parent (Union[int, str], optional): Parent to add this item to. (runtime adding)
            before (Union[int, str], optional): This item will be displayed before the specified item in the parent.
            source (Union[int, str], optional): Overrides 'id' as value storage key.
            payload_type (str, optional): Sender string type must be the same as the target for the target to run the payload_callback.
            drag_callback (Callable, optional): Registers a drag callback for drag and drop.
            drop_callback (Callable, optional): Registers a drop callback for drag and drop.
            show (bool, optional): Attempt to render widget.
            pos (Union[List[int], Tuple[int, ...]], optional): Places the item relative to window coordinates, [0,0] is top left.
            filter_key (str, optional): Used by filter widget.
            tracked (bool, optional): Scroll tracking
            track_offset (float, optional): 0.0f:top, 0.5f:center, 1.0f:bottom
            wrap (int, optional): Number of pixels from the start of the item until wrapping starts.
            bullet (bool, optional): Places a bullet to the left of the text.
            color (Union[List[int], Tuple[int, ...]], optional): Color of the text (rgba).
            show_label (bool, optional): Displays the label to the right of the text.
            id (Union[int, str], optional): (deprecated)
        """
        kwargs = {'default_value': default_value, 'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'indent': indent, 'parent': parent, 'before': before, 'source': source, 'payload_type': payload_type, 'drag_callback': drag_callback, 'drop_callback': drop_callback, 'show': show, 'pos': pos, 'filter_key': filter_key, 'tracked': tracked, 'track_offset': track_offset, 'wrap': wrap, 'bullet': bullet, 'color': color, 'show_label': show_label}
        super().__init__(**kwargs)

    def set_values(self, values: list[Any]):
        """ Set value of the object.

        Args:
            values (list[Any]): value to set.
        """
        self.value = '\n'.join(map(str, values))


class InputText(ValueObject):
    is_instance = True
    generator = staticmethod(dpg_org.add_input_text)

    def __init__(self, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, width: int = 0, height: int = 0, indent: int = -1, parent: DpgTag = 0, before: DpgTag = 0, source: DpgTag = 0, payload_type: str = '$$DPG_PAYLOAD', callback: Callable | None = None, drag_callback: Callable | None = None, drop_callback: Callable | None = None, show: bool = True, enabled: bool = True, pos: list[int] | tuple[int, ...] = [], filter_key: str = '', tracked: bool = False, track_offset: float = 0.5, default_value: str = '', hint: str = '', multiline: bool = False, no_spaces: bool = False, uppercase: bool = False, tab_input: bool = False, decimal: bool = False, hexadecimal: bool = False, readonly: bool = False, password: bool = False, scientific: bool = False, on_enter: bool = False, auto_select_all: bool = False, ctrl_enter_for_new_line: bool = False, no_horizontal_scroll: bool = False, always_overwrite: bool = False, no_undo_redo: bool = False, escape_clears_all: bool = False):
        """	 Adds input for text.

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
            source (Union[int, str], optional): Overrides 'id' as value storage key.
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
            default_value (str, optional):
            hint (str, optional): Displayed only when value is an empty string. Will reappear if input value is set to empty string. Will not show if default value is anything other than default empty string.
            multiline (bool, optional): Allows for multiline text input.
            no_spaces (bool, optional): Filter out spaces and tabs.
            uppercase (bool, optional): Automatically make all inputs uppercase.
            tab_input (bool, optional): Allows tabs to be input into the string value instead of changing item focus.
            decimal (bool, optional): Only allow characters 0123456789.+-*/
            hexadecimal (bool, optional): Only allow characters 0123456789ABCDEFabcdef
            readonly (bool, optional): Activates read only mode where no text can be input but text can still be highlighted.
            password (bool, optional): Display all input characters as '*'.
            scientific (bool, optional): Only allow characters 0123456789.+-*/eE (Scientific notation input)
            on_enter (bool, optional): Only runs callback on enter key press.
            auto_select_all (bool, optional): Select entire text when first taking mouse focus
            ctrl_enter_for_new_line (bool, optional): In multi-line mode, unfocus with Enter, add new line with Ctrl+Enter (default is opposite: unfocus with Ctrl+Enter, add line with Enter).
            no_horizontal_scroll (bool, optional): Disable following the cursor horizontally
            always_overwrite (bool, optional): Overwrite mode
            no_undo_redo (bool, optional): Disable undo/redo.
            escape_clears_all (bool, optional): Escape key clears content if not empty, and deactivate otherwise (contrast to default behavior of Escape to revert)
            id (Union[int, str], optional): (deprecated)
        """
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'width': width, 'height': height, 'indent': indent, 'parent': parent, 'before': before, 'source': source, 'payload_type': payload_type, 'callback': callback, 'drag_callback': drag_callback, 'drop_callback': drop_callback, 'show': show, 'enabled': enabled, 'pos': pos, 'filter_key': filter_key, 'tracked': tracked, 'track_offset': track_offset, 'default_value': default_value, 'hint': hint, 'multiline': multiline, 'no_spaces': no_spaces, 'uppercase': uppercase, 'tab_input': tab_input, 'decimal': decimal, 'hexadecimal': hexadecimal, 'readonly': readonly, 'password': password, 'scientific': scientific, 'on_enter': on_enter, 'auto_select_all': auto_select_all, 'ctrl_enter_for_new_line': ctrl_enter_for_new_line, 'no_horizontal_scroll': no_horizontal_scroll, 'always_overwrite': always_overwrite, 'no_undo_redo': no_undo_redo, 'escape_clears_all': escape_clears_all}
        super().__init__(**kwargs)

    def set_values(self, values: list[Any]):
        """ Set value of the object.

        Args:
            values (list[Any]): value to set.
        """
        self.value = '\n'.join(map(str, values))
