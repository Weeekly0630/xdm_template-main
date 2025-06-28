"""
Standard XPath functions without prefixes for AUTOSAR XML.
"""

from typing import List, Any, Union, Optional

class XPath:
    """Class containing standard XPath functions."""
    
    @staticmethod
    def count(node_set: List[Any]) -> int:
        """
        Count the number of nodes in a node set.

        Args:
            node_set: Set of nodes to count.

        Returns:
            int: The number of nodes.
        """
        pass

    @staticmethod
    def position() -> int:
        """
        Get the context position in the current node list.

        Returns:
            int: Current position (1-based index).
        """
        pass

    @staticmethod
    def last() -> int:
        """
        Get the size of the current node list.

        Returns:
            int: Size of the current node list.
        """
        pass

    @staticmethod
    def name(node: Optional[Any] = None) -> str:
        """
        Get the name of a node.

        Args:
            node: Optional node to get name from. If None, uses current node.

        Returns:
            str: The name of the node.
        """
        pass

    @staticmethod
    def string(value: Any) -> str:
        """
        Convert value to string.

        Args:
            value: Value to convert.

        Returns:
            str: String representation of the value.
        """
        pass

    @staticmethod
    def concat(*args: str) -> str:
        """
        Concatenate strings.

        Args:
            *args: Strings to concatenate.

        Returns:
            str: Concatenated string.
        """
        pass

    @staticmethod
    def contains(str1: str, str2: str) -> bool:
        """
        Check if str1 contains str2.

        Args:
            str1: String to search in.
            str2: String to search for.

        Returns:
            bool: True if str1 contains str2.
        """
        pass

    @staticmethod
    def substring(string: str, start: int, length: Optional[int] = None) -> str:
        """
        Extract substring from string.

        Args:
            string: String to extract from.
            start: Start position (1-based).
            length: Optional length of substring.

        Returns:
            str: The extracted substring.
        """
        pass

    @staticmethod
    def substring_before(string: str, substr: str) -> str:
        """
        Get substring before the first occurrence of substr.

        Args:
            string: String to extract from.
            substr: String to search for.

        Returns:
            str: Part of string before substr.
        """
        pass

    @staticmethod
    def substring_after(string: str, substr: str) -> str:
        """
        Get substring after the first occurrence of substr.

        Args:
            string: String to extract from.
            substr: String to search for.

        Returns:
            str: Part of string after substr.
        """
        pass

    @staticmethod
    def string_length(string: Optional[str] = None) -> int:
        """
        Get length of string.

        Args:
            string: Optional string to measure. If None, uses current node string value.

        Returns:
            int: Length of the string.
        """
        pass

    @staticmethod
    def normalize_space(string: Optional[str] = None) -> str:
        """
        Normalize whitespace in string.

        Args:
            string: Optional string to normalize. If None, uses current node string value.

        Returns:
            str: String with normalized whitespace.
        """
        pass

    @staticmethod
    def translate(string: str, from_str: str, to_str: str) -> str:
        """
        Replace characters in string.

        Args:
            string: String to transform.
            from_str: String containing characters to replace.
            to_str: String containing replacement characters.

        Returns:
            str: Transformed string.
        """
        pass

    @staticmethod
    def starts_with(str1: str, str2: str) -> bool:
        """
        Check if str1 starts with str2.

        Args:
            str1: String to check.
            str2: Prefix to look for.

        Returns:
            bool: True if str1 starts with str2.
        """
        pass

    @staticmethod
    def number(value: Any = None) -> float:
        """
        Convert value to number.

        Args:
            value: Optional value to convert. If None, uses current node.

        Returns:
            float: The numeric value.
        """
        pass

    @staticmethod
    def sum(node_set: List[Any]) -> float:
        """
        Sum the values in a node-set.

        Args:
            node_set: Set of nodes whose values to sum.

        Returns:
            float: Sum of the values.
        """
        pass
