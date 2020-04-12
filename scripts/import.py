#!/usr/bin/python3

# coding: utf-8

import xmlrpc.client
import os
import sys
import getopt
import csv

# get values from environment variables 
username = os.environ.get("IMPORT_SCRIPT_USERNAME")
password = os.environ.get("IMPORT_SCRIPT_PASSWORD")
db = os.environ.get("IMPORT_SCRIPT_DATABASE")
# url defaults to localhost
url = os.environ.get("IMPORT_SCRIPT_URL") or 'http://localhost:8069'

try:
    common = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/common')
    common.version()
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/object')
except Exception as e:
    raise Exception("Could not successfully connect to RPC server").with_traceback(
        e
    )

# Import Departments
filename = '/data/org_structure/odoo-org-csv.csv'
if os.path.isfile(filename):
    reader = csv.DictReader(open(filename,"r"))
    for row in reader:
        dept = {
            "name": row["Department Name"]
        }

        # if Department has a parent, get parent_id 
        if row["Parent Department/External ID"]:
            res = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Parent Department/External ID"]]]],{'fields': ['res_id']})
            dept["parent_id"] = int(res[0]["res_id"])

        print(dept)

        # Check if Department exists
        exist_dept = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        # If Department doesn't exist
        if not exist_dept:
            # Create Department
            dept_id = models.execute(
                db, 
                uid, 
                password,
                'hr.department',
                'create', 
                dept
            )
            print("Dept ID")
            print(dept_id)

            # Create Department External ID
            dept_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'hr.department',
                'res_id': dept_id
            }    
            dept_map_id = models.execute(db, uid, password,'ir.model.data','create', dept_map)
            print("Dept Ext ID")
            print(dept_map_id)

            # Create en_CA Translation
            dept_translation = {
                'name': 'hr.department,name',
                'res_id': dept_id,
                'lang': 'en_CA',
                'type': 'model',
                'src': row["Department Name"],
                'value': row["Department Name"],
                'module': '__import__',
                'state': 'translated'
            }
            dept_translation_id = models.execute(
                db,
                uid,
                password,
                'ir.translation',
                'create',
                dept_translation
            )
            print("Dept Translation ID")
            print(dept_translation_id)

            # if we have a Translation
            if ("Translation" in row):
                # Create Translation
                dept_translation = {
                    'name': 'hr.department,name',
                    'res_id': dept_id,
                    'lang': 'fr_CA',
                    'type': 'model',
                    'src': row["Department Name"],
                    'value': row["Translation"],
                    'module': '__import__',
                    'state': 'translated'
                }
                dept_translation_id = models.execute(
                    db,
                    uid,
                    password,
                    'ir.translation',
                    'create',
                    dept_translation
                )
                print("Dept Translation ID")
                print(dept_translation_id)

        # If Department exists
        else:
            
            # Update Department
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.department',
                'write', 
                [exist_dept[0]["res_id"], dept]
            )
            print("Dept ID")
            print(exist_dept[0]["res_id"])
         
            # Get en_CA Translation ID
            exist_dept_translation = models.execute_kw(
                db, 
                uid, 
                password,
                'ir.translation', 
                'search_read',
                [['&', '&',('name', '=', 'hr.department,name'),('res_id', '=', exist_dept[0]["res_id"]),('lang', '=', 'en_CA')]],{'fields': ['id']}
            )
            
            # Update en_CA Translation
            dept_translation = {
                'src': row["Department Name"],
                'value': row["Department Name"]
            }
            models.execute_kw(db, uid, password,'ir.translation','write', [exist_dept_translation[0]["id"], dept_translation])

            if ("Translation" in row):
                # Get fr_CA Translation ID
                exist_dept_translation = models.execute_kw(
                    db, 
                    uid, 
                    password,
                    'ir.translation', 
                    'search_read',
                    [['&', '&',('name', '=', 'hr.department,name'),('res_id', '=', exist_dept[0]["res_id"]),('lang', '=', 'fr_CA')]],{'fields': ['id']}
                )

                # If fr_CA Translation exists
                if exist_dept_translation:
                    # Update Translation
                    dept_translation = {
                        'src': row["Department Name"],
                        'value': row["Translation"]
                    }
                    models.execute_kw(db, uid, password,'ir.translation','write', [exist_dept_translation[0]["id"], dept_translation])

                # If fr_CA Translation doesn't exist
                else:
                    # Create Translation
                    dept_translation = {
                        'name': 'hr.department,name',
                        'res_id': exist_dept[0]["res_id"],
                        'lang': 'fr_CA',
                        'type': 'model',
                        'src': row["Department Name"],
                        'value': row["Translation"],
                        'module': '__import__',
                        'state': 'translated'
                    }
                    dept_translation_id = models.execute(
                        db,
                        uid,
                        password,
                        'ir.translation',
                        'create',
                        dept_translation
                    )

# Import Users
filename = '/data/org_structure/odoo-users-csv.csv'
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

        # Check if Job exists
        exist = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row[0]]]],{'fields': ['res_id']})

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

filename = '/data/org_structure/odoo-employees-csv.csv'
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