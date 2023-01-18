from types import SimpleNamespace
from src.utils.keyboard import create_keyboards


keys = SimpleNamespace(
    random_connect=':bust_in_silhouette: Random Connect',
    settings=':gear: Settings',
    exit=':cross_mark: Cancel'
)


keyboards = SimpleNamespace(
    main=create_keyboards(keys.random_connect, keys.settings),
    exit=create_keyboards(keys.exit)
)

states = SimpleNamespace(
    main='MAIN',
    random_connect='RANDOM_CONNECT',
    connected="CONNECTED"
)
