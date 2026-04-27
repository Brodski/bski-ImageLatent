from typing_extensions import override
from comfy_api.latest import ComfyExtension, io
from .bskinodes import BskiNode
from .bskiconditioning import BskiVideoSmooth
from .bski_first_last import BskiFirstLast
# from .bskiUtils import MaskBatchSplitter
from .bski_KJbox2Comfy import Bski_KJBboxToComfyBBox


NODE_CLASS_MAPPINGS = {
    "BskiNode": BskiNode,
    "BskiVideoSmooth": BskiVideoSmooth,
    "BskiFirstLast": BskiFirstLast,
    "Bski_KJBboxToComfyBBox": Bski_KJBboxToComfyBBox
    # "MaskBatchSplitter //Inspire": MaskBatchSplitter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BskiNode": "Bskis first node does cool stuff",
    "BskiVideoSmooth": "Bski Video Smooth :)",
    "BskiFirstLast": "first last super cool",
    "MaskBatchSplitter //Inspire": "bski's MaskBatchSplitter",
    "Bski_KJBboxToComfyBBox": "KJ Bbox To Comfy BBox, bski"
}


class BskiExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [BskiNode, BskiVideoSmooth, BskiFirstLast, Bski_KJBboxToComfyBBox]

async def comfy_entrypoint() -> BskiExtension:
    return BskiExtension()

