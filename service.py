import requests
import json
import os
import sys

url = "https://thiethaa89.jfrog.io/artifactory/api/search/aql"

bearer = sys.argv[1]
token = sys.argv[2]

headers = {
    'Authorization': f'{bearer} {token}',
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


# Bearer eyJ2ZXIiOiIyIiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYiLCJraWQiOiJ3UUhUY1BDakhDZnN5UzRVMFJUaUU4VzlMUENBWDZ4WFdROEpWR2hocXhRIn0.eyJzdWIiOiJqZmZlQDAwMFwvdXNlcnNcL2FydGlmYWN0b3J5ZGVtb0BnbWFpbC5jb20iLCJzY3AiOiJhcHBsaWVkLXBlcm1pc3Npb25zXC9hZG1pbiBhcGk6KiIsImF1ZCI6ImpmcnRAKiIsImlzcyI6ImpmZmVAMDAwIiwiaWF0IjoxNjI0MDczNjY5LCJqdGkiOiIwZjliMDAwNS05N2MwLTRiZWUtOWNhMi0xZjU1MTk5MTM0MTIifQ.DArlOO9qm-5vZCKcxPcr4lhz4XGRBU8nPEKoDnw3tTO-C4dY3MZuUVrREWcW74fQeZ2fHLBh2xw6HoQb8UsfaFgxyV-VCIdyb4Qfe52JSTI2VPl8gQVkylvWpnUuPCzipCgGMEXw6oXSckN7kGzanrB3-epxL6jLBdZc8p4nzoHqjVVmAp3b-r9ityBt9ou117G1vAY-7UR8nRwAEE0csGv4YPdYe5jjmm4igZE5mv7QGfxmeHdxQ_4wbtOCP-jC0jCfXv6JONYp46rfjjNlGOetmVBism3n_YLJsYZDNhBP5Vf2Kdt8WBJgybKnwBr4zP7zWjz5xQE-zC3omRUt3A