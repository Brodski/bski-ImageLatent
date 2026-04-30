import logging
from typing import List
from comfy_api.latest import io
import torch
import comfy
import sys
import nodes
import re


class BskiAppendAnyToList(io.ComfyNode):
    """
    Input A must be a list.
    Input B can be any datatype.
    Appends B onto A, then returns all outputs.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="BskiAppendAnyToList",
            display_name="Bski Append Any To List",
            category="utils/list",
            inputs=[
                io.Custom("*").Input("list_a"),
                io.Custom("*").Input("anything"),
            ],
            outputs=[
                io.Image.Output("IMAGE", is_output_list=True),
                io.String.Output("STRING", is_output_list=True),
                io.Int.Output("INT", is_output_list=True),
                io.Float.Output("FLOAT", is_output_list=True),
                io.Conditioning.Output("CONDITIONING", is_output_list=True),
                io.Latent.Output("LATENT", is_output_list=True),
                io.Custom("*").Output("ANY", is_output_list=True),
            ],
        )

    @classmethod
    def execute(cls, list_a: List, anything) -> io.NodeOutput:
        logging.info("BSKI APPEND NODE EXECUTE")

        if not isinstance(list_a, list):
            list_a = [list_a]

        logging.info("type: " + str(type(anything)))
        logging.info("class: " + str(anything.__class__.__name__))

        list_a.append(anything)

        # cheeky code to prevent duplicates, b/c re-running the workflow sometimes double stacks the list. (pray no bugs)
        list_a = cls._deduplicate(list_a)

        # yes, double brackets are needed because of the OUTPUT_IS_LIST... ¯\_(ツ)_/¯
        # shoutout to Crystools https://github.com/crystian/ComfyUI-Crystools/blob/main/nodes/list.py#L86
        merged = [list_a]
        # first_item = merged[0] if merged else None

        return io.NodeOutput(
            merged,   # IMAGE
            merged,   # STRING
            merged,   # INT
            merged,   # FLOAT
            merged,   # CONDITIONING
            merged,   # LATENT
            merged    # ANY
        )
    
    @staticmethod
    def _deduplicate(items: List) -> List:
        unique = []
        for candidate in items:
            is_dup = False
            for seen in unique:
                try:
                    # Tensor comparison
                    if isinstance(candidate, torch.Tensor) and isinstance(seen, torch.Tensor):
                        if torch.equal(candidate, seen):
                            is_dup = True
                            break
                    # Fallback for hashable / comparable types
                    elif candidate == seen:
                        is_dup = True
                        break
                except Exception:
                    pass  # If comparison fails, treat as non-duplicate
            if not is_dup:
                unique.append(candidate)
        return unique
    
class BskiRemove1stImageOfBatch(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="BskiRemove1stImage",
            display_name="bski remove 1st image",
            description="shiiiiiiiiiit",
            category="image/batch",
            inputs=[
                io.Image.Input("IMAGE", tooltip=""),
            ],
            outputs=[
                io.Image.Output("IMAGE"),
            ],
        )

    @classmethod
    def execute(cls, images) -> io.NodeOutput:
        batch_cut = images[1:]
        return io.NodeOutput(batch_cut)
    









    
class BskiImageListToImageBatch(io.ComfyNode):
    #special unwrap b/c comfyui is w/e
    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="BskiImageListToImageBatch",
            display_name="Bski 'Image List' to Batch",
            description="comfyUI is doing some nutty shit, custom node just to unwrap lists, which aren't actually list b/c comfyUI fucking around with it",
            category="utils/list",
            inputs=[
                io.Image.Input("images", tooltip=""),
            ],
            outputs=[
                io.Image.Output("IMAGE"),  # remove is_output_list=True
            ],
        )

    # claude
    @classmethod
    def execute(cls, images) -> io.NodeOutput:

        # Normalize whatever ComfyUI throws at us into a flat list of tensors
        def flatten(x):
            if isinstance(x, torch.Tensor):
                # Could be [B,H,W,C] — split into list of per-batch tensors
                return [x[i:i+1] for i in range(x.shape[0])] if x.dim() == 4 else [x]
            elif isinstance(x, list):
                result = []
                for item in x:
                    result.extend(flatten(item))
                return result
            else:
                raise TypeError(f"Unexpected type in images: {type(x)}")

        flat = flatten(images)

        if not flat:
            raise ValueError("No tensors found in images input")

        shape = flat[0].shape[1:3]  # [H, W]
        out = []

        for img in flat:
            if img.shape[1:3] != shape:
                img = comfy.utils.common_upscale(
                    img.permute([0, 3, 1, 2]),
                    shape[1], shape[0],
                    upscale_method='bicubic',
                    crop='center'
                ).permute([0, 2, 3, 1])
            out.append(img)

        return io.NodeOutput(torch.cat(out, dim=0))

    # @classmethod
    # def execute(cls, images: List) -> io.NodeOutput:
    #     image_actually = None
    #     if isinstance(images, list) and len(images) == 1:
    #         try:
    #             if images[0][0] and isinstance(images[0][0], list):
    #                 image_actually = images[0]
    #         except:
    #             print("oops idk bro")
    #     else:
    #         image_actually = images

    #     shape = image_actually[0].shape[1:3]
    #     out = []

    #     for i in range(len(image_actually)):
    #         img = image_actually[i]
    #         if image_actually[i].shape[1:3] != shape:
    #             img = comfy.utils.common_upscale(img.permute([0,3,1,2]), shape[1], shape[0], upscale_method='bicubic', crop='center').permute([0,2,3,1])
    #         out.append(img)

    #     out = torch.cat(out, dim=0)

    #     return io.NodeOutput(out)  # was: return out
    























        # if len(image_actually) == 0:
        #     return ()
        # if len(image_actually) == 1:
        #     img = image_actually[0]
        #     if img.ndim == 3:  # add batch dim if missing
        #         img = img.unsqueeze(0)
        #     return (img,)

        # # Start with the first image
        # image1 = image_actually[0]
        # if image1.ndim == 3:
        #     image1 = image1.unsqueeze(0)

        # for image2 in image_actually[1:]:
        #     # Ensure batch dim
        #     if image2.ndim == 3:
        #         image2 = image2.unsqueeze(0)

        #     # Ensure same device
        #     if image2.device != image1.device:
        #         image2 = image2.to(image1.device)

        #     # Ensure HxW match exactly
        #     H, W = image1.shape[1], image1.shape[2]
        #     if image2.shape[1] != H or image2.shape[2] != W:
        #         image2 = comfy.utils.common_upscale(
        #             image2.movedim(-1, 1),  # move channels first
        #             W,  # width
        #             H,  # height
        #             "lanczos",
        #             "center"
        #         ).movedim(1, -1)  # move channels back last

        #     # Ensure channels match
        #     if image2.shape[3] != image1.shape[3]:
        #         # simple fix: truncate or pad channels
        #         min_C = min(image1.shape[3], image2.shape[3])
        #         image1 = image1[:, :, :, :min_C]
        #         image2 = image2[:, :, :, :min_C]

        #     # Concatenate along batch dimension
        #     image1 = torch.cat((image1, image2), dim=0)

        # return (image1,)



    #@classmethod
    #def fingerprint_inputs(s, image, string_field, int_field, float_field, print_to_screen):
    #    return ""

    # @classmethod
    # def check_lazy_status(cls, image, string_field, int_field, float_field, print_to_screen):
    #     """
    #         Return a list of input names that need to be evaluated.

    #         This function will be called if there are any lazy inputs which have not yet been
    #         evaluated. As long as you return at least one field which has not yet been evaluated
    #         (and more exist), this function will be called again once the value of the requested
    #         field is available.

    #         Any evaluated inputs will be passed as arguments to this function. Any unevaluated
    #         inputs will have the value None.
    #     """
    #     if print_to_screen == "enable":
    #         return ["int_field", "float_field", "string_field"]
    #     else:
    #         return []

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"


# Add custom API routes, using router
# from aiohttp import web
# from server import PromptServer

# @PromptServer.instance.routes.get("/hello")
# async def get_hello(request):
#     return web.json_response("hello")


