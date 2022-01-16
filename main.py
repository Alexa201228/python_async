import asyncio
import os

import aiofiles
import aiohttp
import requests

from models import Photo
from utils import timer

ALBUM_URL = 'https://jsonplaceholder.typicode.com/albums/'
PHOTO_URL = 'https://jsonplaceholder.typicode.com/photos/'
DIR_NAME = 'uploads'


@timer
async def get_json_data(url: str):
    data = requests.get(url)
    return data.json()


async def write_photo(photo, album_title, photo_data) -> None:
    """
    Запись картинки на диск
    :param photo: Object Photo
    :return: None
    """
    filename = f'{DIR_NAME}/{album_title}/{photo_data.title}.jpeg'
    async with aiofiles.open(filename, 'wb') as file:
        photo_data.file = photo
        await file.write(photo)


async def upload_photo(url, album_title, photo, session):
    """
    Извлечения файла по url адресу
    :param url:
    :param session:
    :return:
    """
    async with session.get(url, allow_redirects=True) as response:
        data = await response.read()
        return await write_photo(data, album_title, photo)


@timer
async def main():
    """
    Главная функция вызова
    :return:
    """
    if not os.path.exists(DIR_NAME):
        os.mkdir(DIR_NAME)
    photo_data = await get_json_data(PHOTO_URL)
    album_data = await get_json_data(ALBUM_URL)
    albums_dict = dict()
    for album in album_data:
        albums_dict[album['id']] = album['title']
        if not os.path.exists(f"uploads/{album['title']}"):
            os.mkdir(f"uploads/{album['title']}")

    photo_tasks = []

    async with aiohttp.ClientSession() as session:
        for photo in photo_data:
            new_photo = Photo(title=photo['title'], album_id=photo['albumId'], url=photo['url'], thumbnail_url=photo['thumbnailUrl'])
            task = asyncio.create_task(upload_photo(photo['url'], albums_dict[photo['albumId']], new_photo, session))
            photo_tasks.append(task)
        await asyncio.gather(*photo_tasks)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
