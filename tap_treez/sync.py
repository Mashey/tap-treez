
import singer
import logging
from singer import Transformer, metadata
from tap_treez.client import TreezClient
from tap_treez.streams import STREAMS
from datetime import datetime, timezone, timedelta

LOGGER = singer.get_logger()

logger_2 = logging.getLogger(__name__)


def bookmark_time():
    return datetime.strftime((datetime.now() + timedelta(seconds=1)),
                             "%Y-%m-%dT%H:%M:%S.000Z")

def sync(config, state, catalog):
    records = 0
    client = TreezClient(client_id=config['client_id'],
                         api_key=config['api_key'],
                         dispensary=config['dispensary'])

    with Transformer() as transformer:
        for stream in catalog.get_selected_streams(state):
            tap_stream_id = stream.tap_stream_id
            stream_obj = STREAMS[tap_stream_id](client, state)
            replication_key = stream.replication_key
            stream_schema = stream.schema.to_dict()
            stream_metadata = metadata.to_map(stream.metadata)

            LOGGER.info('Staring sync for stream: %s', tap_stream_id)

            state = singer.set_currently_syncing(state, tap_stream_id)
            singer.write_state(state)

            stream_start_bookmark = bookmark_time()

            singer.write_schema(
                tap_stream_id,
                stream_schema,
                stream_obj.key_properties,
                stream.replication_key
            )

            for record in stream_obj.sync():
                transformed_record = transformer.transform(
                    record, stream_schema, stream_metadata)
                singer.write_record(
                    tap_stream_id,
                    transformed_record,
                )
                records += 1
            
            singer.write_bookmark(state,
                                  tap_stream_id,
                                  replication_key,
                                  stream_start_bookmark)
            LOGGER.info(f"Total Records written: {records}")
            singer.write_state(state)


    LOGGER.info(f'Records written: {records}')
    state = singer.set_currently_syncing(state, None)
    singer.write_state(state)
