import os

from typing import IO, Union, List

from PIL import Image, ImageEnhance, ImageChops


def __get_thumbnail_of_image(file_path, target_height=128) -> Image.Image:
    img = Image.open(file_path)
    width, height = img.size
    return img.resize((int(target_height * width / height), target_height), Image.Resampling.LANCZOS)


def generate_thumbnail_of_dataset(directory, target_height=128):
    if os.path.exists(os.path.join(directory, "thumbnail.png")):
        return
    if not os.listdir(directory):
        return
    images = [__get_thumbnail_of_image(os.path.join(directory, filename), target_height) for filename in os.listdir(directory) if filename != "thumbnail.png"]

    total_width = sum(img.width for img in images)
    combined_image = Image.new("RGB", (total_width, target_height))
    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    combined_image.save(os.path.join(directory, "thumbnail.png"))


def __parse_image_metadata(img: Image.Image) -> dict:
    info_dict = {}
    for key, value in img.info.items():
        if isinstance(value, bytes):
            try:
                info_dict[key] = value.decode("utf-8", errors="ignore")  # Decode safely
            except UnicodeDecodeError:
                info_dict[key] = None  # Remove non-decodable binary data
        else:
            info_dict[key] = value

    return {
        "format": img.format,
        "mode": img.mode,
        "size": img.size,
        "width": img.width,
        "height": img.height,
        "palette": img.palette,
        "info": str(info_dict),
    }


def get_image_metadata(fp: Union[str, bytes, os.PathLike[str], os.PathLike[bytes],IO[bytes]]) -> dict:
    img = Image.open(fp)
    return __parse_image_metadata(img)


def clone_dataset_with_images(origin_directory: str, target_directory: str, brightness: float, noise: float) -> List[dict]:
    images = []
    for image_name in os.listdir(origin_directory):
        with Image.open(os.path.join(origin_directory, image_name)) as img:
            # Change Brightness
            enhancer = ImageEnhance.Brightness(img)
            img_enhanced = enhancer.enhance(brightness / 100).convert("RGB")

            # Add Gaussian Noise
            noise_img = Image.effect_noise((img_enhanced.width, img_enhanced.height), noise).convert("RGB")
            noisy_image = ImageChops.add(img_enhanced, noise_img)

            noisy_image.save(os.path.join(target_directory, image_name))

            # Get metadata
            if img.filename != "thumbnail.png":
                images.append({
                    "name": img.filename,
                    "file_path": os.path.join(target_directory, image_name),
                    "metadata": __parse_image_metadata(noisy_image)
                })
    return images