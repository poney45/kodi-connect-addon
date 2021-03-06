import json
import xbmc

from utils import _get

def _kodi_rpc(obj):
    return json.loads(xbmc.executeJSONRPC(json.dumps(obj)))

def get_movies():
    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": 'VideoLibrary.GetMovies',
        "id": 1,
        'params': {
            'properties': ['title', 'genre', 'cast', 'set']
        }
    })
    return _get(res, 'result', 'movies')

def get_tv_shows():
    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": 'VideoLibrary.GetTVShows',
        "id": 1,
        'params': {
            'properties': ['title', 'genre', 'cast']
        }
    })
    return _get(res, 'result', 'tvshows')

def get_active_playerid():
    res = _kodi_rpc({ "jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1 })
    players = _get(res, 'result')
    if not players:
        return None
    players = [player for player in players if _get(player, 'type') == 'video']
    if not players:
        return None
    return players[0]['playerid']

def is_player_playing(playerid):
    if not playerid:
        return None

    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": "Player.GetProperties",
        "id": 1,
        'params': {
            'playerid': playerid,
            'properties': ['speed']
        }
    })

    speed = _get(res, 'result', 'speed')
    if speed is None:
        return None

    return speed != 0

def play_pause_player(playerid):
    if not playerid:
        return

    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": "Player.PlayPause",
        "id": 1,
        'params': {
            'playerid': playerid
        }
    })

def stop_player(playerid):
    if not playerid:
        return

    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": "Player.Stop",
        "id": 1,
        'params': {
            'playerid': playerid
        }
    })

def get_episodes_for_season(tvshow_id, season_num):
    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": 'VideoLibrary.GetEpisodes',
        "id": 1,
        'params': {
            'tvshowid': tvshow_id,
            'season': season_num,
            'properties': ['episode'],
        }
    })

    return _get(res, 'result', 'episodes')

def get_episodeid(tvshow_id, season_num, episode_num):
    episodes = get_episodes_for_season(tvshow_id, season_num)

    if not episodes:
        return None

    for episode in episodes:
        if episode['episode'] == episode_num:
            return episode['episodeid']
    return None

def get_last_episodeid(tvshow_id, season_num):
    episodes = get_episodes_for_season(tvshow_id, season_num)

    if not episodes:
        return None

    return episodes[-1]['episodeid']

def get_next_unwatched_episode_of_tvshow(tvshow_id):
    FILTER_UNWATCHED = { "operator": "lessthan", "field": "playcount", "value": "1" };
    SORT_EPISODE = { "method": "episode", "order": "ascending" };

    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": 'VideoLibrary.GetEpisodes',
        "id": 1,
        'params': {
            'tvshowid': tvshow_id,
            'filter': FILTER_UNWATCHED,
            'sort': SORT_EPISODE,
            'properties': ['playcount'],
            'limits': { 'start': 0, 'end': 1 },
        }
    })

    episodes = _get(res, 'result', 'episodes')

    if not episodes:
        return None

    return episodes[0]['episodeid']

def play_movieid(movie_id):
    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": 'Player.Open',
        "id": 1,
        'params': {
            'item': { 'movieid': movie_id },
            'options': { 'resume': True },
        },
    })

    return res

def play_episodeid(episode_id):
    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": 'Player.Open',
        "id": 1,
        'params': {
            'item': { 'episodeid': episode_id },
            'options': { 'resume': True },
        },
    })

    return res

def get_current_item(playerid):
    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": "Player.GetItem",
        "params": {
            "properties": ["title", "season", "episode", "duration", "tvshowid", "set"],
            "playerid": playerid
        },
        "id": "VideoGetItem",
    })

    return _get(res, 'result', 'item')

def seek_to_percentage(playerid, percentage):
    res = _kodi_rpc({
        "jsonrpc": "2.0",
        "method": "Player.Seek",
        "params": {
            "percentage": percentage,
            "playerid": playerid,
        },
        "id": 1,
    })

    return _get(res, 'result')
