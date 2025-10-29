import json
import time
import logging
import aiohttp

from .const import API_DOMAIN, LANG

_LOGGER = logging.getLogger(__name__)

def get_sn() -> str:
    return str(int(round(time.time() * 1000)))

_CACHE_PID = []

async def async_get_pid_list(lang='en'):
    global _CACHE_PID
    if _CACHE_PID:
        return _CACHE_PID
    
    if lang not in ['zh', 'en', 'es', 'pt', 'ja', 'ru', 'pt', 'nl', 'ko', 'fr', 'de']:
        _LOGGER.warning(f"Unsupported lang={lang}, using {LANG}")
        lang = LANG

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{API_DOMAIN}/api/v2/device_product/model', params={'lang': lang}, timeout=3) as res:
                if res.status != 200:
                    raise ValueError("Non-200 response")
                pid_list = await res.json()
    except Exception as e:
        _LOGGER.error(f"Error fetching PID list: {e}")
        return []
    
    if pid_list.get('ret') != '1' or not isinstance(pid_list.get('info', {}).get('list'), list):
        return []
    
    _CACHE_PID = pid_list['info']['list']
    return _CACHE_PID
