from pathlib import Path
import sys

_current_dir = Path(__file__).parent
_models_dir = _current_dir / "models"
for _p in [_current_dir, _models_dir]:
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from typing_extensions import override
from comfy_api.latest import ComfyExtension, io
from .bskinodes import BskiAppendAnyToList
from .bskiconditioning import BskiVideoSmooth
from .bski_first_last import BskiFirstLast
# from .bskiUtils import MaskBatchSplitter
from .bski_KJbox2Comfy import Bski_KJBboxToComfyBBox
from .bski_mask_grow_plus import BskiMaskGrowPlus
from .bskinodes import BskiImageListToImageBatch
from .bskinodes import BskiRemove1stImageOfBatch
from .bski_sam3 import BskiSAM3Segment
from .bski_depth_measure import BskiDepthMeasure
from .bski_lazy_sort import BskiLazySort
from .bski_preview_any import BskiPreviewAny

NODE_CLASS_MAPPINGS = {
    "BskiAppendAnyToList": BskiAppendAnyToList,
    "BskiVideoSmooth": BskiVideoSmooth,
    "BskiFirstLast": BskiFirstLast,
    "Bski_KJBboxToComfyBBox": Bski_KJBboxToComfyBBox,
    "BskiMaskGrowPlus": BskiMaskGrowPlus,
    "BskiImageListToImageBatch": BskiImageListToImageBatch,
    "BskiRemove1stImageOfBatch": BskiRemove1stImageOfBatch,
    "BskiSAM3Segment" : BskiSAM3Segment,
    "BskiDepthMeasure": BskiDepthMeasure,
    "BskiLazySort": BskiLazySort,
    "BskiPreviewAny": BskiPreviewAny
    # "MaskBatchSplitter //Inspire": MaskBatchSplitter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BskiAppendAnyToList": "Bski Append Any To List",
    "BskiVideoSmooth": "Bski Video Smooth :)",
    "BskiFirstLast": "first last super cool",
    "MaskBatchSplitter //Inspire": "bski's MaskBatchSplitter",
    "Bski_KJBboxToComfyBBox": "KJ Bbox To Comfy BBox, bski",
    "BskiMaskGrowPlus": "Bski Grow Mask+",
    "BskiImageListToImageBatch": "Bski image list to image batch, i guess",
    "BskiRemove1stImageOfBatch": "Bski Remove 1st Entry",
    "BskiSAM3Segment": "bski SAM3 Segment",
    "BskiLazySort": "Bski Lazy Sort"
}


class BskiExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [BskiAppendAnyToList, BskiVideoSmooth, BskiFirstLast, Bski_KJBboxToComfyBBox, BskiMaskGrowPlus, BskiImageListToImageBatch, BskiRemove1stImageOfBatch, BskiSAM3Segment, BskiDepthMeasure, BskiLazySort, BskiPreviewAny]

async def comfy_entrypoint() -> BskiExtension:
    return BskiExtension()

