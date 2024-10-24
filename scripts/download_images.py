import re
from io import BytesIO
from itertools import pairwise
from time import sleep

import requests
from PIL import Image

from src.icon_browser.infra.data_source.image_dir import IMAGE_DIR

NOT_FOUND = 404


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

            res = requests.get(
                f"https://material-icons.github.io/material-icons-png/png/black/{icon_name}/baseline-4x.png",
                timeout=1000,
            )
            if res.status_code == NOT_FOUND:
                continue

            image = Image.open(BytesIO(res.content))
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            background.save(IMAGE_DIR / f"{var_name}.png")

            sleep(0.01)


if __name__ == "__main__":
    download_images()
