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

# Filename Paths
org_path = './data/odoo-org-csv.csv'
jobs_path = './data/odoo-jobs-csv.csv'
buildings_path = './data/odoo-buildings-csv.csv'
regions_path = './data/odoo-regions-csv.csv'
skill_levels_path = './data/odoo-skill-levels-csv.csv'
sub_skills_path = './data/odoo-sub-skills-csv.csv'
skill_types_path = './data/odoo-skills-csv.csv'
logging_rules_path = './data/odoo-logging-rules-csv.csv'
users_path = './data/odoo-users-csv.csv'
employees_path = './data/odoo-employees-csv.csv'

try:
    common = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/common')
    common.version()
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/object')
except Exception as e:
    raise Exception("Could not successfully connect to RPC server").with_traceback(
        e
    )

def str_to_bool(s):
    if s == 'TRUE':
         return True
    elif s == 'FALSE':
         return False
    else:
         raise ValueError

# Import Teams

if os.path.isfile(org_path):
    reader = csv.DictReader(open(org_path,"r"))
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

# Import Job Positions

if os.path.isfile(jobs_path):
    reader = csv.DictReader(open(jobs_path,"r"))
    for row in reader:

        # Check if Job exists
        exist_job = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        job = {
            'name': row["Job Position"]
        }

        # If Job doesn't exist
        if not exist_job:

            print("test")

            # Create Job
            job_id = models.execute(db, uid, password,'hr.job','create', job)
            print("Job ID")
            print(job_id)

            # Create Job External ID
            job_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'hr.job',
                'res_id': job_id
            }
            job_map_id = models.execute(db, uid, password,'ir.model.data','create', job_map)
            print("Job Ext ID")
            print(job_map_id)

            # Create en_CA Translation
            job_translation = {
                'name': 'hr.job,name',
                'res_id': job_id,
                'lang': 'en_CA',
                'type': 'model',
                'src': row["Job Position"],
                'value': row["Job Position"],
                'module': '__import__',
                'state': 'translated'
            }
            job_translation_id = models.execute(
                db,
                uid,
                password,
                'ir.translation',
                'create',
                job_translation
            )
            print("Job Translation ID")
            print(job_translation_id)

            # if we have a Translation
            if ("Translation" in row):
                # Create Translation
                job_translation = {
                    'name': 'hr.job,name',
                    'res_id': job_id,
                    'lang': 'fr_CA',
                    'type': 'model',
                    'src': row["Job Position"],
                    'value': row["Translation"],
                    'module': '__import__',
                    'state': 'translated'
                }
                job_translation_id = models.execute(
                    db,
                    uid,
                    password,
                    'ir.translation',
                    'create',
                    job_translation
                )
                print("Job Translation ID")
                print(job_translation_id)


        # If Job exists
        else:
                    
            # Update Job
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.job',
                'write', 
                [exist_job[0]["res_id"], job]
            )
            print("Job ID")
            print(exist_job[0]["res_id"])
         
            # Get en_CA Translation ID
            exist_job_translation = models.execute_kw(
                db, 
                uid, 
                password,
                'ir.translation', 
                'search_read',
                [['&', '&',('name', '=', 'hr.job,name'),('res_id', '=', exist_job[0]["res_id"]),('lang', '=', 'en_CA')]],{'fields': ['id']}
            )
            
            # Update en_CA Translation
            job_translation = {
                'src': row["Job Position"],
                'value': row["Job Position"]
            }
            models.execute_kw(db, uid, password,'ir.translation','write', [exist_job_translation[0]["id"], job_translation])

            if ("Translation" in row):
                # Get fr_CA Translation ID
                exist_job_translation = models.execute_kw(
                    db, 
                    uid, 
                    password,
                    'ir.translation', 
                    'search_read',
                    [['&', '&',('name', '=', 'hr.job,name'),('res_id', '=', exist_job[0]["res_id"]),('lang', '=', 'fr_CA')]],{'fields': ['id']}
                )

                # If fr_CA Translation exists
                if exist_job_translation:
                    # Update Translation
                    job_translation = {
                        'src': row["Job Position"],
                        'value': row["Translation"]
                    }
                    models.execute_kw(db, uid, password,'ir.translation','write', [exist_job_translation[0]["id"], job_translation])

                # If fr_CA Translation doesn't exist
                else:
                    # Create Translation
                    job_translation = {
                        'name': 'hr.job,name',
                        'res_id': exist_job[0]["res_id"],
                        'lang': 'fr_CA',
                        'type': 'model',
                        'src': row["Job Position"],
                        'value': row["Translation"],
                        'module': '__import__',
                        'state': 'translated'
                    }
                    job_translation_id = models.execute(
                        db,
                        uid,
                        password,
                        'ir.translation',
                        'create',
                        job_translation
                    )

