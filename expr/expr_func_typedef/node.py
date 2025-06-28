"""
Node manipulation functions for XPath expressions in AUTOSAR XML.
"""

from typing import Optional, List, Any, Union

class Node:
    """Class containing node manipulation functions."""

    @staticmethod
    def exists(path: Optional[str] = None) -> bool:
        """
        Check if a specified node exists in the configuration.

        Args:
            path: Optional path to the node to check. If None, checks current node.

        Returns:
            bool: True if the node exists, False otherwise.
        """
        pass

    @staticmethod
    def value(node: Optional[Any] = None) -> Optional[str]:
        """
        Retrieve the value of a node.

        Args:
            node: Optional node to get value from. If None, uses current node.

        Returns:
            str: The value of the node, or None if node doesn't exist.
        """
        pass

    @staticmethod
    def current() -> Any:
        """
        Reference the current context node in the configuration.

        Returns:
            Any: The current context node.
        """
        pass

    @staticmethod
    def ref(path: str) -> Optional[Any]:
        """
        Retrieve a single referenced node based on a specified path.

        Args:
            path: ASPath to the referenced node.

        Returns:
            Any: The referenced node, or None if not found.
        """
        pass

    @staticmethod
    def refs(path: str) -> List[Any]:
        """
        Retrieve multiple referenced nodes based on a specified path.

        Args:
            path: ASPath to the referenced nodes.

        Returns:
            List[Any]: List of referenced nodes.
        """
        pass

    @staticmethod
    def refvalid(node: Any) -> bool:
        """
        Validate if a node reference is valid.

        Args:
            node: The node containing the reference to validate.

        Returns:
            bool: True if reference is valid, False otherwise.
        """
        pass

    @staticmethod
    def contains(node: Any, value: str) -> bool:
        """
        Check if a node contains a specific value.

        Args:
            node: The node to check.
            value: The value to look for.

        Returns:
            bool: True if node contains the value, False otherwise.
        """
        pass

    @staticmethod
    def containsValue(node: Any, value: str) -> bool:
        """
        Check if a node contains a specific value (alternative version).

        Args:
            node: The node to check.
            value: The value to look for.

        Returns:
            bool: True if node contains the value, False otherwise.
        """
        pass

    @staticmethod
    def empty(node: Optional[Any] = None) -> bool:
        """
        Check if a node is empty.

        Args:
            node: Optional node to check. If None, uses current node.

        Returns:
            bool: True if the node is empty, False otherwise.
        """
        pass

    @staticmethod
    def fallback(primary: Optional[str], fallback: str) -> str:
        """
        Provide a fallback value if the primary value is not available.

        Args:
            primary: The primary value to try.
            fallback: The fallback value to use if primary is not available.

        Returns:
            str: Either the primary value or fallback value.
        """
        return primary if primary is not None else fallback

    @staticmethod
    def filter(node: Any, condition: str) -> List[Any]:
        """
        Filter nodes based on a condition.

        Args:
            node: The node to filter.
            condition: The condition to filter by.

        Returns:
            List[Any]: List of nodes that match the condition.
        """
        pass

    @staticmethod
    def islast(node: Any) -> bool:
        """
        Check if a node is the last one in its context.

        Args:
            node: The node to check.

        Returns:
            bool: True if the node is last, False otherwise.
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
    def paths(node: Any) -> List[str]:
        """
        Get all paths associated with a node.

        Args:
            node: The node to get paths from.

        Returns:
            List[str]: List of paths.
        """
        pass

    @staticmethod
    def refexists(node: Any) -> bool:
        """
        Check if a reference exists.

        Args:
            node: The node containing the reference to check.

        Returns:
            bool: True if reference exists, False otherwise.
        """
        pass

    @staticmethod
    def when(node: Any, condition: str) -> bool:
        """
        Evaluate a condition on a node.

        Args:
            node: The node to evaluate.
            condition: The condition to evaluate.

        Returns:
            bool: Result of the condition evaluation.
        """
        pass
