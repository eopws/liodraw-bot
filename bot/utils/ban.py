from bot import ROOT_PATH

async def add_to_banned_list(id: str):
    with open(f'{ROOT_PATH}/bot/banned.txt', 'a') as f:
        f.write(f"{id}\n")

async def remove_from_banned_list(id: str):
    banned_array = parse_banned_list()

    banned_array.remove(id)

    with open(f'{ROOT_PATH}/bot/banned.txt', 'w') as f:
        f.write(banned_array.join('\n') + '\n')

def parse_banned_list():
    with open(f'{ROOT_PATH}/bot/banned.txt', 'r') as f:
        filecontent = f.read()

        banned_array = filecontent.split('\n')

        banned_array.pop()

        return banned_array
