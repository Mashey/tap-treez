# Treez Tap

This is a [Singer](https://singer.io) tap that reads data from the [Treez API](https://code.treez.io/) and produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

## How to use it

`tap-treez` works together with any other [Singer Target](https://singer.io) to move data from the Treez API to any target destination.

### Install

First, make sure Python 3 is installed on your system or follow these
installation instructions for [Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/) or
[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04).

This project is set up using [Python Poetry](https://python-poetry.org/). Once cloned and within the project directory, install dependencies with:

```bash
poetry install
```

## Configuration

Requirements to get started are API Credentials in the form of an API Key, Client ID and Dispensary.

# Streams

## Incremental Streams
All streams from the Treez API are setup to be Incremental.  These are iterated based on the Update field for each table.  The update field is then bookmarked for the next stream. (If there is not starting bookmark the beginning sync date is 2000-01-01T00:00:00.000-00:00)

[Customers](https://code.treez.io/reference#customer_api)
- Primary key fields: `customer_id`
- Replication strategy: INCREMENTAL
- Replication based on: `last_update`
- Nested Tables:  
    - Caregiver Details:
        - Table Name: `caregiver_details`
        - Primary key: `caregiver_customer_id`
    - Addresses:
        - Table Name: `addresses`
    - Merged Customer Ids:
        - Table Name: `merged_customer_ids`
    - Image List:
        - Table Name: `imageList`
    - Customer Groups:
        - Table Name: `customer_groups`
- Transformations: none

[Products](https://code.treez.io/reference#product_api-beta)
- Primary key fields: `product_id`
- Replication strategy: INCREMENTAL
- Replication based on: `last_update_at`
- Nested Tables:
    - Sellable Quantity Details:
        - Table Name: `sellable_quantity_detail`
    - Product Configurable Fields:
        - Table Name: `product_configurable_fields`
    - Pricing
        - Table Name: `pricing`
    - Attributes
        - Table Name: `attributes`
    - Product Barcodes:
        - Table Name: `product_barcodes`
    - E-Commerce:
        - Table Name: `e_commerce`
    - Lab Results:
        - Table Name: `lab_results`
    - External References:
        - Table Name: `external_references`
- Transformations: none

[Tickets](https://api-doc.marketman.com/?version=latest#6de85108-2163-41e8-8215-8ecf38fd6671)
- Primary key fields: `ticket_id`
- Replication strategy: INCREMENTAL
- Replication based on: `last_update_at`
- Foreign Keys: `customer_id`, `employee_id`
- Nested Tables:
    - Created By Employee:
        - Table Name: `created_by_employee`
        - Key Fields: `employee_id`
    - Deliver Address:
        - Table Name: `deliver_address`
        - Key Fields: `id`
    - Items:
        - Table Name: `items`
        - Key Field: `product_id`
        - Nested Tables:
            - POS Discounts
                - Table Name: `items.POS_discounts`
                - Key Fields: `id`
            - Discounts
                - Table Name: `items.discounts`
                - Key Fields: `id`
            - Tax
                - Table Name: `items.tax`
                - Key Fields: `id`
    - Payments
        - Table Name: `payments`
        - Key Field: `payment_id`
    - Purchase Limit:
        - Table Name: `purchase_limits`
- Transformations: none