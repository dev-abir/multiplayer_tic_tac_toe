from flask_socketio import emit, send

from Game import Game


class Player:
    def __init__(self, uid, uname, game_character, ws_sid):
        self.uid = uid
        self.uname = uname
        self.game_character = game_character
        self.ws_sid = ws_sid  # websocket sid(for sending messages to a particular player)

    def to_dict(self):
        return {"uid": self.uid, "uname": self.uname, "game_character": self.game_character, "ws_sid": self.ws_sid}

    def __str__(self):
        return str(self.to_dict())


class Room:
    def __init__(self, room_id, player1, player2):
        self.room_id = room_id
        self.player1 = player1
        self.player2 = player2
        self.game = Game()

    def broadcast_board(self):
        emit("get_board", self.game.board, to=self.player1.ws_sid)
        emit("get_board", self.game.board, to=self.player2.ws_sid)
    
    def broadcast_event(self, event, message):
        emit(event, message, to=self.player1.ws_sid)
        emit(event, message, to=self.player2.ws_sid)

    def add_player(self, new_player):
        if self._add_player(new_player):
            other_player = self.player1 if new_player != self.player1 else self.player2
            if other_player is not None:  # check if the new player joined is the 1st player of the room...
                new_player.game_character = 'o'
                send("Sorry, you are forced to use 'o', as your game character.")
                send(f"You are playing with {other_player.uname}", to=new_player.ws_sid)
                send(f"You are playing with {new_player.uname}", to=other_player.ws_sid)
                self.broadcast_board()
            else:
                send("Please wait for new players to join.")
            return True
        else:
            return False

    def add_turn(self, this_player_id, character, posX, posY):
        other_player = self.player1 if this_player_id != self.player1.uid else self.player2
        if other_player is None:
            return "Illegal turn!"
        else:
            return self.game.add_turn_internal(character, posX, posY)

    def _add_player(self, player):
        if self.player1 is None:
            self.player1 = player
            return True
        elif self.player2 is None:
            self.player2 = player
            return True
        else:
            return False
