FROM odoo:13.0

USER root
COPY ./add-ons /var/lib/odoo
COPY ./odoo.conf /etc/odoo/

RUN python3 -m pip install wheel
RUN python3 -m pip install zxcvbn-python

ARG ODOO_DBNAME
ENV ODOO_DBNAME ${ODOO_DBNAME}

# USER odoo
ENTRYPOINT ["sh", "-c", "/entrypoint.sh -u hr_modifier -d $ODOO_DBNAME"]
