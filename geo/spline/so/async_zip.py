#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
# from https://codereview.stackexchange.com/questions/293319/zipping-many-files
from datetime import datetime
from pathlib import Path
from time import sleep
import asyncio
import shutil
import tempfile


def create_zip(dir_to_zip: Path, output_dir: Path, epsilon: float = 1e-3) -> None:
    """Zip a directory.

    dir_to_zip (Path): Directory to zip.
    output_dir (Path): Dir where the zip will be written.

    """
    try:
        dest_file_no_ext = output_dir.joinpath(dir_to_zip.stem)
        print(
            f"{datetime.now()}: Creating ZIP archive: {dest_file_no_ext.name}.zip from "
            f"{dir_to_zip.name}",
        )

        # You could swap the call below with
        # sleep(10) or something to test without actually creating files.

        shutil.make_archive(
            f"{dest_file_no_ext}",  # Name of zip without ext.
            "zip",
            dir_to_zip.parent,  # Dir to zip from.
            dir_to_zip.name,  # Dir to include in the zip
        )
        print(f"{datetime.now()}: Created: {dest_file_no_ext.name}.zip.")
        sleep(epsilon)
    except Exception:
        print(
            "asyncio.TaskGroup fails in its entirety if any exceptions occur "
            "but I would simply swallow and log any exceptions here.",
        )
        raise


async def async_create_zip(dir_to_zip: Path, output_dir: Path) -> None:
    loop = asyncio.get_event_loop()
    create_zip_task = loop.run_in_executor(
        None,
        lambda: create_zip(dir_to_zip, output_dir),
    )
    await create_zip_task


async def make_packages() -> None:
    def create_fake_dir(fake_dir: Path, num_bytes: int) -> Path:
        # Test function to create directories containing
        # files of various sizes.
        fake_dir.mkdir()

        with fake_dir.joinpath("fakefile.bin").open("wb") as outstream:
            outstream.write(b"\x00" * num_bytes)

        return fake_dir

    with tempfile.TemporaryDirectory() as td:
        tempdir = Path(td)
        tempdir = Path("/tmp")

        output_dir = tempdir.joinpath("output")
        print(f"output_dir: {output_dir}")

        # In my real code, the dirs come from multiple locations.
        test_dirs = [
            create_fake_dir(tempdir.joinpath("dir1"), 100000000),  # 100mb
            create_fake_dir(tempdir.joinpath("dir2"), 1000000),  # 1mb
            create_fake_dir(tempdir.joinpath("dir3"), 100000000),  # 100mb
            create_fake_dir(tempdir.joinpath("dir4"), 500000),  # 0.5mb
        ]

        # Test synchronous.
        print("Synchronous Test:")
        start = datetime.now()
        for test_dir in test_dirs:
            create_zip(test_dir, output_dir)
        end = datetime.now()
        total = (end - start).total_seconds()
        print(f"total time: {total}")

        print("Asynchronous Test:")
        start = datetime.now()
        async with asyncio.TaskGroup() as tg:
            # Fire off create_zip tasks for every package file we find.
            # These tasks will be run asynchronously - so as to not pointlessly
            # wait for large zip files to be packed before packing others.

            for test_dir in test_dirs:
                tg.create_task(async_create_zip(test_dir, output_dir))
        end = datetime.now()
        total = (end - start).total_seconds()
        print(f"total time: {total}")


def run() -> None:
    # Creating zips might be a bit slow, so lets try
    # and run zip creation asynchronously.
    asyncio.run(make_packages())


if __name__ == "__main__":
    run()
