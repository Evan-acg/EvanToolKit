import click
import pytest

from app.common import P
from app.modules.bilibili.main import Context, Schedule


@click.group()
def main():
    pass


@main.command()
@click.option("-k", "--keyword", type=str, required=False, help="test case keyword")
def test(keyword: str | None) -> None:
    args: list[str] = ["-vs", "--lf"]
    if keyword:
        args.extend(["-k", keyword])
    pytest.main(args)


@main.command()
@click.option(
    "-m",
    "--media_path",
    type=click.Path(exists=True),
    required=True,
    help="where is media stored",
)
@click.option(
    "-o",
    "--output_path",
    type=click.Path(),
    required=True,
    help="where to store output",
)
@click.option(
    "-d",
    "--dictionary_path",
    type=click.Path(exists=True),
    required=True,
    help="where is dictionary stored",
)
@click.option("-t", "--output_type", type=click.Choice(["mp4", "mkv"]), default="mp4")
def run(media_path: P, output_path: P, dictionary_path: P, output_type: str) -> None:
    context = Context(
        media_path=media_path,
        output_path=output_path,
        dictionary_Path=dictionary_path,
        output_type=output_type,
    )
    schedule: Schedule = Schedule(context)
    schedule.invoke()


if __name__ == "__main__":

    # 'cls && python starter.py run'
    # 'cls && python starter.py test'

    main()
