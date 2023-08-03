import pathlib
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from . import config

BASE_DIR = pathlib.Path(__file__).resolve().parent

settings = config.get_settings()
ASTRADB_CONNECT_BUNDLE = BASE_DIR / "unecrypted" / "astradb_connect.zip"
ASTRADB_CLIEND_ID = settings.ASTRADB_CLIENT_ID
ASTRADB_CLIEND_SECRET  = settings.ASTRADB_CLIENT_SECRET


def get_session():
    cloud_config = {
      'secure_connect_bundle': ASTRADB_CONNECT_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRADB_CLIEND_ID, ASTRADB_CLIEND_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session
