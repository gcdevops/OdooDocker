FROM bitnami/odoo:13.0.20200310-debian-10-r18

USER root
COPY ./add-ons /mnt/extra-addons
COPY ./themes /mnt/extra-addons
COPY ./scripts/entrypoint.sh /
COPY ./odoo.conf /etc/odoo/
#RUN chown odoo /etc/odoo/odoo.conf
#RUN chmod 777 /entrypoint.sh

#USER odoo
