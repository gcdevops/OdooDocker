FROM odoo:13.0

USER root
COPY ./add-ons /var/lib/odoo
COPY ./odoo.conf /etc/odoo/

RUN python3 -m pip install wheel
RUN python3 -m pip install zxcvbn-python

ENV ODOO_DBNAME "local-dev"

# USER odoo
ENTRYPOINT ["sh", "-c", "/entrypoint.sh -u hr_modifier -d $ODOO_DBNAME"]
