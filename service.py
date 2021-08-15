import requests
import json
import os
from dotenv import load_dotenv


# list of folders that will hold 10 images per folder
from requests.auth import HTTPBasicAuth

pathTenImages = {'bas/instanceportal',
                 'ivupro/addons',
                 'ivupro/content',
                 'ivupro/drivers',
                 'ivupro/factoryapplications',
                 'ivupro/sals',
                 'ivupro/server',
                 'ivupro/symbols',
                 'webctrl/addons',
                 'webctrl/content',
                 'webctrl/drivers',
                 'webctrl/factoryapplications',
                 'webctrl/sals',
                 'webctrl/server',
                 'webctrl/symbols'
                 }

# list of folders that will hold 5 images per folder
pathFiveImages = {'bacnetschub',
                 'bas/admintool',
                 'bas/messenger'}

print(f'type of 10 imgs: {type(pathTenImages)}')
print(f'type of 5 ings: {type(pathFiveImages)}')

# this is the  search API that return list of images based on the AQL payload that I pass in the  request body and this API use Bearer Token for authorization
# url = "https://cocomelon.jfrog.io/artifactory/api/search/aql"
url = "http://localhost:8082/artifactory/api/search/aql"
load_dotenv()
token = os.environ.get('SECRET_TOKEN')
print("token:::",token)
headers = {
    'Authorization': f'{token}',
    'Content-Type': 'text/plain'
}
# this function accept two parameters. the 1st one is list of path to the folders and the 2nd one is number of images to remove within the folders.
#
def main_function (paths, totalRemove):

    for path in paths:
        payload = f"items.find(\n{{\n  \"repo\": \"docker-local-dev\",\n  \"path\": {{\n    \"$match\": \"{path}\"\n  }},\n  \"name\": {{\n    \"$match\": \"SNAPSHOT_*\"\n  }},\n  \"type\": \"folder\"\n}}).sort({{\"$asc\" : [\"created\"]}})\n"
        # payload = f"items.find(\n{{\n  \"repo\": \"docker-local-dev\",\n  \"path\": {{\n    \"$match\": \"{path}\"\n  }},\n  \"name\": {{\n    \"$match\": \"SNAPSHOT_*\"\n  }},\n  \"type\": \"folder\"\n}}).include(\"name\", \"repo\",\"path\")"
        print("\n------------------",path,"---------------------\n")

        response = requests.request("POST", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)

        prettyJson = json.dumps(response_dict, indent=1)
        print(prettyJson)

        total = response_dict["range"]["total"]
        print('Total Artifact in the Repository::', total)

        remove = total - totalRemove
        print('Total Artifact to be Removed::', remove)

        if remove > 0:
            os.system('jfrog rt ping')
            cmd_search=f'jfrog rt s --spec=json-files/{path}.json --limit={remove}'
            cmd_delete = f'jfrog rt del --spec=json-files/{path}.json --limit={remove} --dry-run --quiet=true'
            print("--------list of old images to be deleted::----------")
            os.system(cmd_search)
            os.system(cmd_delete)
        else:
            print('Nothing to Delete!')

main_function(pathTenImages,10)
main_function(pathFiveImages,5)


