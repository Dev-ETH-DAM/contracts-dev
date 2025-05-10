import binascii
import json
import os

from src.ContractUtility import ContractUtility
from src.MainContract import get_request_queue, move_to_in_progress_queue, get_in_progress_queue
from src.SubContract import add_crumb


async def process_request_queue(contract_address= '0x123f578600F8B64B235ba9D627F121c619731275'):
    request_items = await get_request_queue(contract_address)

    queue_list = []

    for task_tuple in request_items:
        task_object = {
            "sender": task_tuple[0],
            "timestamp": task_tuple[1],
            "content": task_tuple[2],
            "sum": task_tuple[3],
            "id": task_tuple[4],
            "subContractAddress": task_tuple[5],
        }
        
        queue_list.append(task_object)

    contract_utility = ContractUtility('sapphire-testnet')

    dummuJson = '''
    [
      {
        "alias_name": "Service A",
        "price": 10,
        "setup_task": {"command": "npm install", "timeout": 60},
        "setup_validation": {"script": "./validate_version.sh", "expected_output": "v1.2.3"},
        "max_run": 100
      },
      {
        "alias_name": "Service B",
        "price": 25,
        "setup_task": {"command": "sudo apt update && sudo apt install -y nginx", "timeout": 120},
        "setup_validation": {"url": "http://localhost", "status_code": 200},
        "max_run": 50
      },
      {
        "alias_name": "Service C",
        "price": 5,
        "setup_task": {"command": "python manage.py migrate", "timeout": 90},
        "setup_validation": {"query": "SELECT COUNT(*) FROM users", "min_rows": 1},
        "max_run": 200
      }
    ]
    '''

    for item in queue_list:
        sub_contract_address = await contract_utility.deploy_contract('SubContract')

        data = json.loads(dummuJson)

        for obj in data:

            await add_crumb(sub_contract_address, generate_random_bytes16(), obj['alias_name'], obj['price'], json.dumps(obj['setup_task']), json.dumps(obj['setup_validation']), obj['max_run'])

        await move_to_in_progress_queue(contract_address, item['id'], sub_contract_address)


    b = await get_in_progress_queue(contract_address)

    print(b)

        
def generate_random_bytes16():
  """Generates a random 16-byte value and returns it as a hex string."""
  random_bytes = os.urandom(16)
  hex_string = binascii.hexlify(random_bytes).decode('utf-8')
  return f"0x{hex_string}"