import logging
from typing import Any, Callable, Self

from dearpygui_wrapper import DpgTag, dpg
from dearpygui_wrapper.base import Container, Object

logger = logging.getLogger('dgp_wrapper')


class Window(Object):
    is_instance = True
    generator = staticmethod(dpg.add_window)

    def __init__(self, *, label: str | None = None, user_data: Any = None, use_internal_label: bool = True, tag: DpgTag = 0, width: int = 0, height: int = 0, indent: int = -1, show: bool = True, pos: list[int] | tuple[int, ...] = [], delay_search: bool = False, min_size: list[int] | tuple[int, ...] = [100, 100], max_size: list[int] | tuple[int, ...] = [30000, 30000], menubar: bool = False, collapsed: bool = False, autosize: bool = False, no_resize: bool = False, unsaved_document: bool = False, no_title_bar: bool = False, no_move: bool = False, no_scrollbar: bool = False, no_collapse: bool = False, horizontal_scrollbar: bool = False, no_focus_on_appearing: bool = False, no_bring_to_front_on_focus: bool = False, no_close: bool = False, no_background: bool = False, modal: bool = False, popup: bool = False, no_saved_settings: bool = False, no_open_over_existing_popup: bool = True, no_scroll_with_mouse: bool = False, on_close: Callable | None = None):
        """	 Creates a new window for following items to be added to.

        Args:
            label (str, optional): Overrides 'name' as label.
            user_data (Any, optional): User data for callbacks
            use_internal_label (bool, optional): Use generated internal label instead of user specified (appends ### uuid).
            tag (Union[int, str], optional): Unique id used to programmatically refer to the item.If label is unused this will be the label.
            width (int, optional): Width of the item.
            height (int, optional): Height of the item.
            indent (int, optional): Offsets the widget to the right the specified number multiplied by the indent style.
            show (bool, optional): Attempt to render widget.
            pos (Union[List[int], Tuple[int, ...]], optional): Places the item relative to window coordinates, [0,0] is top left.
            delay_search (bool, optional): Delays searching container for specified items until the end of the app. Possible optimization when a container has many children that are not accessed often.
            min_size (Union[List[int], Tuple[int, ...]], optional): Minimum window size.
            max_size (Union[List[int], Tuple[int, ...]], optional): Maximum window size.
            menubar (bool, optional): Shows or hides the menubar.
            collapsed (bool, optional): Collapse the window.
            autosize (bool, optional): Autosized the window to fit it's items.
            no_resize (bool, optional): Allows for the window size to be changed or fixed.
            unsaved_document (bool, optional): Show a special marker if the document is not saved.
            no_title_bar (bool, optional): Title name for the title bar of the window.
            no_move (bool, optional): Allows for the window's position to be changed or fixed.
            no_scrollbar (bool, optional):  Disable scrollbars. (window can still scroll with mouse or programmatically)
            no_collapse (bool, optional): Disable user collapsing window by double-clicking on it.
            horizontal_scrollbar (bool, optional): Allow horizontal scrollbar to appear. (off by default)
            no_focus_on_appearing (bool, optional): Disable taking focus when transitioning from hidden to visible state.
            no_bring_to_front_on_focus (bool, optional): Disable bringing window to front when taking focus. (e.g. clicking on it or programmatically giving it focus)
            no_close (bool, optional): Disable user closing the window by removing the close button.
            no_background (bool, optional): Sets Background and border alpha to transparent.
            modal (bool, optional): Fills area behind window according to the theme and disables user ability to interact with anything except the window.
            popup (bool, optional): Fills area behind window according to the theme, removes title bar, collapse and close. Window can be closed by selecting area in the background behind the window.
            no_saved_settings (bool, optional): Never load/save settings in .ini file.
            no_open_over_existing_popup (bool, optional): Don't open if there's already a popup
            no_scroll_with_mouse (bool, optional): Disable user vertically scrolling with mouse wheel.
            on_close (Callable, optional): Callback ran when window is closed.
            id (Union[int, str], optional): (deprecated)
        """
        kwargs = {'label': label, 'user_data': user_data, 'use_internal_label': use_internal_label, 'tag': tag, 'width': width, 'height': height, 'indent': indent, 'show': show, 'pos': pos, 'delay_search': delay_search, 'min_size': min_size, 'max_size': max_size, 'menubar': menubar, 'collapsed': collapsed, 'autosize': autosize, 'no_resize': no_resize, 'unsaved_document': unsaved_document, 'no_title_bar': no_title_bar, 'no_move': no_move, 'no_scrollbar': no_scrollbar, 'no_collapse': no_collapse, 'horizontal_scrollbar': horizontal_scrollbar, 'no_focus_on_appearing': no_focus_on_appearing, 'no_bring_to_front_on_focus': no_bring_to_front_on_focus, 'no_close': no_close, 'no_background': no_background, 'modal': modal, 'popup': popup, 'no_saved_settings': no_saved_settings, 'no_open_over_existing_popup': no_open_over_existing_popup, 'no_scroll_with_mouse': no_scroll_with_mouse, 'on_close': on_close}
        super().__init__(**kwargs)

    def build(self, primary=False, *args, **kwargs) -> 'Window':
        super().build(None, *args, **kwargs)
        dpg.set_primary_window(self.tag, primary)

        return self


