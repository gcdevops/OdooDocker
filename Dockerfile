FROM odoo:13.0

USER root
COPY ./add-ons /mnt/extra-addons
COPY ./odoo.conf /etc/odoo/
RUN chown odoo /etc/odoo/odoo.conf

USER odoo