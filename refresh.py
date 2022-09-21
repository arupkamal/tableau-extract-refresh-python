#!pip install --upgrade tableau-api-lib

import warnings
warnings.filterwarnings("ignore")

from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import get_workbooks_dataframe, get_datasources_dataframe
from tableau_api_lib.utils import flatten_dict_column

tableau_server_config = {
        'my_env': {
                'server': 'https://tabemea.MyServer.com',
                'api_version': '3.11',
                'personal_access_token_name':   'Python',           #create from [My Account Setting] in Tableau
                'personal_access_token_secret': 'XXXXXXXXXXXXXXXX', #create from [My Account Setting] in Tableau
                'site_name': 'Default',
                'site_url':  ''
        }
}

conn = TableauServerConnection(tableau_server_config, env='my_env', ssl_verify=False)
conn.sign_in()

workbooks_df = get_workbooks_dataframe(conn)
flatten_dict_column(df = workbooks_df, keys= ['name', 'id'], col_name='project')

My_workbook_id = 'e51f504d-219d-4c13-87c5-77f2b4fc74d5'
jobid =conn.update_workbook_now(workbook_id = My_workbook_id).json()['job']['id']

progress = 0
while progress< 100:
    resp = conn.query_job(job_id = jobid).json()['job']
    print('.', end='')
    try:
        progress    = int(resp['progress'])
    except:
        pass
    #exitcode    = resp['finishCode']
    #startedAt   = resp['startedAt']
    #completedAt = resp['completedAt']

print(f" {progress}%")
