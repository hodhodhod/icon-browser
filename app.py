import csv
import logging
from pathlib import Path

import flet as ft
import open_clip
import torch
from open_clip import CustomTextCLIP
from open_clip.tokenizer import HFTokenizer
from voyager import Index

MODEL_NAME = "xlm-roberta-large-ViT-H-14"
PRETRAINED = "frozen_laion5b_s13b_b90k"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

ICON_CSV = Path("data/icon.csv")

PORT = 8000


class SearchIconsQueryService:
    def __init__(
        self,
        index: Index,
        clip: CustomTextCLIP,
        tokenizer: HFTokenizer,
        csv_path: Path,
        result_num: int,
    ) -> None:
        self.index = index
        self.result_num = result_num
        self.clip = clip
        self.tokenizer = tokenizer
        with csv_path.open("r") as f:
            self.mapping = {int(row["id"]): row["name"] for row in csv.DictReader(f)}

    @torch.no_grad()
    def __call__(self, word: str) -> tuple[list[str], list[float]]:
        encoding = self.tokenizer([word]).to(DEVICE)
        vector = self.clip.encode_text(encoding, normalize=True).squeeze(0)
        ids, distances = self.index.query(vector.cpu().numpy(), self.result_num)
        icons = [self.mapping[id_] for id_ in ids.tolist()]
        return icons, distances.tolist()


if __name__ == "__main__":
    clip = open_clip.create_model(MODEL_NAME, PRETRAINED)
    clip.eval()
    clip.to(DEVICE)
    tokenizer = open_clip.get_tokenizer(MODEL_NAME)
    index = Index.load("data/icon_index.voy")
    query = SearchIconsQueryService(index, clip, tokenizer, ICON_CSV, 20)

    def main(page: ft.Page) -> None:
        gv = ft.GridView(
            auto_scroll=False,
            max_extent=150,
            child_aspect_ratio=0.8,
            expand=True,
        )

        def on_submit(e: ft.ControlEvent) -> None:
            icons, _ = query(e.control.value)
            gv.controls = [
                ft.Column([ft.Icon(icon, size=100), ft.Text(icon, size=12)], spacing=0)
                for icon in icons
            ]
            e.page.update()

        search_field = ft.SearchBar(on_submit=on_submit)

        appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.SEARCH, color=ft.colors.ON_PRIMARY),
            title=ft.Text(
                value="Icon Browser",
                size=32,
                text_align=ft.TextAlign.START,
                color=ft.colors.ON_PRIMARY,
            ),
            toolbar_height=75,
            bgcolor=ft.colors.PRIMARY,
        )

        view = ft.View(controls=[search_field, gv], appbar=appbar)
        page.views.append(view)
        page.update()

    logging.info("Starting the app...on http://localhost:%d", PORT)
    ft.app(main, view=ft.AppView.WEB_BROWSER, port=PORT)
