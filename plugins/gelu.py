from leanpass_plugins import PluginInfo, op
import numpy as np

info = PluginInfo(
    name="gelu",
    author="Test Contributor",
    github_username="testcontrib",
    description="Gaussian Error Linear Unit activation function."
)

@op(info.name)
def gelu_forward(x):
    # Standard GELU approximation
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * np.power(x, 3))))