# Import Buildings

if os.path.isfile(buildings_path):
    reader = csv.DictReader(open(buildings_path,"r"))
    for row in reader:

        # Check if Building exists
        exist_building = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        #Get Country ID
        country = row["Country/External ID"]
        country = country.replace('base.', '')
        print(country)
        country_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[['&',('model', '=', 'res.country'),('name', '=', country)]],{'fields': ['res_id']})
        print(country_id[0]["res_id"])

        #Get State ID
        state = row["State/External ID"]
        state = state.replace('base.', '')
        print(state)
        state_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[['&',('model', '=', 'res.country.state'),('name', '=', state)]],{'fields': ['res_id']})
        print(state_id[0]["res_id"])

        building = {
            'name': row["Name"],
            'is_company': "true",
            'street': row["Street"],
            'city': row["City"],
            'zip': row["Zip"],
            'street': row["Street"],
            'country_id': country_id[0]["res_id"],
            'state_id': state_id[0]["res_id"]
        }

        # If Building doesn't exist
        if not exist_building:

            # Create Building
            building_id = models.execute(db, uid, password,'res.partner','create', building)
            print("Building ID")
            print(building_id)

            # Create Building External ID
            building_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'res.partner',
                'res_id': building_id
            }
            building_map_id = models.execute(db, uid, password,'ir.model.data','create', building_map)
            print("Building Ext ID")
            print(building_map_id)

        # If Building exists
        else:
                    
            # Update Building
            models.execute_kw(
                db, 
                uid, 
                password,
                'res.partner',
                'write', 
                [exist_building[0]["res_id"], building]
            )
            print("Building ID")
            print(exist_building[0]["res_id"])

# Import Regions

