import os
import glob
import json
import importlib.util
import re
import sys

import ast

def extract_plugin_info(file_path):
    basename = os.path.basename(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
            
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    # Look for `info = PluginInfo(...)`
                    if isinstance(target, ast.Name) and target.id == 'info':
                        if isinstance(node.value, ast.Call) and getattr(node.value.func, 'id', '') == 'PluginInfo':
                            info_dict = {}
                            for keyword in node.value.keywords:
                                # ast.Constant is used in Python 3.8+ for strings
                                if isinstance(keyword.value, ast.Constant):
                                    info_dict[keyword.arg] = keyword.value.value
                                # Fallback for older AST nodes if necessary
                                elif getattr(ast, 'Str', None) and isinstance(keyword.value, ast.Str):
                                    info_dict[keyword.arg] = keyword.value.s
                                    
                            return {
                                "name": info_dict.get("name", ""),
                                "author": info_dict.get("author", ""),
                                "github_username": info_dict.get("github_username", ""),
                                "description": info_dict.get("description", ""),
                                "file": basename
                            }
    except Exception as e:
        print(f"Error statically parsing info from {basename}: {e}")
    return None

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    plugins_dir = os.path.join(root_dir, 'plugins')
    plugin_files = glob.glob(os.path.join(plugins_dir, '*.py'))
    
    registry = []
    for file in plugin_files:
        basename = os.path.basename(file)
        if basename.startswith('_') or basename == '__init__.py':
            continue
        info = extract_plugin_info(file)
        if info:
            registry.append(info)
            
    # Sort alphabetically by name
    registry.sort(key=lambda x: x['name'])
    
    # Save registry.json
    with open(os.path.join(root_dir, 'registry.json'), 'w') as f:
        json.dump(registry, f, indent=2)
        
    # Update README.md
    readme_path = os.path.join(root_dir, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
            
        # Build table
        table = "| Plugin | Author | Description |\n|---|---|---|\n"
        for item in registry:
            github_link = f"[{item['author']}](https://github.com/{item['github_username']})"
            table += f"| `{item['name']}` | {github_link} | {item['description']} |\n"
            
        # Replace section
        pattern = r"(<!-- REGISTRY_START -->\n).*?(\n<!-- REGISTRY_END -->)"
        new_content = re.sub(pattern, rf"\g<1>{table}\g<2>", readme_content, flags=re.DOTALL)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
if __name__ == '__main__':
    main()

