from leanpass_plugins import PluginInfo, op
import numpy as np

info = PluginInfo(
    name="mish",
    author="Test Contributor",
    github_username="testcontrib",
    description="Mish activation function: x * tanh(softplus(x))."
)

@op(info.name)
def mish_forward(x):
    # Mish: x * tanh(ln(1 + e^x))
    # np.log1p(np.exp(x)) is a numerically stable softplus
    softplus_x = np.log1p(np.exp(x))
    return x * np.tanh(softplus_x)