if os.path.isfile(regions_path):
    reader = csv.DictReader(open(regions_path,"r"))
    for row in reader:

        # Check if Region exists
        exist_region = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        region = {
            'name': row["Name"]
        }

        # If Region doesn't exist
        if not exist_region:

            # Create Region
            region_id = models.execute(db, uid, password,'hr.region','create', region)
            print("Region ID")
            print(region_id)

            # Create Region External ID
            region_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'hr.region',
                'res_id': region_id
            }
            region_map_id = models.execute(db, uid, password,'ir.model.data','create', region_map)
            print("Region Ext ID")
            print(region_map_id)

            # Create en_CA Translation
            region_translation = {
                'name': 'hr.region,name',
                'res_id': region_id,
                'lang': 'en_CA',
                'type': 'model',
                'src': row["Name"],
                'value': row["Name"],
                'module': '__import__',
                'state': 'translated'
            }
            region_translation_id = models.execute(
                db,
                uid,
                password,
                'ir.translation',
                'create',
                region_translation
            )
            print("Region Translation ID")
            print(region_translation_id)

            # if we have a Translation
            if ("Translation" in row):
                # Create Translation
                region_translation = {
                    'name': 'hr.region,name',
                    'res_id': region_id,
                    'lang': 'fr_CA',
                    'type': 'model',
                    'src': row["Name"],
                    'value': row["Translation"],
                    'module': '__import__',
                    'state': 'translated'
                }
                region_translation_id = models.execute(
                    db,
                    uid,
                    password,
                    'ir.translation',
                    'create',
                    region_translation
                )
                print("Region Translation ID")
                print(region_translation_id)


        # If Region exists
        else:
                    
            # Update Region
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.region',
                'write', 
                [exist_region[0]["res_id"], region]
            )
            print("Region ID")
            print(exist_region[0]["res_id"])
         
            # Get en_CA Translation ID
            exist_region_translation = models.execute_kw(
                db, 
                uid, 
                password,
                'ir.translation', 
                'search_read',
                [['&', '&',('name', '=', 'hr.region,name'),('res_id', '=', exist_region[0]["res_id"]),('lang', '=', 'en_CA')]],{'fields': ['id']}
            )
            
            # Update en_CA Translation
            region_translation = {
                'src': row["Name"],
                'value': row["Name"]
            }
            models.execute_kw(db, uid, password,'ir.translation','write', [exist_region_translation[0]["id"], region_translation])

            if ("Translation" in row):
                # Get fr_CA Translation ID
                exist_region_translation = models.execute_kw(
                    db, 
                    uid, 
                    password,
                    'ir.translation', 
                    'search_read',
                    [['&', '&',('name', '=', 'hr.region,name'),('res_id', '=', exist_region[0]["res_id"]),('lang', '=', 'fr_CA')]],{'fields': ['id']}
                )

                # If fr_CA Translation exists
                if exist_region_translation:
                    # Update Translation
                    region_translation = {
                        'src': row["Name"],
                        'value': row["Translation"]
                    }
                    models.execute_kw(db, uid, password,'ir.translation','write', [exist_region_translation[0]["id"], region_translation])

                # If fr_CA Translation doesn't exist
                else:
                    # Create Translation
                    region_translation = {
                        'name': 'hr.region,name',
                        'res_id': exist_region[0]["res_id"],
                        'lang': 'fr_CA',
                        'type': 'model',
                        'src': row["Name"],
                        'value': row["Translation"],
                        'module': '__import__',
                        'state': 'translated'
                    }
                    region_translation_id = models.execute(
                        db,
                        uid,
                        password,
                        'ir.translation',
                        'create',
                        region_translation
                    )

# Import Skill Levels

if os.path.isfile(skill_levels_path):
    reader = csv.DictReader(open(skill_levels_path,"r"))
    for row in reader:

        # Check if Skill Level exists
        exist_skill_level = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        skill_level = {
            'name': row["Name"],
            'level_progress': row["level_progress"],
        }

        # If Skill Level doesn't exist
        if not exist_skill_level:

            # Create Skill Level
            skill_level_id = models.execute(db, uid, password,'hr.skill.level','create', skill_level)
            print("Skill Level ID")
            print(skill_level_id)

            # Create Skill Level External ID
            skill_level_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'hr.skill.level',
                'res_id': skill_level_id
            }
            skill_level_map_id = models.execute(db, uid, password,'ir.model.data','create', skill_level_map)
            print("Skill Level Ext ID")
            print(skill_level_map_id)

        # If Skill Level exists
        else:
                    
            # Update Skill Level
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.skill.level',
                'write', 
                [exist_skill_level[0]["res_id"], skill_level]
            )
            print("Skill Level ID")
            print(exist_skill_level[0]["res_id"])

# Import Sub-skills

