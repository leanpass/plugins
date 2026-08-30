# LeanPass Plugins

A central repository for community-contributed plugins for LeanPass.

## How to Contribute a Plugin in < 5 Minutes

1. **Fork** this repository.
2. **Copy** the template:
   ```bash
   cp plugins/_template.py plugins/your_op_name.py
   ```
3. **Fill in** the `PluginInfo` at the top of your new file with your details.
4. **Implement** your operation using LeanPass and NumPy, and decorate it with `@op(info.name)`.
5. **Open a Pull Request**. Our CI will automatically test that your plugin loads successfully. Once merged, you will automatically appear in the Credits Table below!

*Note for LeanPass core maintainers: LeanPass core needs a small `plugin_registry.py` added to support the `@op` registration API used here.*

## Credits / Plugin Registry

<!-- REGISTRY_START -->
| Plugin | Author | Description |
|---|---|---|
| `mish` | [Test Contributor](https://github.com/testcontrib) | Mish activation function: x * tanh(softplus(x)). |

<!-- REGISTRY_END -->

