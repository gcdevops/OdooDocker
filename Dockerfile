FROM odoo:13.0

USER root
COPY ./add-ons /var/lib/odoo
COPY ./odoo.conf /etc/odoo/
