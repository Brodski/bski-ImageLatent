from comfy_api.latest import io
import torch
import node_helpers
import comfy
import comfy.utils
import comfy.clip_vision
import comfy.latent_formats
import logging

# consider this code. it is my custom node for ComfyUI, it takes in a video, ie an array of images (eg 20 images) they are from a continuous recording/video of a sort. I want to generate a very similar video that uses all of those images/frames and we use a denoise strength (0-1) on every one of those images. kind of like how image to image would use, "0 = this image is known, and 1 = this image is unknown/all-noise .  It purpose is to smooth out the video
class BskiVideoSmooth(io.ComfyNode):
    """
    Takes a sequence of video frames (e.g. from a composited video) and creates
    WAN I2V conditioning that treats every frame as a partially-known reference.

    All frames are VAE-encoded into concat_latent_image, and a uniform denoise
    mask tells the model how much freedom it has to modify each frame.
    Low denoise (0.1-0.3) gently smooths temporal artifacts while preserving content.
    High denoise (0.5+) allows the model to substantially rework the video.

    Use with a standard KSampler (denoise=1.0, let the concat_mask do the work)
    or with a WAN dual-pass sampler for two-stage refinement.
    """

    @classmethod
    def define_schema(cls) -> io.Schema:
        return io.Schema(
            node_id="BskiVideoSmooth",
            display_name="Bski Video Smooth (WAN I2V)",
            category="conditioning/video_models",
            inputs=[
                io.Conditioning.Input("positive"),
                io.Conditioning.Input("negative"),
                io.Vae.Input("vae"),
                io.Image.Input("images", tooltip="All video frames as an image batch. Ideally 4n+1 frames (5, 9, 13, 17, 21, ... 81) for optimal WAN alignment."),
                io.Float.Input(
                    "denoise", default=0.20, min=0.0, max=1.0, step=0.01, round=0.01,
                    display_mode=io.NumberDisplay.slider,
                    tooltip="1 = make new anchor_images, 0=anchor_images stay same (as possible) - Similar to img2img denoise.",
                    # tooltip="0 = preserve frames exactly, 1 = regenerate completely. Low values (0.1-0.3) smooth while preserving content.",
                ),
                io.Float.Input(
                    "denoise_mask", default=0.20, min=0.0, max=1.0, step=0.01, round=0.01,
                    display_mode=io.NumberDisplay.slider,
                    tooltip="# 1 = big change, 0 = zero change (1=must look like anchor image, 0=dont?)",
                    # tooltip="2nd step denoise, how closely Wan stays to newly generated anchor_images",
                    # tooltip="0 = preserve frames exactly, 1 = regenerate completely. Low values (0.1-0.3) smooth while preserving content.",
                ),
                io.Int.Input("width", default=832, min=16, max=8192, step=16, display_mode=io.NumberDisplay.number),
                io.Int.Input("height", default=480, min=16, max=8192, step=16, display_mode=io.NumberDisplay.number),
                # io.Int.Input("batch_size", default=1, min=1, max=4096, display_mode=io.NumberDisplay.number),
            ],
            outputs=[
                io.Conditioning.Output(display_name="positive"),
                io.Conditioning.Output(display_name="negative"),
                io.Latent.Output(display_name="latent"),
                io.Int.Output(display_name="frame_count"),
            ],
        )

    @classmethod
    def execute(cls, positive, negative, vae, images, denoise, denoise_mask, width, height):
        # Empty latent for the sampler (standard WAN approach - model generates
        # from noise, guided by concat conditioning)
        device = comfy.model_management.intermediate_device()
        num_frames = images.shape[0]
        spacial_scale = vae.spacial_compression_encode()
        latent_channels = vae.latent_channels
        latent_t = ((num_frames - 1) // 4) + 1
        total_latents = ((num_frames - 1) // 4) + 1
        H = height // spacial_scale
        W = width // spacial_scale
        batch_size = 1
        latent = torch.zeros([batch_size, latent_channels, latent_t, H, W], device=device)

        logging.info("denoise_mask" + str(denoise_mask))
        logging.info("denoise" + str(denoise))
        logging.info("latent_channels " + str(latent_channels))

        # Resize all frames to target resolution
        images = comfy.utils.common_upscale(
            images.movedim(-1, 1), width, height, "bilinear", "center"
        ).movedim(1, -1)

        #### VAE-encode all frames into latent space
        #### concat_latent_image = vae.encode(images_resized[:, :, :, :3])
        # anchor_latent = vae.encode(images[:, :, :, :3])
        # anchor_latent = anchor_latent * denoise

        source = images[:, :, :, :3]
        # noisy_images = source + denoise * (0.5 - source)
        # noisy_images[0] = images[0]
        
        logging.info("source")
        logging.info("source")
        logging.info("source")
        logging.info("source")
        logging.info("source")
        logging.info(source)
        # logging.info("blended")
        # logging.info("blended")
        # logging.info("blended")
        # logging.info("blended")
        # logging.info(blended)
        # logging.info("noisy_image")
        # logging.info("noisy_image")
        # logging.info("noisy_image")
        # logging.info("noisy_image")
        # logging.info(noisy_images)

        # anchor_latent = vae.encode(noisy_images)
        # image_cond_latent = anchor_latent

        anchor_latent = vae.encode(source)
        noise_prep_tensor = torch.randn_like(anchor_latent)
        logging.info("noise_prep_tensor")
        logging.info("noise_prep_tensor")
        logging.info("noise_prep_tensor")
        logging.info("noise_prep_tensor")
        logging.info("noise_prep_tensor")
        logging.info("noise_prep_tensor")
        logging.info("noise_prep_tensor")
        logging.info(noise_prep_tensor)

        logging.info("anchor_latent BEFORE")
        logging.info("anchor_latent BEFORE")
        logging.info("anchor_latent BEFORE")
        logging.info("anchor_latent BEFORE")
        logging.info("anchor_latent BEFORE")
        logging.info("anchor_latent BEFORE")
        logging.info("anchor_latent BEFORE")
        logging.info(anchor_latent)
        # image_cond_latent = (1 - denoise) * anchor_latent + denoise * noise_prep_tensor
        image_cond_latent = anchor_latent + denoise * 0.1 * torch.randn_like(anchor_latent)
        image_cond_latent[:, :, 0] = anchor_latent[:, :, 0] # keep OG 1st image
        # image_cond_latent = torch.lerp(anchor_latent, noise_prep_tensor, denoise)
        # image_cond_latent = anchor_latent + torch.randn_like(anchor_latent) * (denoise * 0.05)

        logging.info("anchor_latent AFTER")
        logging.info("anchor_latent AFTER")
        logging.info("anchor_latent AFTER")
        logging.info("anchor_latent AFTER")
        logging.info("anchor_latent AFTER")
        logging.info("anchor_latent AFTER")
        logging.info("anchor_latent AFTER")
        logging.info(image_cond_latent)
        
        # 1 = big change, 0 = zero change
        logging.info("total_latents: " + str(total_latents))
        logging.info("latent.shape[2]: " + str(latent.shape[2]))
        logging.info("--------------")
        logging.info("H: " + str(H))
        logging.info("image_cond_latent.shape[-2]: " + str(image_cond_latent.shape[-2]))
        logging.info("--------------")
        logging.info("W: " + str(W))
        logging.info("image_cond_latent.shape[-1]: " + str(image_cond_latent.shape[-1]))
        logging.info("--------------")
        mask_svi = torch.ones((1, 1, total_latents, H, W), device=device, dtype=anchor_latent.dtype) * denoise_mask  # !!!!!!!
        mask_svi[:, :, :1] = 0.0

        mask_alt = torch.ones((1, 1, latent.shape[2], image_cond_latent.shape[-2], image_cond_latent.shape[-1]), device=images[0].device, dtype=images[0].dtype)
        mask_alt[:, :, :((images[0].shape[0] - 1) // 4) + 1] = 0.0
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info("mask_svi")
        logging.info(mask_svi)
        logging.info("mask_ALT")
        logging.info("mask_ALT")
        logging.info("mask_ALT")
        logging.info("mask_ALT")
        logging.info("mask_ALT")
        logging.info(mask_svi)

        # Attach encoded frames + mask to conditioning
        positive_out = node_helpers.conditioning_set_values(positive, {
            "concat_latent_image": image_cond_latent,
            "concat_mask": mask_svi,
        })

        negative_out = node_helpers.conditioning_set_values(negative, {
            "concat_latent_image": image_cond_latent,
            "concat_mask": mask_svi,
        })

        out_latent = {"samples": latent}

        return io.NodeOutput(positive_out, negative_out, out_latent, num_frames)

