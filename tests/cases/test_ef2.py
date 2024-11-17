import os.path as osp

from app.modules.bilibili.src.analyzer import (
    Ef2EpisodeFinder,
    Ef2FilenameFinder,
    Ef2LinkFinder,
    Ef2ReferenceFinder,
    Ef2SourceFilenameFinder,
    Ef2UserAgentFinder,
    EpisodeInfoFinder,
)
from app.modules.bilibili.src.file import MediaFileExactlyName


class TestEf2Analyzer:
    def test_ef2_episode_finder(self) -> None:
        source: str = osp.abspath("./tests/resources/ef2/0.ef2")
        with open(source, "r", encoding="utf8") as file:
            content: str = file.read()

        finder: Ef2EpisodeFinder = Ef2EpisodeFinder()
        items: list[str] = finder.find(content)
        assert 64 == len(items)

    def test_ef2_filename_finder(self) -> None:
        source: str = "filename: 02 - 2-monorepo开发环境搭建.mp4"
        expected: str = "02 - 2-monorepo开发环境搭建.mp4"
        finder: Ef2FilenameFinder = Ef2FilenameFinder()
        result: str = finder.find(source)
        assert expected == result

    def test_ef2_source_filename_finder(self) -> None:
        source: str = (
            "https://cn-zjjh-ct-04-25.bilivideo.com/upgcxcode/56/27/26650872756/26650872756-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1731662272&gen=playurlv2&os=bcache&oi=1918700663&trid=0000a71efa0b7ac04a579105988e2a9714e4u&mid=8560309&platform=pc&og=hw&upsig=985abb3fef3a1398b70751e3c7e8ddb9&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&cdnid=6583&bvc=vod&nettype=0&orderid=0,3&buvid=543DCD8D-B993-C4B7-9E37-E8E9994ABDF748614infoc&build=0&f=u_0_0&agrr=1&bw=44604&logo=80000000"
        )
        expected: str = "26650872756-1-30080.m4s"
        finder: Ef2SourceFilenameFinder = Ef2SourceFilenameFinder()
        result: str = finder.find(source)
        assert expected == result

    def test_ef2_link_finder(self) -> None:
        source: str = (
            "https://cn-zjjh-ct-04-25.bilivideo.com/upgcxcode/56/27/26650872756/26650872756-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1731662272&gen=playurlv2&os=bcache&oi=1918700663&trid=0000a71efa0b7ac04a579105988e2a9714e4u&mid=8560309&platform=pc&og=hw&upsig=985abb3fef3a1398b70751e3c7e8ddb9&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&cdnid=6583&bvc=vod&nettype=0&orderid=0,3&buvid=543DCD8D-B993-C4B7-9E37-E8E9994ABDF748614infoc&build=0&f=u_0_0&agrr=1&bw=44604&logo=80000000"
        )
        finder: Ef2LinkFinder = Ef2LinkFinder()
        result: str = finder.find(source)
        assert source == result

    def test_ef2_reference_finder(self) -> None:
        source: str = "referer: https://www.bilibili.com/video/BV13YDmYWEbx"
        expected: str = "https://www.bilibili.com/video/BV13YDmYWEbx"
        finder: Ef2ReferenceFinder = Ef2ReferenceFinder()
        result: str = finder.find(source)
        assert expected == result

    def test_ef2_user_agent_finder(self) -> None:
        source: str = (
            "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
        )
        expected: str = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
        )
        finder: Ef2UserAgentFinder = Ef2UserAgentFinder()
        result: str = finder.find(source)
        assert expected == result

    def test_ef2_episode_info_finder(self) -> None:
        source: str = (
            "<\nhttps://xy123x138x84x210xy.mcdn.bilivideo.cn:4483/upgcxcode/98/24/26650872498/26650872498-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1731662272&gen=playurlv2&os=mcdn&oi=1918700663&trid=0000f74da209943d41269e0e9d7027e0d6d6u&mid=8560309&platform=pc&og=cos&upsig=091d213e51d9b5137538036c322004c8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&mcdnid=50012574&bvc=vod&nettype=0&orderid=0,3&buvid=543DCD8D-B993-C4B7-9E37-E8E9994ABDF748614infoc&build=0&f=u_0_0&agrr=1&bw=26532&logo=A0020000\nreferer: https://www.bilibili.com/video/BV13YDmYWEbx\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0\nfilename: 01 - 1-Vue3和核心设计思想.mp4\n>"
        )
        expected = {
            "filename": "01 - 1-Vue3和核心设计思想.mp4",
            "source_filename": "26650872498-1-30080.m4s",
            "link": "https://xy123x138x84x210xy.mcdn.bilivideo.cn:4483/upgcxcode/98/24/26650872498/26650872498-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1731662272&gen=playurlv2&os=mcdn&oi=1918700663&trid=0000f74da209943d41269e0e9d7027e0d6d6u&mid=8560309&platform=pc&og=cos&upsig=091d213e51d9b5137538036c322004c8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&mcdnid=50012574&bvc=vod&nettype=0&orderid=0,3&buvid=543DCD8D-B993-C4B7-9E37-E8E9994ABDF748614infoc&build=0&f=u_0_0&agrr=1&bw=26532&logo=A0020000",
            "reference": "https://www.bilibili.com/video/BV13YDmYWEbx",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        }

        finder = EpisodeInfoFinder()

        assert expected == finder.find(source)

    def test_ef2_episode_info_finder_with_post_action_change_filename(self) -> None:
        source: str = (
            "<\nhttps://xy123x138x84x210xy.mcdn.bilivideo.cn:4483/upgcxcode/98/24/26650872498/26650872498-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1731662272&gen=playurlv2&os=mcdn&oi=1918700663&trid=0000f74da209943d41269e0e9d7027e0d6d6u&mid=8560309&platform=pc&og=cos&upsig=091d213e51d9b5137538036c322004c8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&mcdnid=50012574&bvc=vod&nettype=0&orderid=0,3&buvid=543DCD8D-B993-C4B7-9E37-E8E9994ABDF748614infoc&build=0&f=u_0_0&agrr=1&bw=26532&logo=A0020000\nreferer: https://www.bilibili.com/video/BV13YDmYWEbx\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0\nfilename: 01 - 1-Vue3和核心设计思想.mp4\n>"
        )
        expected = {
            "filename": "01 - 1-Vue3和核心设计思想",
            "source_filename": "26650872498-1-30080.m4s",
            "link": "https://xy123x138x84x210xy.mcdn.bilivideo.cn:4483/upgcxcode/98/24/26650872498/26650872498-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1731662272&gen=playurlv2&os=mcdn&oi=1918700663&trid=0000f74da209943d41269e0e9d7027e0d6d6u&mid=8560309&platform=pc&og=cos&upsig=091d213e51d9b5137538036c322004c8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&mcdnid=50012574&bvc=vod&nettype=0&orderid=0,3&buvid=543DCD8D-B993-C4B7-9E37-E8E9994ABDF748614infoc&build=0&f=u_0_0&agrr=1&bw=26532&logo=A0020000",
            "reference": "https://www.bilibili.com/video/BV13YDmYWEbx",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        }

        finder = EpisodeInfoFinder()
        finder.add_action(
            lambda s: s.update({"filename": s["filename"][: s["filename"].rfind(".")]})
        )

        assert expected == finder.find(source)


class TestMediaAction:
    def test_exactly_name(self) -> None:
        source = osp.abspath(r"F:\\temp\\26651658260-1-30064.m4s")
        expected: str = osp.abspath(r"F:\\temp\\26651658260-1-30064.mp4")
        action: MediaFileExactlyName = MediaFileExactlyName()
        assert expected == action.invoke(source)
