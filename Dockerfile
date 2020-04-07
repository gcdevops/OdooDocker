FROM odoo:13.0

USER root
COPY ./add-ons /var/lib/odoo/addons/13.0/
COPY ./odoo.conf /etc/odoo/
