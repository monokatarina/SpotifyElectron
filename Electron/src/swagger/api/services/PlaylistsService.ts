/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PlaylistsService {
    /**
     * Get Playlist
     * Get playlist
     *
     * Args:
     * name: playlist name
     * token: JWT info
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getPlaylistPlaylistsNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/playlists/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Playlist
     * Update playlist
     *
     * Args:
     * name: playlist name
     * photo: playlist new photo
     * description: playlist new description
     * song_names: playlist new song names. Defaults to Body(...).
     * new_name: playlist new name. Defaults to None.
     * token: JWT info
     * @param name
     * @param photo
     * @param description
     * @param requestBody
     * @param newName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updatePlaylistPlaylistsNamePut(
        name: string,
        photo: string,
        description: string,
        requestBody: Array<string>,
        newName?: (string | null),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/playlists/{name}',
            path: {
                'name': name,
            },
            query: {
                'photo': photo,
                'description': description,
                'new_name': newName,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Playlist
     * Delete playlsit
     *
     * Args:
     * name: playlist name
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deletePlaylistPlaylistsNameDelete(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/playlists/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Playlist
     * Create playlist
     *
     * Args:
     * name: playlist name
     * photo: playlist photo
     * description: playlist description
     * song_names: list of song names included in playlist.
     * token: JWT info
     * @param name
     * @param photo
     * @param description
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createPlaylistPlaylistsPost(
        name: string,
        photo: string,
        description: string,
        requestBody: Array<string>,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/playlists/',
            query: {
                'name': name,
                'photo': photo,
                'description': description,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Playlists
     * Get all playlists
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getPlaylistsPlaylistsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/playlists/',
        });
    }
    /**
     * Get Selected Playlists
     * Get selected playlists
     *
     * Args:
     * names: playlist names
     * token: JWT info
     * @param names
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getSelectedPlaylistsPlaylistsSelectedNamesGet(
        names: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/playlists/selected/{names}',
            path: {
                'names': names,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Songs To Playlist
     * Add songs to playlist
     *
     * Args:
     * name: playlist name
     * song_names: song names
     * @param name
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addSongsToPlaylistPlaylistsNameSongsPatch(
        name: string,
        requestBody: Array<string>,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/playlists/{name}/songs/',
            path: {
                'name': name,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Remove Songs From Playlist
     * Remove songs from playlist
     *
     * Args:
     * name: playlist name
     * song_names: song names
     * @param name
     * @param songNames
     * @returns any Successful Response
     * @throws ApiError
     */
    public static removeSongsFromPlaylistPlaylistsNameSongsDelete(
        name: string,
        songNames: Array<string>,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/playlists/{name}/songs/',
            path: {
                'name': name,
            },
            query: {
                'song_names': songNames,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
