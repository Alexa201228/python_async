from __future__ import annotations


class Photo:
    """
    Класс фотографии
    Атрибуты:
    title: название фотографии
    album_id: идентификатор альбома фотографии
    url: ссылка на файл фотографии
    thumbnail_url: ссылка на thumbnail фотографии
    file: файл фотографии
    """
    def __init__(self, title: str, album_id: str, url: str, thumbnail_url: str, file=None):
        self.title = title
        self.album_id = album_id
        self.url = url
        self.thumbnail_url = thumbnail_url
        self.file = file