if os.path.isfile(sub_skills_path):
    reader = csv.DictReader(open(sub_skills_path,"r"))
    for row in reader:

        # Check if Sub-skill exists
        exist_sub_skill = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        sub_skill = {
            'name': row["Name"]
        }

        # If Sub-skill doesn't exist
        if not exist_sub_skill:

            # Create Sub-skill
            sub_skill_id = models.execute(db, uid, password,'hr.skill','create', sub_skill)
            print("Sub-skill ID")
            print(sub_skill_id)

            # Create Sub-skill External ID
            sub_skill_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'hr.skill',
                'res_id': sub_skill_id
            }
            sub_skill_map_id = models.execute(db, uid, password,'ir.model.data','create', sub_skill_map)
            print("Sub-skill Ext ID")
            print(sub_skill_map_id)

            # Create en_CA Translation
            sub_skill_translation = {
                'name': 'hr.skill,name',
                'res_id': sub_skill_id,
                'lang': 'en_CA',
                'type': 'model',
                'src': row["Name"],
                'value': row["Name"],
                'module': '__import__',
                'state': 'translated'
            }
            sub_skill_translation_id = models.execute(
                db,
                uid,
                password,
                'ir.translation',
                'create',
                sub_skill_translation
            )
            print("Sub-skill Translation ID")
            print(sub_skill_translation_id)

            # if we have a Translation
            if ("Translation" in row):
                # Create Translation
                sub_skill_translation = {
                    'name': 'hr.skill,name',
                    'res_id': sub_skill_id,
                    'lang': 'fr_CA',
                    'type': 'model',
                    'src': row["Name"],
                    'value': row["Translation"],
                    'module': '__import__',
                    'state': 'translated'
                }
                sub_skill_translation_id = models.execute(
                    db,
                    uid,
                    password,
                    'ir.translation',
                    'create',
                    sub_skill_translation
                )
                print("Sub-skill Translation ID")
                print(sub_skill_translation_id)


        # If Sub-skill exists
        else:
                    
            # Update Sub-skill
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.skill',
                'write', 
                [exist_sub_skill[0]["res_id"], sub_skill]
            )
            print("Sub-skill ID")
            print(exist_sub_skill[0]["res_id"])
         
            # Get en_CA Translation ID
            exist_sub_skill_translation = models.execute_kw(
                db, 
                uid, 
                password,
                'ir.translation', 
                'search_read',
                [['&', '&',('name', '=', 'hr.skill,name'),('res_id', '=', exist_sub_skill[0]["res_id"]),('lang', '=', 'en_CA')]],{'fields': ['id']}
            )
            
            # Update en_CA Translation
            sub_skill_translation = {
                'src': row["Name"],
                'value': row["Name"]
            }
            models.execute_kw(db, uid, password,'ir.translation','write', [exist_sub_skill_translation[0]["id"], sub_skill_translation])

            if ("Translation" in row):
                # Get fr_CA Translation ID
                exist_sub_skill_translation = models.execute_kw(
                    db, 
                    uid, 
                    password,
                    'ir.translation', 
                    'search_read',
                    [['&', '&',('name', '=', 'hr.skill,name'),('res_id', '=', exist_sub_skill[0]["res_id"]),('lang', '=', 'fr_CA')]],{'fields': ['id']}
                )

                # If fr_CA Translation exists
                if exist_sub_skill_translation:
                    # Update Translation
                    sub_skill_translation = {
                        'src': row["Name"],
                        'value': row["Translation"]
                    }
                    models.execute_kw(db, uid, password,'ir.translation','write', [exist_sub_skill_translation[0]["id"], sub_skill_translation])

                # If fr_CA Translation doesn't exist
                else:
                    # Create Translation
                    sub_skill_translation = {
                        'name': 'hr.skill,name',
                        'res_id': exist_sub_skill[0]["res_id"],
                        'lang': 'fr_CA',
                        'type': 'model',
                        'src': row["Name"],
                        'value': row["Translation"],
                        'module': '__import__',
                        'state': 'translated'
                    }
                    sub_skill_translation_id = models.execute(
                        db,
                        uid,
                        password,
                        'ir.translation',
                        'create',
                        sub_skill_translation
                    )

# Import Skill Types

