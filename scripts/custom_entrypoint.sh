#!/bin/bash

echo "ODOO: Run custom_entrypoint.sh"

if [[ -z "$ODOO_UPGRADE_MODULE" ]]
then
    echo "ODOO: No upgrade mode"
    /entrypoint.sh "$@"
    echo "ODOO: Done"
else
    echo "ODOO: Upgrade for the following modules: $ODOO_UPGRADE_MODULE"
    /entrypoint.sh "$@" -u $ODOO_UPGRADE_MODULE -d $ODOO_DBNAME
fi
