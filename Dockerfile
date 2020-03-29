FROM bitnami/odoo:13.0.20200310-debian-10-r18

COPY ./add-ons /bitnami/odoo/data/addons/13.0/
COPY ./themes /bitnami/odoo/data/addons/13.0/


ENTRYPOINT [ "/app-entrypoint.sh" ]
CMD [ "nami", "start", "--foreground", "odoo" ]