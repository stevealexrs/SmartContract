from typing import Dict
import urllib.request
import urllib.parse
import json
import time

ETHERSCAN_URL = 'https://api.etherscan.io/api'
APPROVAL_EVENT = '0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'

def padInput(input: str) -> str:
    return f"0x{input.removeprefix('0x').rjust(64, '0')}"

def unpadInput(input: str) -> str:
    return f"0x{input[-40:]}"

def etherscanErc20Balance(token: str, address: str) -> int:
    params = {
        'module': 'account',
        'action': 'tokenbalance',
        'contractaddress': token,
        'address': address,
        'tag': 'latest'
    }
    url = f"{ETHERSCAN_URL}?{urllib.parse.urlencode(params)}"
    while(True):
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        content = json.loads(r.decode('utf-8'))
        result = content["result"]
        status = int(content["status"])

        if status == 0 and result == "Max rate limit reached, please use API Key for higher rate limit":
            time.sleep(5)
            continue

        return int(result)
    

def etherscanApproval(token: str, spender: str) -> Dict[str, int]:
    params = {
        'module': 'logs',
        'action': 'getLogs',
        'topic0': APPROVAL_EVENT,
        'topic2': padInput(spender),
        'topic0_2_opr': 'and',
        'address': token, 
        'fromBlock': 0,
        'toBlock': 'latest',
        'page': 0,
        'offset': 1000
    }
    url = f"{ETHERSCAN_URL}?{urllib.parse.urlencode(params)}"
    approvals = {}
    while(True):
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req).read()
        content = json.loads(r.decode('utf-8'))
        result = content["result"]
        status = int(content["status"])

        if status == 0 and len(result) == 0:
            break

        if status == 0 and result == "Max rate limit reached, please use API Key for higher rate limit":
            time.sleep(5)
            continue

        for event in result:
            approver = unpadInput(event["topics"][1])
            amount = int(event["data"], 16)

            if approver not in approvals:
                approvals[approver] = amount

        params['page'] += 1
    url = f"{ETHERSCAN_URL}?{urllib.parse.urlencode(params)}"
    return {k: v for k, v in approvals.items() if v != 0}

def etherscanApprovalWithBalances(approvals: Dict[str, int], token: str):
    approvalsWithBalance = {}
    for approver in approvals:
        balance = etherscanErc20Balance(token=token, address=approver)
        if balance > 0:
            approvalsWithBalance[approver] = min(balance, approvals[approver])
    return approvalsWithBalance

print(etherscanApprovalWithBalances(etherscanApproval(
    token="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", 
    spender="0x044b75f554b886a065b9567891e45c79542d7357")
), "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
    

    