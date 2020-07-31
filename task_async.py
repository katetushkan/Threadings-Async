import asyncio
import datetime
import os
import aiofiles
import aiohttp

from task import DOWNLOAD_URL, flag_download_path_forming, simple_download

ASYNC_DOWNLOAD_DIR = './async_flags'


async def set_url_connection(request, client_url):
    async with request.get(client_url) as response:
        return await response.read()


async def async_download_single_flag(request, flag):
    flags_info = await set_url_connection(request, DOWNLOAD_URL + flag.flag_url)

    image = '{}.png'.format(flag.flag_name)
    path = os.path.join(ASYNC_DOWNLOAD_DIR, image)

    async with aiofiles.open(path, 'wb') as file:
        await file.write(flags_info)


async def async_download():
    flags = flag_download_path_forming()

    async with aiohttp.ClientSession() as request:
        await asyncio.gather(*[async_download_single_flag(request, flag) for flag in flags])


if __name__ == '__main__':
    async_download_start = datetime.datetime.now()
    asyncio.run(async_download())
    print(datetime.datetime.now() - async_download_start)

    simple_download_start = datetime.datetime.now()
    simple_download()
    print(datetime.datetime.now() - simple_download_start)