if os.path.isfile(skill_types_path):
    reader = csv.DictReader(open(skill_types_path,"r"))
    for row in reader:

        if row["ID"] != "":
            
            # Check if Skill Type exists
            exist_skill_type = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

            skill_type = {
                'name': row["name"]
            }

            # If Skill Type doesn't exist
            if not exist_skill_type:

                # Create Skill Type
                skill_type_id = models.execute(db, uid, password,'hr.skill.type','create', skill_type)
                print("Skill Type ID")
                print(skill_type_id)

                # Create Skill Type External ID
                skill_type_map = {
                    'name': row["ID"],
                    'module': '__import__',
                    'model': 'hr.skill.type',
                    'res_id': skill_type_id
                }
                skill_type_map_id = models.execute(db, uid, password,'ir.model.data','create', skill_type_map)
                print("Skill Type Ext ID")
                print(skill_type_map_id)

                # Create en_CA Translation
                skill_type_translation = {
                    'name': 'hr.skill.type,name',
                    'res_id': skill_type_id,
                    'lang': 'en_CA',
                    'type': 'model',
                    'src': row["name"],
                    'value': row["name"],
                    'module': '__import__',
                    'state': 'translated'
                }
                skill_type_translation_id = models.execute(
                    db,
                    uid,
                    password,
                    'ir.translation',
                    'create',
                    skill_type_translation
                )
                print("Skill Type Translation ID")
                print(skill_type_translation_id)

                # if we have a Translation
                if ("Translation" in row):
                    # Create Translation
                    skill_type_translation = {
                        'name': 'hr.skill.type,name',
                        'res_id': skill_type_id,
                        'lang': 'fr_CA',
                        'type': 'model',
                        'src': row["name"],
                        'value': row["Translation"],
                        'module': '__import__',
                        'state': 'translated'
                    }
                    skill_type_translation_id = models.execute(
                        db,
                        uid,
                        password,
                        'ir.translation',
                        'create',
                        skill_type_translation
                    )
                    print("Skill Type Translation ID")
                    print(skill_type_translation_id)


            # If Skill Type exists
            else:
                
                skill_type_id = exist_skill_type[0]["res_id"]

                # Update Skill Type
                models.execute_kw(
                    db, 
                    uid, 
                    password,
                    'hr.skill.type',
                    'write', 
                    [skill_type_id, skill_type]
                )
                print("Skill Type ID")
                print(skill_type_id)
            
                # Get en_CA Translation ID
                exist_skill_type_translation = models.execute_kw(
                    db, 
                    uid, 
                    password,
                    'ir.translation', 
                    'search_read',
                    [['&', '&',('name', '=', 'hr.skill.type,name'),('res_id', '=', skill_type_id),('lang', '=', 'en_CA')]],{'fields': ['id']}
                )
                
                # Update en_CA Translation
                skill_type_translation = {
                    'src': row["name"],
                    'value': row["name"]
                }
                models.execute_kw(db, uid, password,'ir.translation','write', [exist_skill_type_translation[0]["id"], skill_type_translation])

                if ("Translation" in row):
                    # Get fr_CA Translation ID
                    exist_skill_type_translation = models.execute_kw(
                        db, 
                        uid, 
                        password,
                        'ir.translation', 
                        'search_read',
                        [['&', '&',('name', '=', 'hr.skill.type,name'),('res_id', '=', skill_type_id),('lang', '=', 'fr_CA')]],{'fields': ['id']}
                    )

                    # If fr_CA Translation exists
                    if exist_skill_type_translation:
                        # Update Translation
                        skill_type_translation = {
                            'src': row["name"],
                            'value': row["Translation"]
                        }
                        models.execute_kw(db, uid, password,'ir.translation','write', [exist_skill_type_translation[0]["id"], skill_type_translation])

                    # If fr_CA Translation doesn't exist
                    else:
                        # Create Translation
                        skill_type_translation = {
                            'name': 'hr.skill.type,name',
                            'res_id': skill_type_id,
                            'lang': 'fr_CA',
                            'type': 'model',
                            'src': row["name"],
                            'value': row["Translation"],
                            'module': '__import__',
                            'state': 'translated'
                        }
                        skill_type_translation_id = models.execute(
                            db,
                            uid,
                            password,
                            'ir.translation',
                            'create',
                            skill_type_translation
                        )

        if ("skill_ids/id" in row):

            #Get Skill ID
            exist_skill = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["skill_ids/id"]]]],{'fields': ['res_id']})

            skill = {
                'skill_type_id': skill_type_id
            }

            # Update Skill by adding/updating Skill Type
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.skill',
                'write', 
                [exist_skill[0]["res_id"], skill]
            )
            print("Skill ID")
            print(exist_skill[0]["res_id"])


        if row["skill_level_ids/id"] != "":

            #Get Skill Level ID
            exist_skill_level = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["skill_level_ids/id"]]]],{'fields': ['res_id']})

            skill_level = {
                'skill_type_id': skill_type_id
            }

            # Update Skill by adding/updating Skill Level
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.skill.level',
                'write', 
                [exist_skill_level[0]["res_id"], skill_level]
            )
            print("Skill Level ID")
            print(exist_skill_level[0]["res_id"])

