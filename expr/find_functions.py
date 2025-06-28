#!/usr/bin/env python3
"""
Script to find and extract unique function calls from XDM files.
Only searches within expr="..." attributes.
Usage: python find_functions.py [config_file]

If config_file is not provided, defaults to 'find_functions_config.yaml'
"""

import re
import sys
from pathlib import Path
from typing import Set, List, Dict, Tuple
import yaml
from collections import defaultdict

DEFAULT_CONFIG = "find_functions_config.yaml"

def extract_functions(content: str) -> Tuple[Set[str], Set[str]]:
    """
    Extract all unique function calls from expr attributes in the content.
    
    Args:
        content: The content to search in
        
    Returns:
        Tuple containing:
            - Set of prefixed function names (like node:xxx, text:xxx)
            - Set of unprefixed function names (like count, position)
    """
    # First find all expr="..." attributes
    expr_pattern = r'expr="([^"]*)"'
    expr_matches = re.findall(expr_pattern, content)
    
    prefixed_functions = set()
    unprefixed_functions = set()
    
    for expr in expr_matches:
        # Find patterns like text:something(), node:something(), etc.
        prefixed_pattern = r'(?:text|node|num|ecu):[\w-]+\('
        prefixed_matches = re.findall(prefixed_pattern, expr)
        prefixed_functions.update(match.rstrip('(') for match in prefixed_matches)
        
        # Find unprefixed function calls - looking for word followed by ( that's not prefixed
        # Now includes hyphenated names like substring-after
        # Negative lookbehind ensures it's not preceded by :
        unprefixed_pattern = r'(?<![:.\w])\b([a-zA-Z_][\w-]*)\('
        unprefixed_matches = re.findall(unprefixed_pattern, expr)
        
        # Filter out common programming keywords and known non-functions
        ignored_words = {'if', 'for', 'while', 'switch', 'catch', 'function', 'and', 'or', 'not'}
        unprefixed_functions.update(match for match in unprefixed_matches 
                                  if match not in ignored_words)
    
    return prefixed_functions, unprefixed_functions

def get_sorted_functions(functions: Set[str]) -> List[str]:
    """
    Sort functions alphabetically.
    
    Args:
        functions: Set of function names
        
    Returns:
        Sorted list of function names
    """
    return sorted(list(functions))

def load_config(config_file: Path) -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        Dictionary containing configuration
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config file: {e}")
        sys.exit(1)

def process_files(config: dict) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Process all input files specified in config.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Tuple containing:
            - Dictionary mapping filenames to sets of prefixed functions
            - Dictionary mapping filenames to sets of unprefixed functions
    """
    prefixed_by_file = defaultdict(set)
    unprefixed_by_file = defaultdict(set)
    
    for file_path in config['input_files']:
        try:
            path = Path(file_path)
            if not path.exists():
                print(f"Warning: File {path} does not exist, skipping...")
                continue
                
            content = path.read_text(encoding='utf-8')
            prefixed, unprefixed = extract_functions(content)
            if prefixed or unprefixed:  # Only add file if it has functions
                prefixed_by_file[path.name] = prefixed
                unprefixed_by_file[path.name] = unprefixed
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue
            
    return prefixed_by_file, unprefixed_by_file

def format_function_list(functions: Set[str], by_file: Dict[str, Set[str]], show_files: bool) -> List[str]:
    """
    Format the function list for output.
    
    Args:
        functions: Set of all unique functions
        by_file: Dictionary mapping filenames to sets of functions
        show_files: Whether to show which files each function appears in
        
    Returns:
        List of formatted strings
    """
    lines = []
    sorted_funcs = get_sorted_functions(functions)
    
    for func in sorted_funcs:
        if show_files:
            # Find all files containing this function
            files = sorted([f for f, funcs in by_file.items() if func in funcs])
            files_str = ", ".join(files)
            lines.append(f"{func} (found in: {files_str})")
        else:
            lines.append(func)
            
    return lines

def output_results(prefixed_by_file: Dict[str, Set[str]], 
                  unprefixed_by_file: Dict[str, Set[str]], 
                  config: dict):
    """
    Output the results according to configuration.
    
    Args:
        prefixed_by_file: Dictionary mapping filenames to sets of prefixed functions
        unprefixed_by_file: Dictionary mapping filenames to sets of unprefixed functions
        config: Configuration dictionary
    """
    all_prefixed = set().union(*prefixed_by_file.values())
    all_unprefixed = set().union(*unprefixed_by_file.values())
    show_files = config['output'].get('show_file_sources', True)
    
    # Prepare output
    output_lines = []
    
    if all_prefixed:
        output_lines.append(f"\nFound {len(all_prefixed)} unique prefixed functions in expr attributes:")
        output_lines.extend(format_function_list(all_prefixed, prefixed_by_file, show_files))
    
    if all_unprefixed:
        if output_lines:  # Add blank line between sections if there are prefixed functions
            output_lines.append("")
        output_lines.append(f"\nFound {len(all_unprefixed)} unique unprefixed functions in expr attributes:")
        output_lines.extend(format_function_list(all_unprefixed, unprefixed_by_file, show_files))
    
    if not output_lines:
        output_lines.append("No functions found in expr attributes.")
    
    # Output the results
    print("\n".join(output_lines))
    
    # Save to file if configured
    if config['output'].get('save_to_file', False):
        output_file = config['output'].get('output_file', 'function_list.txt')
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(output_lines))
            print(f"\nResults saved to {output_file}")
        except Exception as e:
            print(f"Error saving to file: {e}")

def main():
    # Get config file path
    config_file = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CONFIG)
    if not config_file.exists():
        print(f"Error: Config file {config_file} does not exist")
        sys.exit(1)
    
    # Load configuration
    config = load_config(config_file)
    
    # Process files
    prefixed_by_file, unprefixed_by_file = process_files(config)
    
    # Output results
    output_results(prefixed_by_file, unprefixed_by_file, config)

if __name__ == '__main__':
    main()
