from pathlib import Path
from civitai_manager.utils.config import Config
import download
import pytest

@pytest.mark.asyncio
async def test_download_queue():
    queue = download.DownloadQueue(dest_dir=".")
    assert isinstance(queue.dest_dir, Path)
    assert isinstance(queue.config, Config)
    assert queue.empty()

    task = download.DownloadTask(url="https://google.com", dest=Path("./foo.html"), config=queue.config)
    await queue.add(task=task)
    assert not queue.empty()

    await queue.start()
    q = await queue.get()
