from streamlit.runtime.caching import get_data_cache_stats_provider


def clear(key: str) -> None:
    """Companion function for st.cache_data_clear() that clears a specific key"""
    data_caches = get_data_cache_stats_provider()
    with data_caches._caches_lock:
        data_cache = data_caches._function_caches.get(key)
        if data_cache is not None:
            data_cache.clear()
            data_cache.storage.close()
            data_caches._function_caches.pop(key)
