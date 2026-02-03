#  Copyright 2025 Hardware vCommunity Content MP
#  Author: Onur Yuzseven

def check_server(server):
    if server.startswith("http"):
        return str(server)
    else:
        return f"https://{server}"