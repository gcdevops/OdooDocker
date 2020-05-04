import xmlrpc.client
import sys
import os

username = os.environ.get("DELETE_SCRIPT_USERNAME")
password = os.environ.get("DELETE_SCRIPT_PASSWORD")
db = os.environ.get("DELETE_SCRIPT_DATABASE")
url = os.environ.get("DELETE_SCRIPT_URL") or 'http://localhost:8069'

try:
    common = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/common')
    common.version()
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(url + '/xmlrpc/2/object')
except Exception as e:
    raise Exception("Could not successfully connect to RPC server").with_traceback(
        e.__traceback__
    )

print("Deleting Departments")
res = models.execute_kw(db, uid, password,'hr.department', 'search', [[]])
for row in res:
    sys.stdout.write("\rDeleting Department: %i" % row)
    sys.stdout.flush()
    models.execute_kw(db, uid, password, 'hr.department', 'unlink', [row])

print("Deleting Jobs")
res = models.execute_kw(db, uid, password,'hr.job', 'search', [[]])
for row in res:
    sys.stdout.write("\rDeleting Job: %i" % row)
    sys.stdout.flush()
    models.execute_kw(db, uid, password, 'hr.job', 'unlink', [row])

print("Deleting Employees")
res = models.execute_kw(db, uid, password,'hr.employee', 'search', [[]])
count = 0
last_position = 0
for row in range(0,len(res), 300):
    start = last_position
    if (start + 300 > len(res)):
        stop = start + ( 300 - stop + len(res))
    else:
        stop = start + 300
    sys.stdout.write("\rDeleted %i Employee" % count)
    sys.stdout.flush()
    models.execute_kw(db, uid, password, 'hr.employee', 'unlink', [res[start:stop]])
    last_position = stop 
    count += stop-start