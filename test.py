import multiprocessing
import requests
import app
import time

hostname = '0.0.0.0'

def start_server():
    app.read_json_files()
    app.app.run(host=hostname)


t = multiprocessing.Process(target=start_server)
t.start()
time.sleep(2)

def get_endpoints():
    endpoints = ['/employees','/employees/1','/offices','/offices/1',\
                 '/departments','/departments/1','/departments?expand=superdepartment.superdepartment',\
                 '/employees?expand=manager.manager&expand=department.superdepartment']
    results = {}
    for endpoint in endpoints:
        results[endpoint] = requests.get(f'http://{hostname}:5000{endpoint}')

    return results

def test_endpoints_return_200(results):
    for k,r in results.items():
        assert r.status_code == 200, k + 'endpoint returned error code'

def test_lists_return_id_1(results):
    lists = ['/employees','/offices','/departments']
    for list in lists:
        assert 'id' in results[list].json()[0], list + " endpoint: couldn't find id in first record of list endpoint"

def test_expanded_offices(result):
    assert 'id' in result.json()[8]['superdepartment']['superdepartment']

def test_multiple_expansion_employees(result):
    assert 'id' in result.json()[34]['department']['superdepartment']
    assert 'id' in result.json()[34]['manager']['manager']

#def test_lists_return_list
results = get_endpoints()
try:
    test_endpoints_return_200(results)
    test_lists_return_id_1(results)
    test_expanded_offices(results['/departments?expand=superdepartment.superdepartment'])
    test_multiple_expansion_employees(results['/employees?expand=manager.manager&expand=department.superdepartment'])
finally:
    t.terminate()

print('Tests completed.')