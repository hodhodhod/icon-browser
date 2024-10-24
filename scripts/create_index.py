import csv
from itertools import batched

import open_clip
import torch
from PIL import Image

from src.icon_browser.infra.data_source.icon_csv_path import ICON_CSV
from src.icon_browser.infra.data_source.icon_index_path import ICON_INDEX_PATH
from src.icon_browser.infra.data_source.image_dir import IMAGE_DIR
from src.lib.voyager_session import VoyagerSession

BATCH_SIZE = 128

MODEL_NAME = "xlm-roberta-large-ViT-H-14"
PRETRAINED = "frozen_laion5b_s13b_b90k"


def execute() -> None:
    # model
    model, preprocess = open_clip.create_model_from_pretrained(MODEL_NAME, PRETRAINED)
    model.eval()
    model.cuda()
    with (
        VoyagerSession.create(ICON_INDEX_PATH, model.visual.output_dim) as index,
        ICON_CSV.open("w") as f,
    ):
        writer = csv.DictWriter(f, fieldnames=["id", "name"])
        writer.writeheader()
        for batch in batched(IMAGE_DIR.iterdir(), BATCH_SIZE):
            images = [Image.open(path) for path in batch]
            inputs = torch.stack([preprocess(image) for image in images]).cuda()
            image_features = model.encode_image(inputs, normalize=True)
            names = [path.stem for path in batch]
            ids = [hash(name) for name in names]
            index.add_items(image_features.cpu().numpy(), ids)
            writer.writerows(
                {"id": id_, "name": name} for id_, name in zip(ids, names, strict=True)
            )


if __name__ == "__main__":
    execute()
