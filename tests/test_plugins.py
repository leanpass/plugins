import os
import glob
import pytest
import importlib.util
import numpy as np
import sys

# Assuming test is run from root or tests dir
plugins_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'plugins'))
plugin_files = [f for f in glob.glob(os.path.join(plugins_dir, '*.py')) 
                if not os.path.basename(f).startswith('_') and not os.path.basename(f) == '__init__.py']

@pytest.mark.parametrize("plugin_file", plugin_files)
def test_plugin_loads_and_registers(plugin_file):
    basename = os.path.basename(plugin_file)
    module_name = f"plugins_test.{basename[:-3]}"
    
    spec = importlib.util.spec_from_file_location(module_name, plugin_file)
    assert spec is not None and spec.loader is not None, f"Failed to load spec for {basename}"
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    # Check if info exists
    assert hasattr(module, 'info'), f"{basename} is missing the 'info' PluginInfo object"
    
    info = module.info
    assert hasattr(info, 'name'), "PluginInfo missing 'name'"
    assert hasattr(info, 'author'), "PluginInfo missing 'author'"
    assert hasattr(info, 'github_username'), "PluginInfo missing 'github_username'"
    assert hasattr(info, 'description'), "PluginInfo missing 'description'"
    
    # Check if the op was registered in the real registry
    try:
        from leanpass.plugin_registry import _REGISTRY
    except ImportError:
        from leanpass_plugins import _REGISTRY
    assert info.name in _REGISTRY, f"Op '{info.name}' was not registered in _REGISTRY"

