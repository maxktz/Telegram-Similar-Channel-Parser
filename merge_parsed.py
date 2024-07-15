from pathlib import Path

from config import LINE_FORMAT, SAVING_DIRECTORY

WRITE_TO = Path(SAVING_DIRECTORY) / "ALL_MERGED.txt"


def main():
    # if not LINE_FORMAT.startswith("{username}:"):
    #     raise ValueError(
    #         'For correct work of this module the LINE_FORMAT should start with "{username}:"'
    #     )

    saved_channels_dir = Path(SAVING_DIRECTORY).absolute()
    if not saved_channels_dir.is_dir():
        raise ValueError(f"Directory not exists {SAVING_DIRECTORY}")
    channel_files = [p for p in saved_channels_dir.iterdir() if p.suffix == ".txt"]

    all_channels = set()
    for file in channel_files:
        text = file.read_text(encoding="utf-8")
        channels = text.split("\n")
        for channel in channels:
            channel = channel.strip()
            if channel:
                # username = channel.split(":")[0].lower()
                all_channels.add(channel)

    WRITE_TO.write_text("\n".join(all_channels), encoding="utf-8")

    print(f'{len(all_channels)} merged and written to "{WRITE_TO}"')


if __name__ == "__main__":
    main()
