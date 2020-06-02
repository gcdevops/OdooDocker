FROM odoo:13.0

USER root
COPY ./add-ons /var/lib/odoo
COPY ./odoo.conf /etc/odoo/
COPY ./scripts/custom_entrypoint.sh /

RUN python3 -m pip install wheel
RUN python3 -m pip install zxcvbn-python
RUN chmod +x /custom_entrypoint.sh  && \
    chown odoo:odoo /custom_entrypoint.sh

ARG ODOO_DBNAME
ENV ODOO_DBNAME ${ODOO_DBNAME}
ENV ODOO_UPGRADE_MODULE ""

# USER odoo
ENTRYPOINT ["/custom_entrypoint.sh"]
