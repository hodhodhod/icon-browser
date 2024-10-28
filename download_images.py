import re
from io import BytesIO
from itertools import pairwise
from pathlib import Path
from time import sleep

import requests
from PIL import Image

NOT_FOUND = 404
IMAGE_DIR = Path("data/images")


def download_images() -> None:
    response = requests.get(
        "https://raw.githubusercontent.com/flutter/flutter/master/packages/flutter/lib/src/material/icons.dart",
        timeout=1000,
    )
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    for comment_line, code_line in pairwise(response.text.splitlines()):
        icon_match = re.search(
            r'/// <i class="material-icons md-36">([a-z0-9_]+)</i>',
            comment_line,
        )
        var_match = re.search(r"const IconData ([a-z0-9_]+)", code_line)

        if icon_match and var_match:
            icon_name = icon_match.group(1)
            var_name = var_match.group(1)

            image_response = requests.get(
                f"https://material-icons.github.io/material-icons-png/png/black/{icon_name}/baseline-4x.png",
                timeout=1000,
            )
            if image_response.status_code == NOT_FOUND:
                continue

            transparent_image = Image.open(BytesIO(image_response.content))
            image = Image.new("RGB", transparent_image.size, (255, 255, 255))
            image.paste(transparent_image, mask=transparent_image.split()[3])
            image.save(IMAGE_DIR / f"{var_name}.png")

            sleep(0.01)


if __name__ == "__main__":
    download_images()
