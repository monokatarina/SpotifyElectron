"""Song repository for managing common persisted data regardless of the current architecture.
The repository will only handle Song metadata
"""

import app.spotify_electron.song.providers.song_collection_provider as provider
from app.logging.logging_constants import (
    LOGGING_BASE_SONG_REPOSITORY,
)
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import (
    SongDeleteError,
    SongMetadataDAO,
    SongNotFoundError,
    SongRepositoryError,
    get_song_metadata_dao_from_document,
)
from app.spotify_electron.song.providers.song_collection_provider import (
    get_song_collection,
)
from app.spotify_electron.song.validations.base_song_repository_validations import (
    validate_song_delete_count,
    validate_song_exists,
)

song_repository_logger = SpotifyElectronLogger(LOGGING_BASE_SONG_REPOSITORY).get_logger()


async def check_song_exists(name: str) -> bool:
    """Check if song exits

    Args:
        name: song name

    Raises:
        SongRepositoryError: checking if song exists

    Returns:
        if song exists
    """
    try:
        collection = provider.get_song_collection()
        song = await collection.find_one({"filename": name}, {"_id": 1})
    except Exception as exception:
        song_repository_logger.exception(f"Error checking if Song {name} exists in database")
        raise SongRepositoryError from exception
    else:
        result = song is not None
        song_repository_logger.debug(f"Song with name {name} exists: {result}")
        return result


async def get_song_metadata(name: str) -> SongMetadataDAO:
    """Get song metadata from database

    Args:
        name: song name

    Raises:
        SongNotFoundError: found
        SongRepositoryError: unexpected error getting song metadata

    Returns:
        the song
    """
    try:
        collection = provider.get_song_collection()
        song = await collection.find_one({"filename": name})

        validate_song_exists(song)
        assert song

        song_dao = get_song_metadata_dao_from_document(
            song_name=name,
            document=song["metadata"],
        )

    except SongNotFoundError as exception:
        raise SongNotFoundError from exception

    except Exception as exception:
        song_repository_logger.exception(f"Error getting Song metadata {name} from database")
        raise SongRepositoryError from exception
    else:
        song_repository_logger.info(f"Get Song metadata by name returned {song_dao}")
        return song_dao


async def delete_song(name: str) -> None:
    """Deletes a song

    Args:
    ----
        name: song name

    Raises:
    ------
        SongRepositoryError: an error occurred while deleting song from database
    """
    try:
        collection = provider.get_song_collection()
        result = await collection.delete_one({"filename": name})
        validate_song_delete_count(result)
        song_repository_logger.info(f"Song {name} Deleted")
    except SongDeleteError as exception:
        song_repository_logger.exception(f"Error deleting song {name} from database")
        raise SongRepositoryError from exception
    except SongRepositoryError as exception:
        song_repository_logger.exception(f"Unexpected error deleting song {name} in database")
        raise SongRepositoryError from exception


async def get_artist_from_song(name: str) -> str:
    """Get artist name from song

    Args:
        name: song name

    Raises:
        SongRepositoryError: while getting artist from song

    Returns:
        the artist name
    """
    try:
        collection = provider.get_song_collection()
        document = await collection.find_one({"filename": name})

        validate_song_exists(document)
        assert document

        song_metadata = get_song_metadata_dao_from_document(
            song_name=name,
            document=document["metadata"],
        )
    except SongRepositoryError as exception:
        song_repository_logger.exception(
            f"Unexpected error getting artist from song {name} in database"
        )
        raise SongRepositoryError from exception
    else:
        return song_metadata.artist


async def increase_song_streams(name: str) -> None:
    """Increase number of song streams

    Args:
        name: song name

    Raises:
        SongRepositoryError: while increasing song streams
    """
    try:
        collection = provider.get_song_collection()
        await collection.update_one({"filename": name}, {"$inc": {"metadata.streams": 1}})
    except SongRepositoryError as exception:
        song_repository_logger.exception(
            f"Unexpected error increasing stream count for artist {name} in database"
        )
        raise SongRepositoryError from exception


async def get_artist_total_streams(artist_name: str) -> int:
    """Get artist total streams

    Args:
        artist_name: artist name

    Raises:
        SongRepositoryError: while getting artist's total streams

    Returns:
        the number of total streams of artist songs
    """
    try:
        collection = get_song_collection()
        result_total_streams_query = collection.aggregate(
            [
                {"$match": {"metadata.artist": artist_name}},
                {"$group": {"_id": None, "streams": {"$sum": "$metadata.streams"}}},
            ]
        )
        result_list = await result_total_streams_query.to_list(length=1)

        if not result_list:
            return 0

        return result_list[0]["streams"]  # type: ignore

    except SongRepositoryError as exception:
        song_repository_logger.exception(
            f"Unexpected error gettig artist {artist_name} total streams in database"
        )
        raise SongRepositoryError from exception


async def get_song_names_search_by_name(song_name: str) -> list[str]:
    """Get song names when searching by name

    Args:
        song_name: song name to match

    Raises:
        SongRepositoryError: while getting songs by name

    Returns:
        list of song names that matched the song name
    """
    try:
        collection = provider.get_song_collection()
        cursor = collection.find(
            {"filename": {"$regex": song_name, "$options": "i"}}, {"_id": 0, "filename": 1}
        )
        return [song["filename"] async for song in cursor]
    except SongRepositoryError as exception:
        song_repository_logger.exception(
            f"Unexpected error getting song names that matched {song_name} in database"
        )
        raise SongRepositoryError from exception


async def get_songs_metadata_by_genre(genre: Genre) -> list[SongMetadataDAO]:
    """Obtains all songs with the selected genre

    Args:
        genre: genre to match

    Raises:
        SongRepositoryError: getting song metadatas from genre

    Returns:
        list of song metadatas with selected genre
    """
    collection = provider.get_song_collection()
    genre_str = Genre.get_genre_string_value(genre)
    cursor = collection.find({"metadata.genre": genre_str})
    try:
        return [
            get_song_metadata_dao_from_document(
                song_name=song_data["filename"], document=song_data["metadata"]
            )
            async for song_data in cursor
        ]
    except SongRepositoryError as exception:
        song_repository_logger.exception(
            f"Unexpected error getting songs metadata by genre {genre} in database"
        )
        raise SongRepositoryError from exception