# Import Audit Rules

if os.path.isfile(logging_rules_path):
    reader = csv.DictReader(open(logging_rules_path,"r"))
    for row in reader:

        # Check if Audit Rule exists
        exist_audit_rule = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        #Get Model ID
        model_id = models.execute_kw(db, uid, password,'ir.model', 'search_read',[[['model', '=', row["Model"]]]],{'fields': ['id']})
        print(model_id[0]["id"])

        audit_rule = {
            'name': row["Name"],
            'model_id': model_id[0]["id"],
            'log_type': row["Type"],
            'log_write': str_to_bool(row["Log Writes"]),
            'log_unlink': str_to_bool(row["Log Deletes"]),
            'log_create': str_to_bool(row["Log Creates"]),
            'log_read': str_to_bool(row["Log Reads"]),
            'state': row["state"],
        }

        # If Audit Rule doesn't exist
        if not exist_audit_rule:

            # Create Audit Rule
            audit_rule_id = models.execute(db, uid, password,'auditlog.rule','create', audit_rule)
            print("Audit Rule ID")
            print(audit_rule_id)

            # Create Audit Rule External ID
            audit_rule_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'auditlog.rule',
                'res_id': audit_rule_id
            }
            audit_rule_map_id = models.execute(db, uid, password,'ir.model.data','create', audit_rule_map)
            print("Audit Rule Ext ID")
            print(audit_rule_map_id)

        # If Audit Rule exists
        else:
                    
            # Update Audit Rule
            models.execute_kw(
                db, 
                uid, 
                password,
                'auditlog.rule',
                'write', 
                [exist_audit_rule[0]["res_id"], audit_rule]
            )
            print("Audit Rule ID")
            print(exist_audit_rule[0]["res_id"])

# Import Users

if os.path.isfile(users_path):
    reader = csv.DictReader(open(users_path,"r"))
    for row in reader:

        user = {
            "name": row["Name"],
            'email': row["Email"],
            'login': row["Login"]
        }        

        # Check if User exists
        exist_user = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        # If User doesn't exist
        if not exist_user:

            # Create User
            user_id = models.execute(db, uid, password,'res.users','create', user)
            print("User ID")
            print(user_id)

            # Create User External ID
            user_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'res.users',
                'res_id': user_id
            }    
            user_map_id = models.execute(db, uid, password,'ir.model.data','create', user_map)
            print("User Ext ID")
            print(user_map_id)

        # If User exists
        else:
            
            # Update User
            models.execute_kw(
                db, 
                uid, 
                password,
                'res.users',
                'write', 
                [exist_user[0]["res_id"], user]
            )
            print("User ID")
            print(exist_user[0]["res_id"])

# Import Employees

