# from .libs.utils import ByPassTypeTuple, empty_pil_tensor, empty_latent
from comfy_api.latest import io
import torch
import node_helpers
import comfy
import comfy.utils
import comfy.clip_vision
import comfy.latent_formats
import logging



# author: Trung0246 --->
class TautologyStr(str):
    def __ne__(self, other):
        return False

class ByPassTypeTuple(tuple):
    def __getitem__(self, index):
        if index > 0:
            index = 0
        item = super().__getitem__(index)
        if isinstance(item, str):
            return TautologyStr(item)
        return item

# class MaskBatchSplitter:
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "masks":       ("MASK",),
#                 "split_count": ("INT", {"default": 4, "min": 0, "max": 50, "step": 1}),
#             }
#         }

#     RETURN_TYPES = ByPassTypeTuple(("MASK",))
#     FUNCTION     = "doit"
#     CATEGORY     = "InspirePack/Util"
#     # category="conditioning/video_models"

#     def doit(self, masks, split_count):
#         cnt = min(split_count, len(masks))
#         res = [mask.unsqueeze(0) for mask in masks[:cnt]]

#         if split_count >= len(masks):
#             lack_cnt = split_count - cnt + 1
#             empty_mask = torch.zeros((1, masks.shape[1], masks.shape[2]), dtype=masks.dtype)
#             res.extend([empty_mask] * lack_cnt)
#         else:
#             res.append(masks[cnt:])  # remaining as sub-batch

#         return tuple(res)
    

# export function register_splitter(node, app) {
# 	if(node.comfyClass === 'ImageBatchSplitter //Inspire' || node.comfyClass === 'LatentBatchSplitter //Inspire' || node.comfyClass === 'MaskBatchSplitter //Inspire') {
# 		let split_count = node.widgets[0];

# 		let output_name = 'output';
# 		let output_type = "*";

# 		if(node.comfyClass === 'ImageBatchSplitter //Inspire') {
# 			output_name = 'image';
# 			output_type = "IMAGE";
# 		}
# 		else if(node.comfyClass === 'LatentBatchSplitter //Inspire') {
# 			output_name = 'latent';
# 			output_type = "LATENT";
# 		}
# 		else if(node.comfyClass === 'MaskBatchSplitter //Inspire') {
# 			output_name = 'mask';
# 			output_type = "MASK";
# 		}

# 		ensure_splitter_outputs(node, output_name, split_count.value, output_type);

# 		Object.defineProperty(split_count, "value", {
# 			set: async function(value) {
# 				if(value < 0 || value > 50)
# 					return;

# 				ensure_splitter_outputs(node, output_name, value, output_type);
# 			},
# 			get: function() {
# 				return node.outputs.length - 1;
# 			}
# 		});
# 	}
# }