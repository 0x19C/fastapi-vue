import os
import json

from typing import IO, Union

from PIL import Image


def get_thumbnail_of_image(file_path, target_height=128):
    img = Image.open(file_path)
    width, height = img.size
    return img.resize((int(target_height * width / height), target_height), Image.Resampling.LANCZOS)


def generate_thumbnail_of_dataset(directory, target_height=128):
    if os.path.exists(os.path.join(directory, "thumbnail.png")):
        return
    if not os.listdir(directory):
        return
    images = [get_thumbnail_of_image(os.path.join(directory, filename), target_height) for filename in os.listdir(directory) if filename != "thumbnail.png"]

    total_width = sum(img.width for img in images)
    combined_image = Image.new("RGB", (total_width, target_height))
    x_offset = 0
    for img in images:
        combined_image.paste(img, (x_offset, 0))
        x_offset += img.width

    combined_image.save(os.path.join(directory, "thumbnail.png"))


def get_image_metadata(fp: Union[str, bytes, os.PathLike[str], os.PathLike[bytes],IO[bytes]]) -> dict:
    img = Image.open(fp)

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


def clone_image(fp: Union[str, bytes, os.PathLike[str], os.PathLike[bytes],IO[bytes]], brightness: float, noise: float):
    img = Image.open(fp)
    print("getdata", len(list(img.getdata())))

    img.thumbnail([128, 128])
    print("thumbnail getdata", len(list(img.getdata())))

    print("getexif", img.getexif())
    print("getextrema", img.getextrema())
    print("getxmp", img.getxmp())
    print("attributes", {
        "filename": img.filename,
        "format": img.format,
        "mode": img.mode,
        "size": img.size,
        "width": img.width,
        "height": img.height,
        "palette": img.palette,
        "info": img.info,
        "is_animated": img.is_animated,
        "n_frames": img.n_frames,
        "has_transparency_data": img.has_transparency_data,
    })
