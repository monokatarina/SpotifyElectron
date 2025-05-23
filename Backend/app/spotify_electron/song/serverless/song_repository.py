"""Song repository for managing persisted data

Song metadata is stored in database and song files are managed by AWS S3 instances
When the song file is not needed, and only the metadata is required use base song services
"""

import app.spotify_electron.song.serverless.providers.song_collection_provider as provider
from app.logging.logging_constants import (
    LOGGING_SONG_SERVERLESS_REPOSITORY,
)
from app.logging.logging_schema import SpotifyElectronLogger
from app.spotify_electron.genre.genre_schema import Genre
from app.spotify_electron.song.base_song_schema import (
    SongCreateError,
    SongNotFoundError,
    SongRepositoryError,
)
from app.spotify_electron.song.serverless.song_schema import (
    SongDAO,
    SongDocument,
    SongMetadataDocument,
    get_song_dao_from_document,
)
from app.spotify_electron.song.validations.base_song_repository_validations import (
    validate_base_song_create,
    validate_song_exists,
)

song_repository_logger = SpotifyElectronLogger(LOGGING_SONG_SERVERLESS_REPOSITORY).get_logger()


async def get_song(name: str) -> SongDAO:
    """Get song from database

    Args:
        name: song name

    Raises:
        SongNotFoundError: found
        SongRepositoryError: unexpected error getting song

    Returns:
        the song
    """
    try:
        collection = provider.get_serverless_song_collection()
        song = await collection.find_one({"filename": name})

        validate_song_exists(song)
        assert song

        song_dao = get_song_dao_from_document(song_name=name, document=song["metadata"])

    except SongNotFoundError as exception:
        raise SongNotFoundError from exception
    except Exception as exception:
        song_repository_logger.exception(f"Error getting Song {name} from database")
        raise SongRepositoryError from exception
    else:
        song_repository_logger.info(f"Get Song by name returned {song_dao}")
        return song_dao


async def create_song(  # noqa: D417
    name: str,
    artist: str,
    seconds_duration: int,
    genre: Genre,
    photo: str,
) -> None:
    """Create song

    Args:
        name: song name
        artist: song artist
        duration: song duration in seconds
        genre: song genre
        photo: song photo

    Raises:
        SongRepositoryError: creating song
    """
    try:
        collection = provider.get_serverless_song_collection()

        song = SongDocument(
            filename=name,
            metadata=SongMetadataDocument(
                artist=artist,
                seconds_duration=seconds_duration,
                genre=str(genre.value),
                photo=photo,
                streams=0,
            ),
        )

        result = await collection.insert_one(song)
        validate_base_song_create(result)
    except SongCreateError as exception:
        song_repository_logger.exception(f"Error inserting Song {song} in database")
        raise SongRepositoryError from exception
    except SongRepositoryError as exception:
        song_repository_logger.exception(f"Unexpected error inserting song {song} in database")
        raise SongRepositoryError from exception
    else:
        song_repository_logger.info(f"Song added to repository: {song}")
