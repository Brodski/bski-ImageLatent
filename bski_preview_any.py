
import json
from comfy_api.latest import io

# Preview Any - original implement from
# https://github.com/rgthree/rgthree-comfy/blob/main/py/display_any.py
# upstream requested in https://github.com/Kosinkadink/rfcs/blob/main/rfcs/0000-corenodes.md#preview-nodes
#
# For some reason, current offical Preview Any node by comfyUI no longer returns the string. They took out the feature or they forgot to test their code
#
class BskiPreviewAny(io.ComfyNode):

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="BskiPreviewAny",
            display_name="Bski Preview As Text",
            category="utils",
            is_output_node=True,
            inputs=[
                io.Custom("*").Input("source"),
            ],
            outputs=[
                io.String.Output(display_name="text"),
            ],
        )

    @classmethod
    def execute(cls, source=None) -> io.NodeOutput:
        value = 'None'
        if isinstance(source, str):
            value = source
        elif isinstance(source, (int, float, bool)):
            value = str(source)
        elif source is not None:
            try:
                value = json.dumps(source, indent=4)
            except Exception:
                try:
                    value = str(source)
                except Exception:
                    value = 'source exists, but could not be serialized.'

        return {"ui": {"text": (value,)}, "result": (value,)}