class ViewPort(Container):
    is_instance = True
    generator = staticmethod(dpg.create_viewport)

    def __init__(self, *, title: str = 'Dear PyGui', small_icon: str = '', large_icon: str = '', width: int = 1280, height: int = 800, x_pos: int = 100, y_pos: int = 100, min_width: int = 250, max_width: int = 10000, min_height: int = 250, max_height: int = 10000, resizable: bool = True, vsync: bool = True, always_on_top: bool = False, decorated: bool = True, clear_color: list[float] | tuple[float, ...] = (0, 0, 0, 255), disable_close: bool = False):
        """ Creates a viewport. Viewports are required.

        Args:
            title (str, optional): Sets the title of the viewport.
            small_icon (str, optional): Sets the small icon that is found in the viewport's decorator bar. Must be ***.ico on windows and either ***.ico or ***.png on mac.
            large_icon (str, optional): Sets the large icon that is found in the task bar while the app is running. Must be ***.ico on windows and either ***.ico or ***.png on mac.
            width (int, optional): Sets the width of the drawable space on the viewport. Does not inclue the border.
            height (int, optional): Sets the height of the drawable space on the viewport. Does not inclue the border or decorator bar.
            x_pos (int, optional): Sets x position the viewport will be drawn in screen coordinates.
            y_pos (int, optional): Sets y position the viewport will be drawn in screen coordinates.
            min_width (int, optional): Applies a minimuim limit to the width of the viewport.
            max_width (int, optional): Applies a maximum limit to the width of the viewport.
            min_height (int, optional): Applies a minimuim limit to the height of the viewport.
            max_height (int, optional): Applies a maximum limit to the height of the viewport.
            resizable (bool, optional): Enables and Disables user ability to resize the viewport.
            vsync (bool, optional): Enables and Disables the renderloop vsync limit. vsync frame value is set by refresh rate of display.
            always_on_top (bool, optional): Forces the viewport to always be drawn ontop of all other viewports.
            decorated (bool, optional): Enabled and disabled the decorator bar at the top of the viewport.
            clear_color (Union[List[float], Tuple[float, ...]], optional): Sets the color of the back of the viewport.
            disable_close (bool, optional): Disables the viewport close button. can be used with set_exit_callback
        """
        self.kwargs = {'title': title, 'small_icon': small_icon, 'large_icon': large_icon, 'width': width, 'height': height, 'x_pos': x_pos, 'y_pos': y_pos, 'min_width': min_width, 'max_width': max_width, 'min_height': min_height, 'max_height': max_height, 'resizable': resizable, 'vsync': vsync, 'always_on_top': always_on_top, 'decorated': decorated, 'clear_color': clear_color, 'disable_close': disable_close}
        dpg.create_context()
        super().__init__(**self.kwargs)

    def build(self, minimized: bool = False, maximized: bool = False, **kwargs) -> Self:
        """	 Shows the main viewport.

        Args:
            minimized (bool, optional): Sets the state of the viewport to minimized
            maximized (bool, optional): Sets the state of the viewport to maximized
        Returns:
            Self: own instance.
        """
        super().build(None)
        dpg.setup_dearpygui()
        dpg.show_viewport(minimized=minimized, maximized=maximized)
        dpg.start_dearpygui()

        return self

    def __del__(self):
        """ Destroy the viewport.
        """
        dpg.destroy_context()
