import logging
from typing import Any, Self

from dearpygui_wrapper import DpgTag, dpg

logger = logging.getLogger('dgp_wrapper')


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

    def build(self, parent: 'Object | None', *args, manager: dict[DpgTag, 'Object'] | None = None, **kwargs) -> Self:
        """ Build the object.

        Args:
            parent (Object | None): parent object.
            manager (dict[DpgTag, Object] | None, optional): tag manager. Defaults to None.

        Raises:
            ValueError: If the object is already built.

        Returns:
            Self: own instance.
        """
        if self.__is_build:
            raise ValueError(f'{self.__class__.__name__} is already built.')
        self.__is_build = True

        self.parent = parent
        if parent is not None:
            self.kwargs.update({'parent': parent.tag})

        self.tag = self.generator(*self.args, **self.kwargs)
        if manager is not None:
            manager.update({self.tag: self})

        return self


class ValueObject(Object):
    @property
    def value(self) -> Any:
        """ Get value of the object.

        Returns:
            Any: value of the object.
        """
        return dpg.get_value(self.tag)

    @value.setter
    def value(self, value: Any):
        """ Set value of the object.

        Args:
            value (Any): value to set.
        """
        dpg.set_value(self.tag, value)

    def set_values(self, values: list[Any]):
        """ Set value of the object.

        Args:
            values (list[Any]): value to set.
        """
        raise NotImplementedError


class Container(Object):
    def __init__(self, *args, **kwargs):
        """ Abstract class for DearPyGui container object.
        """
        super().__init__(*args, **kwargs)
        self.objects: list[Object] = []

    def add(self, obj: Object, manager: dict[DpgTag, Object] | None = None) -> Self:
        """ Add object to the container.

        Args:
            obj (Object): object to add.
            manager (dict[DpgTag, Object] | None, optional): tag manager. Defaults to None.

        Returns:
            Self: own instance.
        """
        self.objects.append(obj)
        if manager is not None:
            manager[obj.tag] = self

        return self

    def remove(self, obj: Object, manager: dict[DpgTag, Object] | None = None) -> Self:
        """ Remove object from the container.

        Args:
            obj (Object): object to remove.
            manager (dict[DpgTag, Object] | None, optional): tag manager. Defaults to None.

        Returns:
            Self: own instance.
        """
        self.objects.remove(obj)
        if manager is not None:
            del manager[obj.tag]

        return self

    def build(self, parent: Object | None, *args, **kwargs) -> Self:
        """ Build the container.

        Args:
            parent (Object): parent object.

        Returns:
            Self: own instance.
        """
        super().build(parent, *args, **kwargs)
        for obj in self.objects:
            obj.build(self, *args, **kwargs)

        return self


class Manager(Container):
    def __init__(self, *args, **kwargs):
        """ Manager class for DearPyGui object.
        """
        super().__init__(*args, **kwargs)
        self.manager: dict[DpgTag, Object] = {}

    def build(self, parent: Object | None, *args, **kwargs) -> Self:
        super().build(parent, *args, manager=self.manager, **kwargs)

        return self
