from settings import log
from game.player import Player
import uuid

class HatGame:
    num_players = 10
    num_words = 6
    id = None
    players = None
    sockets = None

    def __init__(self):
        self.players = {}
        self.sockets = {}
        self.id = str(uuid.uuid4())

    async def name(self, ws, data):
        name = data['name']
        log.debug(f'user {name} logged in as {id(ws)}')
        player = Player(name=name, ws=ws)
        self.players[name] = player
        self.sockets[id(ws)] = player
        await self.game(ws)

    async def game(self, ws):
        await ws.send_json({'cmd': 'game', 'id': self.id, 'numwords': self.num_words})

    async def words(self, ws, data):
        words = data['words']
        p = self.sockets[id(ws)]
        p.set_words(words)
        log.debug(f'user {p.name} sent words: {words}')

        # send prepare message to all players
        for p in self.players.values():
            await self.prepare(p.socket)

    async def prepare(self, ws):
        players = [p.name for p in self.players.values()]
        await ws.send_json({'cmd': 'prepare', 'players': players})
