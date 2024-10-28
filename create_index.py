import csv
from itertools import batched
from pathlib import Path

import open_clip
import torch
from PIL import Image
from voyager import Index, Space

BATCH_SIZE = 128

MODEL_NAME = "xlm-roberta-large-ViT-H-14"
PRETRAINED = "frozen_laion5b_s13b_b90k"

IMAGE_DIR = Path("data/images")
ICON_CSV = Path("data/icon.csv")


@torch.no_grad()
def create_index() -> None:
    # model
    model, preprocess = open_clip.create_model_from_pretrained(MODEL_NAME, PRETRAINED)
    model.eval()
    model.cuda()
    index = Index(Space.Cosine, model.visual.output_dim)
    with ICON_CSV.open("w") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name"])
        writer.writeheader()
        for batch in batched(IMAGE_DIR.iterdir(), BATCH_SIZE):
            images = [Image.open(path) for path in batch]
            inputs = torch.stack([preprocess(image) for image in images]).cuda()
            image_features = model.encode_image(inputs, normalize=True)
            names = [path.stem for path in batch]
            ids = index.add_items(image_features.cpu().numpy())
            writer.writerows(
                {"id": id_, "name": name} for id_, name in zip(ids, names, strict=True)
            )
    index.save("data/icon_index.voy")


if __name__ == "__main__":
    create_index()
