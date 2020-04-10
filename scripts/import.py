#!/usr/bin/env python
# coding: utf-8

import xmlrpc.client
import csv

username =''
password =''
db =''
url = 'http://localhost:8069'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Import Departments

filename = '/data/odoo-org-csv.csv'
reader = csv.reader(open(filename,"rt"))
i = 0
for row in reader:
    if i == 0:
        i = 1
    else:        
        if not row[3]:
            # Create Department without parent
            dept = {
            'name': row[1],
            'complete_name': row[1]
            }
            dept_id = models.execute(db, uid, password,'hr.department','create', dept)
            print("Dept ID")
            print(dept_id)

            # Create Department External ID
            dept_map = {
            'name': row[0],
            'module': '__import__',
            'model': 'hr.department',
            'res_id': dept_id
            }    
            dept_map_id = models.execute(db, uid, password,'ir.model.data','create', dept_map)
            print("Dept Ext ID")
            print(dept_map_id)

            # Create Translation Name

            dept_translation = {
            'name': 'hr.department,name',
            'res_id': dept_id,
            'lang': 'fr_CA',
            'type': 'model',
            'src': row[1],
            'value': row[2],
            'module': '__import__',
            'state': 'translated'
            }    
            dept_translation_id = models.execute(db, uid, password,'ir.translation','create', dept_translation)
            print("Dept Translation ID")
            print(dept_translation_id)

            # Create Translation Complete Name

            dept_translation = {
            'name': 'hr.department,complete_name',
            'res_id': dept_id,
            'lang': 'fr_CA',
            'type': 'model',
            'src': row[1],
            'value': row[2],
            'module': '__import__',
            'state': 'translated'
            }    
            dept_translation_id = models.execute(db, uid, password,'ir.translation','create', dept_translation)
            print("Dept Translation ID")
            print(dept_translation_id)
        else:
            # Create Department with parent
            # Get Department ID
            res = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row[3]]]],{'fields': ['res_id']})
            dept = {
            'name': row[1],
            'complete_name': row[1],
            'parent_id': int(res[0]["res_id"])
            }
            dept_id = models.execute(db, uid, password,'hr.department','create', dept)
            print("Dept ID")
            print(dept_id)

            # Create Department External ID
            dept_map = {
            'name': row[0],
            'module': '__import__',
            'model': 'hr.department',
            'res_id': dept_id
            }    
            dept_map_id = models.execute(db, uid, password,'ir.model.data','create', dept_map)
            print("Dept Ext ID")
            print(dept_map_id)

            # Create Department Translation Name

            dept_translation = {
            'name': 'hr.department,name',
            'res_id': dept_id,
            'lang': 'fr_CA',
            'type': 'model',
            'src': row[1],
            'value': row[2],
            'module': '__import__',
            'state': 'translated'
            }    
            dept_translation_id = models.execute(db, uid, password,'ir.translation','create', dept_translation)
            print("Dept Translation ID")
            print(dept_translation_id)

            # Create Department Translation Complete Name

            dept_translation = {
            'name': 'hr.department,complete_name',
            'res_id': dept_id,
            'lang': 'fr_CA',
            'type': 'model',
            'src': row[1],
            'value': row[2],
            'module': '__import__',
            'state': 'translated'
            }    
            dept_translation_id = models.execute(db, uid, password,'ir.translation','create', dept_translation)
            print("Dept Translation ID")
            print(dept_translation_id)

# Import Users

filename = '/data/odoo-users-csv.csv'
reader = csv.reader(open(filename,"rt"))
i = 0
for row in reader:
    if i == 0:
        i = 1
    else:
        # Create User
        user = {
        'name': row[2],
        'email': row[3],
        'login': row[4]
        }
        user_id = models.execute(db, uid, password,'res.users','create', user)
        print("User ID")
        print(user_id)

        # Create User External ID
        user_map = {
        'name': row[0],
        'module': '__import__',
        'model': 'res.users',
        'res_id': user_id
        }    
        user_map_id = models.execute(db, uid, password,'ir.model.data','create', user_map)
        print("User Ext ID")
        print(user_map_id)

# Import Job Position

filename = '/data/odoo-jobs-csv.csv'
reader = csv.reader(open(filename,"rt"))
i = 0
for row in reader:
    if i == 0:
        i = 1
    else:
        # Create Job
        job = {
        'name': row[1]
        }
        job_id = models.execute(db, uid, password,'hr.job','create', job)
        print("Job ID")
        print(job_id)

        # Create Job External ID
        job_map = {
        'name': row[0],
        'module': '__import__',
        'model': 'hr.job',
        'res_id': job_id
        }
        job_map_id = models.execute(db, uid, password,'ir.model.data','create', job_map)
        print("Job Ext ID")
        print(job_map_id)

        # Create Job Translation

        job_translation = {
        'name': 'hr.job,name',
        'res_id': job_id,
        'lang': 'fr_CA',
        'type': 'model',
        'src': row[1],
        'value': row[2],
        'module': '__import__',
        'state': 'translated'
        }    
        job_translation_id = models.execute(db, uid, password,'ir.translation','create', job_translation)
        print("Job Translation ID")
        print(job_translation_id)

# Import Employees

filename = '/data/odoo-employees-csv.csv'
reader = csv.reader(open(filename,"rt"))
i = 0
for row in reader:
    if i == 0:
        i = 1
    else:
        # Get Department ID
        dept = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row[4]]]],{'fields': ['res_id']})
        
        # Get Job ID
        job = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row[5]]]],{'fields': ['res_id']})

        # Get User ID
        user = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', 'user-' + row[2]]]],{'fields': ['res_id']})

        # Create Employee
        employee = {
        'name': row[1],
        'work_email': row[2],
        'work_phone': row[3],
        'user_id': int(user[0]["res_id"]),
        'department_id': int(dept[0]["res_id"]),
        'job_id': int(job[0]["res_id"])
        }
        employee_id = models.execute(db, uid, password,'hr.employee','create', employee)
        print("Employee ID")
        print(employee_id)

        # Create Employee External ID
        employee_map = {
        'name': row[0],
        'module': '__import__',
        'model': 'hr.employee',
        'res_id': employee_id
        }
        employee_map_id = models.execute(db, uid, password,'ir.model.data','create', employee_map)
        print("Employee Ext ID")
        print(employee_map_id)