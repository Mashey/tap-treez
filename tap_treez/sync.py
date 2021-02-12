
import singer
from singer import Transformer, metadata
from tap_treez.client import TreezClient
from tap_treez.streams import STREAMS

LOGGER = singer.get_logger()


def sync(config, state, catalog):
    records = 0
    client = TreezClient(client_id=config['client_id'],
                         api_key=config['api_key'],
                         dispensary=config['dispensary'])

    with Transformer() as transformer:
        for stream in catalog.get_selected_streams(state):
            tap_stream_id = stream.tap_stream_id
            stream_obj = STREAMS[tap_stream_id](client, state)
            # replication_key = stream_obj.replication_key
            stream_schema = stream.schema.to_dict()
            stream_metadata = metadata.to_map(stream.metadata)

            LOGGER.info('Staring sync for stream: %s', tap_stream_id)

            state = singer.set_currently_syncing(state, tap_stream_id)
            singer.write_state(state)

            singer.write_schema(
                tap_stream_id,
                stream_schema,
                stream_obj.key_properties,
                stream.replication_key
            )

            for record in stream_obj.sync():
                transformed_record = transformer.transform(
                    record, stream_schema, stream_metadata)
                LOGGER.info(f"Writing record: {transformed_record}")
                singer.write_record(
                    tap_stream_id,
                    transformed_record,
                )
                records += 1
            state = singer.clear_bookmark(state, tap_stream_id, 'last_updated_date')
            # singer.write_state(state, tap_stream_id, )

    LOGGER.info(f'Records written: {records}')
    state = singer.set_currently_syncing(state, None)
    singer.write_state(state)
