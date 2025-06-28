"""
Numeric functions for XPath expressions in AUTOSAR XML.
"""

from typing import Optional, List, Any, Tuple, Union

class Num:
    """Class containing numeric functions."""

    @staticmethod
    def dectoint(value: str) -> int:
        """
        Convert decimal string to integer.

        Args:
            value: Decimal string to convert.

        Returns:
            int: The converted integer value.
        """
        pass

    @staticmethod
    def f(value: Union[str, float]) -> float:
        """
        Convert value to float.

        Args:
            value: Value to convert to float.

        Returns:
            float: The converted float value.
        """
        pass

    @staticmethod
    def hextoint(value: str) -> int:
        """
        Convert hexadecimal string to integer.

        Args:
            value: Hexadecimal string to convert.

        Returns:
            int: The converted integer value.
        """
        pass

    @staticmethod
    def i(value: Union[str, int, float]) -> int:
        """
        Convert value to integer.

        Args:
            value: Value to convert to integer.

        Returns:
            int: The converted integer value.
        """
        pass

    @staticmethod
    def integer(value: Union[str, float]) -> int:
        """
        Convert value to integer (alternative version).

        Args:
            value: Value to convert to integer.

        Returns:
            int: The converted integer value.
        """
        pass

    @staticmethod
    def min(values: List[Union[int, float]]) -> Union[int, float]:
        """
        Get minimum value from a list of numbers.

        Args:
            values: List of numbers to find minimum from.

        Returns:
            Union[int, float]: The minimum value.
        """
        pass

    @staticmethod
    def count(node_set: List[Any]) -> int:
        """
        Count the number of nodes in a node-set.

        Args:
            node_set: List of nodes to count.

        Returns:
            int: The number of nodes in the set.
        """
        pass
