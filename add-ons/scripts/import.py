#!/usr/bin/env python
# coding: utf-8

import xmlrpc.client
import csv

username =''
pwd =''
db =''
url = 'http://localhost:8069'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, pwd, {})

filename = ''
reader = csv.reader(open(filename,"rb"))
for row in reader:
    users = {
    'id': row[0],
    'employee_id': row[1],
    'name': row[2],
    'email': row[3],
    'login': row[4],
    }
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    users_id = models.execute(dbname, uid, pwd,'res.users','create', users)
    print(users_id)