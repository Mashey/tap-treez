#!/usr/bin/env python3
import json

import singer
from singer.catalog import write_catalog
from tap_treez.discovery import discover
from tap_treez.sync import sync

REQUIRED_CONFIG_KEYS = ['client_id',
                        'api_key', 
                        'dispensary']

LOGGER = singer.get_logger()


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    catalog = args.catalog if args.catalog else discover()

    if args.discover:
        write_catalog(catalog)
    else:
        sync(args.config, args.state, catalog)


if __name__ == '__main__':
    main()
