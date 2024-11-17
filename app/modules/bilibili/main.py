import os.path as osp
import typing as t
from dataclasses import dataclass

import tqdm  # type: ignore

from app.common import P
from app.common.action import IAction
from app.common.file import FileCollector, FileLoader
from app.modules.bilibili.src.analyzer import Ef2EpisodeFinder, EpisodeInfoFinder
from app.modules.bilibili.src.file import Ef2FileFilter, MediaFileExactlyName
from app.utils.ffmpeg import FfmpegProcessor

MergePack = dict[P, list[P]]


@dataclass
class Context:
    media_path: P = ""
    output_path: P = ""
    output_type: str = "mp4"
    dictionary_Path: P = ""


class Schedule(IAction):
    def __init__(self, context: Context) -> None:
        self.context: Context = context

    def collect_ef2_files(self) -> t.Sequence[P]:
        file_collector: FileCollector = FileCollector()
        file_collector.add_filter(Ef2FileFilter())
        return file_collector.invoke(self.context.dictionary_Path)

    def build_merge_pack(self, ef2_paths: t.Sequence[P]) -> MergePack:
        loader: FileLoader = FileLoader()
        ep_finder: Ef2EpisodeFinder = Ef2EpisodeFinder()
        info_finder = EpisodeInfoFinder()
        info_finder.add_action(
            lambda s: s.update({"filename": s["filename"][: s["filename"].rfind(".")]})
        )

        merge_pack: MergePack = {}

        ef2_contents: t.List[str] = [loader.invoke(ef2_path) for ef2_path in ef2_paths]
        episodes: t.List[str] = [
            episode for content in ef2_contents for episode in ep_finder.find(content)
        ]
        infos = [
            info_finder.find(episode)
            for episode in episodes
            if (info := info_finder.find(episode))
        ]

        for info in infos:
            filename = info["filename"]
            source_filename = info["source_filename"]
            merge_pack.setdefault(filename, []).append(source_filename)

        return merge_pack

    def abspath(self, merge_pack: MergePack) -> MergePack:
        ret: MergePack = {}
        exact_name_action: MediaFileExactlyName = MediaFileExactlyName()

        for k, v in merge_pack.items():
            k = osp.join(
                self.context.output_path, ".".join([str(k), self.context.output_type])
            )
            v = [
                exact_name_action.invoke(osp.join(self.context.media_path, i))
                for i in v
            ]
            ret[k] = v
        return ret

    def invoke(self) -> None:
        dictionary_paths: t.Sequence[P] = self.collect_ef2_files()

        merge_pack: MergePack = self.build_merge_pack(dictionary_paths)
        merge_pack = self.abspath(merge_pack)
        for k, v in tqdm.tqdm(merge_pack.items()):
            processor: FfmpegProcessor = FfmpegProcessor()
            processor.ffmpeg()
            for i in v:
                processor.option("i", str(i))

            processor.option("c", "copy")
            processor.option("y", "")
            processor.option("", str(k), prefix="")
            # processor.invoke()
            print(processor.command)
