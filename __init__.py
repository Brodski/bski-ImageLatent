from typing_extensions import override
from comfy_api.latest import ComfyExtension, io
from .bskinodes import BskiNode
from .bskiconditioning import BskiVideoSmooth


NODE_CLASS_MAPPINGS = {
    "BskiNode": BskiNode,
    "BskiVideoSmooth": BskiVideoSmooth,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BskiNode": "Bskis first node does cool stuff",
    "BskiVideoSmooth": "Bski Video Smooth :)",
}


class BskiExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [BskiNode, BskiVideoSmooth]


async def comfy_entrypoint() -> BskiExtension:
    return BskiExtension()

