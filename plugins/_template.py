from leanpass_plugins import PluginInfo, op
import numpy as np

# 1. Fill out your plugin info
info = PluginInfo(
    name="my_op",
    author="Your Name",
    github_username="yourusername",
    description="A brief description of what this op does."
)

# 2. Implement your forward and backward passes
# Use the @op decorator to register your function
@op(info.name)
def my_op_forward(x):
    # Implement forward pass using numpy
    return np.maximum(0, x)

# thats it, just open a PR and wait for the CI to merge it!
