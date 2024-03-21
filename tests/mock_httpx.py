from typing import Any

from os.path import join, dirname


def get_data_from_url(url: str):
    """
    Depending on the URL, returns the bin data of the requested file
    """
    splitted_url = url.split("/")

    if splitted_url[-2] == "full":
        # Getting indivitual stickers
        pack_id = splitted_url[-3]
        filename = f"{splitted_url[-1]}.bin"
    else:
        # Getting manifest
        pack_id = splitted_url[-2]
        filename = "manifest.bin"

    file_path = join(dirname(__file__), "test_data", pack_id, filename)

    with open(file_path, "rb") as f_in:
        data = f_in.read()
    return data


class MockResponse:
    """
    Used to monkeypatch `httpx`'s response
    """

    status_code = 200

    def __init__(self, url: str):
        self.content_data = get_data_from_url(url)

    @property
    def content(self):
        return self.content_data


class MockHttpx:
    """
    Used to monkeypatch `httpx`
    """

    @staticmethod
    def __init__(*args: Any, **kwargs: Any):
        pass

    @staticmethod
    async def __aenter__(*args: Any, **kwargs: Any):
        return MockHttpx

    @staticmethod
    async def __aexit__(*args: Any, **kwargs: Any):
        pass

    @staticmethod
    async def get(*args: Any, **kwargs: Any):
        return MockResponse(url=args[0])
