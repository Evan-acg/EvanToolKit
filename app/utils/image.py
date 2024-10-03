import filetype  # type: ignore

import os.path as osp


def is_image(path: str) -> bool:
    if osp.isdir(path):
        return False
    kind = filetype.guess(path)
    return getattr(kind, "mime", "").startswith("image/")
