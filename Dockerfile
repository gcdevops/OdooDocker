FROM bitnami/odoo:13.0.20200310-debian-10-r18

COPY ./add-ons /opt/bitnami/odoo/odoo/addons/
COPY ./themes /opt/bitnami/odoo/odoo/addons/


ENTRYPOINT [ "/app-entrypoint.sh" ]
CMD [ "nami", "start", "--foreground", "odoo" ]
