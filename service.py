import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
url = "https://thiethaa89.jfrog.io/artifactory/api/search/aql"


token = os.environ.get('SECRET_TOKEN')
print("token:::",token)
headers = {
    'Authorization': f'{token}',
    'Content-Type': 'text/plain'
}

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
                 'webctrl/symbols'}

pathFiveImages = {'bacnetschub',
                 'bas/admintool',
                 'bas/messenger'}


def mainFunction (paths, totalRemove):
    for path in paths:
        payload = f"items.find(\n{{\n  \"repo\": \"docker-local-dev\",\n  \"path\": {{\n    \"$match\": \"{path}\"\n  }},\n  \"name\": {{\n    \"$match\": \"SNAPSHOT_*\"\n  }},\n  \"type\": \"folder\"\n}}).include(\"name\", \"repo\",\"path\")"
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
            cmd = f'jfrog rt del --spec=json-files/{path}.json --limit={remove} --dry-run --quiet=true'
            os.system(cmd)
        else:
            print('Nothing to Delete!')

mainFunction(pathTenImages,10)
mainFunction(pathFiveImages,5)


