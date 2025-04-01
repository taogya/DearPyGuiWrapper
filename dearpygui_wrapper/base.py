import logging
from typing import Any, Iterator, Self

from dearpygui_wrapper import DpgTag, dpg_org

logger = logging.getLogger('dgp_wrapper')


def get_tag(id: DpgTag) -> DpgTag:
    """ Get tag of the object.

    Args:
        id (DpgTag): id of the object.

    Returns:
        DpgTag: tag of the object.
    """
    return dpg_org.get_item_alias(id) or id


class Object:
    is_instance = False
    generator: staticmethod

    def __init__(self, *args, **kwargs):
        """ Abstract class for DearPyGui object.

        Raises:
            TypeError: If the class is not instance.
        """
        if not self.is_instance:
            raise TypeError(f'Cannot instantiate abstract class {self.__class__.__name__}')
        self.args = args
        self.kwargs = kwargs
        self.__is_build = False

    def __del__(self):
        """ Destructor for the object.
        """
        try:
            self.delete()
        except KeyError:
            pass

    def __str__(self) -> str:
        if hasattr(self, 'tag'):
            return f'<{self.id}: {self.tag}>'
        else:
            return f'{self.__class__.__name__} (not build yet)'

    def delete(self, *args, **kwargs):
        """ Delete the object.
        """
        try:
            dpg_org.delete_item(self.tag)
        except SystemError:
            pass
        except Exception:
            logger.exception(f'[{self.__class__.__name__}] Failed to delete {self}')
        logger.debug(f'[{self.__class__.__name__}] Deleted {self}')

    def default_tag(self) -> DpgTag:
        return f'{self.__class__.__name__}##{self.id}'

    def build(self, parent: 'Object | None' = None, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (Object | None, optional): parent object. Defaults to None.

        Returns:
            Self: own instance.
        """
        if self.__is_build:
            return self
        self.__is_build = True

        self.parent = None
        if self.kwargs.get('parent') is not None and isinstance(parent, Object):
            self.parent = parent
            self.kwargs.update({'parent': parent.tag})

        tag = self.kwargs.pop('tag', 0)
        self.id = self.generator(*self.args, **self.kwargs)
        if tag == 0:
            tag = self.default_tag()
        self.tag = tag
        dpg_org.add_alias(self.tag, self.id)

        logger.debug(f'[{self.__class__.__name__}] Built {self} in {parent}')
        return self

    def print(self, print_func=print):
        """ Print the object.
        """
        print_func(f'own={self}, parent={self.parent}')


class ValueObject(Object):

    def conv_to_value(self, values: list[Any]) -> Any:
        """ Convert values to a single value.

        Args:
            values (list[Any]): values to convert.

        Returns:
            Any: converted value.
        """
        raise NotImplementedError(f'{self.__class__.__name__} does not implement conv_to_value()')

    def set_values(self, values: list[Any], call_callback: bool = True) -> Self:
        """ Set value of the object.

        Args:
            values (list[Any]): value to set.
            call_callback (bool, optional): call callback. Defaults to True.
        """
        value = self.conv_to_value(values)
        self.value = value
        logger.debug(f'[{self.__class__.__name__}] Set value of {self} to {value}')

        if call_callback:
            callback = dpg_org.get_item_callback(self.tag)
            userdata = dpg_org.get_item_user_data(self.tag)
            if callback:
                callback(self.tag, value, userdata)
                logger.debug(f'[{self.__class__.__name__}] Called callback of {self} with {value}')

        return self

    @property
    def value(self) -> Any:
        """ Get value of the object.

        Returns:
            Any: value of the object.
        """
        return dpg_org.get_value(self.tag)

    @value.setter
    def value(self, value: Any):
        """ Set value of the object.

        Args:
            value (Any): value to set.
        """
        dpg_org.set_value(self.tag, value)


class Container(Object):
    def __init__(self, *args, **kwargs):
        """ Abstract class for DearPyGui container object.
        """
        super().__init__(*args, **kwargs)
        self.__objects: dict[DpgTag, Object] = {}
        self.__not_build_objects: list[Object] = []

    def __getitem__(self, key: DpgTag) -> Object:
        """ Get object by tag.

        Args:
            key (DpgTag): tag of the object.

        Returns:
            Object: object with the tag.
        """
        return self.__objects[key]

    def __setitem__(self, key: DpgTag, value: Object):
        """ Set object by tag.

        Args:
            key (DpgTag): tag of the object.
            value (Object): object to set.
        """
        self.__objects[key] = value
        if isinstance(value, Container):
            for _, o in value:
                self.__objects[o.tag] = o

    def __delitem__(self, key: DpgTag):
        """ Delete object by tag.

        Args:
            key (DpgTag): tag of the object.
        """
        obj = self.__objects[key]
        if isinstance(obj, Container):
            for _, o in obj:
                del self.__objects[o.tag]
        del self.__objects[key]

    def __iter__(self) -> Iterator[tuple[DpgTag, Object]]:
        """ Iterate over the objects in the container.
        """
        return iter(self.__objects.items())

    def __bool__(self):
        return len(self.__objects) > 0

    def delete(self, *args, **kwargs):
        """ Delete the container.
        """
        for obj in self.__objects.values():
            obj.delete(*args, **kwargs)
        super().delete(*args, **kwargs)

    def add(self, obj: Object, *args, **kwargs) -> Self:
        """ Add object to the container.

        Args:
            obj (Object): object to add.

        Returns:
            Self: own instance.
        """
        if not hasattr(obj, 'tag'):
            self.__not_build_objects.append(obj)
        else:
            self[obj.tag] = obj

        logger.debug(f'[{self.__class__.__name__}] Added {obj}')
        return self

    def remove(self, obj: Object, *args, **kwargs) -> Self:
        """ Remove object from the container.

        Args:
            obj (Object): object to remove.

        Returns:
            Self: own instance.
        """
        del self[obj.tag]
        return self

    def build(self, parent: Object | None = None, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (Object | None, optional): parent object. Defaults to None.

        Returns:
            Self: own instance.
        """
        super().build(parent=parent, **kwargs)
        for obj in self.__not_build_objects:
            obj.build(parent=self, **kwargs)
            self[obj.tag] = obj
        self.__not_build_objects.clear()

        return self
