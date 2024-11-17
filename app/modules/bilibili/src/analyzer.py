import re
import typing as t
from abc import ABC, abstractmethod

# 全局作用域注入？


class IInfoFinder(ABC):
    @abstractmethod
    def find(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        pass


class Ef2EpisodeFinder(IInfoFinder):
    pattern: re.Pattern = re.compile(r"^<[\s\S]*?^>", re.M)

    def find(self, content: str) -> list[str]:
        return self.pattern.findall(content)


class Ef2FilenameFinder(IInfoFinder):
    pattern: re.Pattern = re.compile(r"^filename:\s?(.*?)$", re.M)

    def find(self, content: str) -> str:
        if matched := self.pattern.search(content):
            return matched.group(1)
        return ""


class Ef2SourceFilenameFinder(IInfoFinder):
    pattern: re.Pattern = re.compile(r"^http.*/(.*?)(?=\?)", re.M)

    def find(self, content: str) -> str:
        if matched := self.pattern.search(content):
            return matched.group(1)
        return ""


class Ef2ReferenceFinder(IInfoFinder):
    pattern: re.Pattern = re.compile(r"^referer:\s?(.*?)$", re.M)

    def find(self, content: str) -> str:
        if matched := self.pattern.search(content):
            return matched.group(1)
        return ""


class Ef2UserAgentFinder(IInfoFinder):
    pattern: re.Pattern = re.compile(r"^User-Agent:\s?(.*?)$", re.M)

    def find(self, content: str) -> str:
        if matched := self.pattern.search(content):
            return matched.group(1)
        return ""


class Ef2LinkFinder(IInfoFinder):
    pattern: re.Pattern = re.compile(r"(?=^http)(.*?)$", re.M)

    def find(self, content: str) -> str:
        if matched := self.pattern.search(content):
            return matched.group(1)
        return ""


EpisodeInfo = t.TypedDict(
    "EpisodeInfo",
    {
        "filename": str,
        "source_filename": str,
        "link": str,
        "reference": str,
        "user_agent": str,
    },
    total=False,
)


class EpisodeInfoFinder(IInfoFinder):

    def __init__(self) -> None:
        self.post_actions: t.List[t.Callable] = []

    def add_action(self, action: t.Callable[[EpisodeInfo], None]) -> None:
        self.post_actions.append(action)

    def find(self, content: str) -> EpisodeInfo:
        ret: EpisodeInfo = {
            "filename": Ef2FilenameFinder().find(content),
            "source_filename": Ef2SourceFilenameFinder().find(content),
            "link": Ef2LinkFinder().find(content),
            "reference": Ef2ReferenceFinder().find(content),
            "user_agent": Ef2UserAgentFinder().find(content),
        }

        for action in self.post_actions:
            action(ret)

        return ret
