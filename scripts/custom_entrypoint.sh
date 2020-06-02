#!/bin/sh

if [[ -z "${ODOO_UPGRADE_MODULE}" ]]; then
    /entrypoint.sh
else
    /entrypoint.sh -u $ODOO_UPGRADE_MODULE -d $ODOO_DBNAME
fi
