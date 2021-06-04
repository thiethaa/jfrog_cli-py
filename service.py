import requests
import json
import os

url = "https://thiethaa.jfrog.io/artifactory/api/search/aql"

headers = {
    'Authorization': 'Bearer eyJ2ZXIiOiIyIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJ1RmdMYkV6RlhVQUZXYkhMcUcxNmJmVE9SSmhBdHJuSEM1V3RueUdYc1drIn0.eyJzdWIiOiJqZmZlQDAwMFwvdXNlcnNcL3RyaXl1bGlhbmEudGhpZUBnbWFpbC5jb20iLCJzY3AiOiJhcHBsaWVkLXBlcm1pc3Npb25zXC9hZG1pbiBhcGk6KiIsImF1ZCI6ImpmcnRAKiIsImlzcyI6ImpmZmVAMDAwIiwiaWF0IjoxNjIyMzkyODI2LCJqdGkiOiJmZGM4NTJmNi1hNzg5LTRhZDUtYTBmMi0yYmYzNjEwYmJkMzQifQ.lU1YB-mLJrISvQbcvmxqG3GWFoOMer3INkP6c44Eb--kOBKk6j43vk0ob_Lg0BDlaGW-N86OuqtxjW_ujqMdXE6Vr2c2qry8yPQWTMN7Dz01cNEeenKcvqh7hj0rWVZegkRuHRW6RFsIyZ-AEmuAoBE0jief-36JtlO616WFDC8LyZJeLYsaPb_Hzirova_k8iXGQ4bqHxUXQXIOOQuNPVMDQf-4MxCLrkbUPJ9PwJ6FF6YOVxvJb2ZQ2g15LdP0a4IjHXTEvQ79E7XFtRSDulfxyMnO8Oe1MthVNtcwfHNIZqV1Q2vtravBuVAJPAHa5o_UzsLcm9HtGodyBEsu8w',
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
    for path in paths :
        payload = f"items.find(\n{{\n  \"repo\": \"docker-local-dev\",\n  \"path\": {{\n    \"$match\": \"{path}\"\n  }},\n  \"name\": {{\n    \"$match\": \"SNAPSHOT_*\"\n  }},\n  \"type\": \"folder\"\n}}).include(\"name\", \"repo\",\"path\")"
        print(path)

        response = requests.request("POST", url, headers=headers, data=payload)
        response_dict = json.loads(response.text)
        print(response_dict)

        total = response_dict["range"]["total"]
        print('total artifact in the repository::', total)

        remove = total - totalRemove
        print('total artifact to be removed::', remove)

        if remove > 0:
            os.system('jfrog rt ping')
            cmd = f'jfrog rt del --spec=json-files/{path}.json --limit={remove} --dry-run --quiet=true'
            os.system(cmd)
        else:
            print('nothing to delete!')

mainFunction(pathTenImages,10)
mainFunction(pathFiveImages,5)