if os.path.isfile(employees_path):
    reader = csv.DictReader(open(employees_path,"r"))
    for row in reader:

        #Get User ID
        user_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', 'user-' + row["ID"]]]],{'fields': ['res_id']})
        user_id = user_id[0]["res_id"]

        #Get Department ID
        department_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Department/External ID"]]]],{'fields': ['res_id']})
        if department_id:
            department_id = department_id[0]["res_id"]

        #Get Job Position ID
        job_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Job Position/External ID"]]]],{'fields': ['res_id']})
        if job_id:
            job_id = job_id[0]["res_id"]

        #Get Work Address ID
        work_address_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Work Address/External ID"]]]],{'fields': ['res_id']})
        if work_address_id:
            work_address_id = work_address_id[0]["res_id"]

        #Get Region ID
        region_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Region/External ID"]]]],{'fields': ['res_id']})
        if region_id:
            region_id = region_id[0]["res_id"]

        employee = {
            'user_id': user_id,
            'name': row["Employee Name"],
            'work_email': row["Work Email"],
            'work_phone': row["Work Phone"],
            'x_employee_office_floor': row["Office floor"],
            'x_employee_office_cubicle': row["Office cubicle"],
            'x_employee_status': row["Employment status"],
            'x_employee_device_type': row["Device type"],
            'x_employee_asset_number': row["Asset number"],
            'x_employee_headset': eval(row["Headset availability"]),
            'x_employee_second_monitor': eval(row["Second monitor availability"]),
            'x_employee_mobile_hotspot': eval(row["Mobile hotspot availability"]),
            'x_employee_remote_access_network': eval(row["Remote access to network"]),
            'x_employee_remote_access_tool': row["Remote connection tool"],
            'department_id': department_id,
            'job_id': job_id,
            'address_id': work_address_id,
            'region_id': region_id
        }

        # Check if Employee exists
        exist_employee = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["ID"]]]],{'fields': ['res_id']})

        # If Employee doesn't exist
        if not exist_employee:

            # Create Employee
            employee_id = models.execute(db, uid, password,'hr.employee','create', employee)
            print("Employee ID")
            print(employee_id)

            # Create Employee External ID
            employee_map = {
                'name': row["ID"],
                'module': '__import__',
                'model': 'hr.employee',
                'res_id': employee_id
            }
            employee_map_id = models.execute(db, uid, password,'ir.model.data','create', employee_map)
            print("Employee Ext ID")
            print(employee_map_id)

        # If Employee exists
        else:
            
            employee_id = exist_employee[0]["res_id"]

            # Update Employee
            models.execute_kw(
                db, 
                uid, 
                password,
                'hr.employee',
                'write', 
                [employee_id, employee]
            )
            print("Employee ID")
            print(employee_id)

        #Get Skill Type ID
        skill_type_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Skills/Skill Type/External ID"]]]],{'fields': ['res_id']})
        if skill_type_id:
            skill_type_id = skill_type_id[0]["res_id"]

            #Get Skill ID
            skill_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Skills/Skill/External ID"]]]],{'fields': ['res_id']})
            skill_id = skill_id[0]["res_id"]

            #Get Skill Level ID
            skill_level_id = models.execute_kw(db, uid, password,'ir.model.data', 'search_read',[[['name', '=', row["Skills/Skill Level/External ID"]]]],{'fields': ['res_id']})
            skill_level_id = skill_level_id[0]["res_id"]

            # Check if Employee Skill Map exists
            exist_employee_skill_map = models.execute_kw(db, uid, password,'hr.employee.skill', 'search_read',[['&', '&', '&', ('employee_id', '=', employee_id), ('skill_id', '=', skill_id), ('skill_level_id', '=', skill_level_id), ('skill_type_id', '=', skill_type_id)]],{'fields': ['id']})

            # If Employee Skill Map doesn't exist
            if not exist_employee_skill_map:

                employee_skill = {
                    'employee_id': employee_id,
                    'skill_id': skill_id,
                    'skill_level_id': skill_level_id,
                    'skill_type_id': skill_type_id
                }

                # Create Employee Skill Map
                employee_skill_id = models.execute(db, uid, password,'hr.employee.skill','create', employee_skill)
                print("Employee Skill ID")
                print(employee_skill_id)