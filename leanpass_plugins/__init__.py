import os
import glob
import warnings
from dataclasses import dataclass
from typing import Callable, Any

try:
    from leanpass.plugin_registry import register_op, op, _REGISTRY
except ImportError:
    warnings.warn("LeanPass core is not installed or missing plugin_registry.py. Plugins may not register correctly.")
    _REGISTRY = {}
    def register_op(name: str, fn: Callable): _REGISTRY[name] = fn
    def op(name: str):
        def decorator(fn):
            register_op(name, fn)
            return fn
        return decorator

@dataclass
class PluginInfo:
    name: str
    author: str
    github_username: str
    description: str

import importlib.util

def load_plugins():
    try:
        import plugins
        plugins_dir = os.path.dirname(plugins.__file__)
    except ImportError:
        # Fallback to local directory for development
        plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
        if not os.path.exists(plugins_dir):
            warnings.warn("Plugins directory not found.")
            return

    plugin_files = glob.glob(os.path.join(plugins_dir, '*.py'))
    for file in plugin_files:
        basename = os.path.basename(file)
        if basename.startswith('_') or basename == '__init__.py':
            continue
        
        module_name = f"plugins.{basename[:-3]}"
        
        try:
            spec = importlib.util.spec_from_file_location(module_name, file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
        except Exception as e:
            warnings.warn(f"Failed to load plugin {basename}: {e}")

load_plugins()

