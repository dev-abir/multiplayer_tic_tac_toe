from flask import Flask, request, session, escape
from flask_socketio import SocketIO, emit, send

from Room import Room, Player

app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "secret!"  # TODO: in production?
# socketio = SocketIO(app, logger=True, engineio_logger=True)
socketio = SocketIO(app)

rooms = [Room(room_id=1, player1=None, player2=None)]
player_count = 1


@socketio.event
def join(message):
    # TODO: for now, forcefully put 'x' as game character
    global player_count  # TODO: may be a bad hack?
    new_player = Player(uid=player_count, uname=_sanitize_str(message["uname"]), game_character='x', ws_sid=request.sid)
    session["player_uid"] = player_count
    player_count += 1
    for room in rooms:
        if room.add_player(new_player):
            session["room_id"] = room.room_id
            emit("player_data", new_player.to_dict())
            return  # if add player is success, exit from this func

    # if no rooms are empty, create a new one...
    rooms.append(Room(room_id=len(rooms) + 1, player1=new_player, player2=None))
    session["room_id"] = len(rooms) + 1
    emit("player_data", new_player.to_dict())
    send("Please wait for new players to join.")


@socketio.event
def turn(json_str):
    posX = json_str["posX"]
    posY = json_str["posY"]
    room_id = session["room_id"]
    player_uid = session["player_uid"]
    room = None
    for _room in rooms:
        if _room.room_id == room_id:
            room = _room
            break
    player = room.player1 if player_uid == room.player1.uid else room.player1
    if room.add_turn(this_player_id=player_uid, character=player.game_character, posX=posX, posY=posY):
        room.broadcast_board()
        game_state = room.game.game_state()
        if game_state == 'w':
            emit("game_won", f"{player.uname} won.")
        elif game_state == 'd':
            emit("game_draw")
    else:
        send("Please wait for your opponent!")


@socketio.on("disconnect")
def on_disconnect():
    # TODO: expecting cookie isn't tampered with
    player_uid = session['player_uid']
    room_id = session["room_id"]

    for room in rooms:
        if room.room_id == room_id:
            room.game.reset_board()
            if room.player1.uid == player_uid:
                if room.player2 is not None:  # TODO: to delete empty rooms (test it once)
                    send(f"Player {room.player1.uname} is disconnected.\nPlease wait for new players to join.",
                         to=room.player2.ws_sid)
                    room.player1 = None
                else:
                    rooms.remove(room)
                return
            elif room.player2.uid == player_uid:
                if room.player1 is not None:  # TODO: to delete empty rooms (test it once)
                    send(f"Player {room.player2.uname} is disconnected.\nPlease wait for new players to join.",
                         to=room.player1.ws_sid)
                    room.player2 = None
                else:
                    rooms.remove(room)
                return

    print(f"[warning] Player with uid {player_uid} isn't deleted.")


def _sanitize_str(string):
    return escape(str(string).strip())


if __name__ == '__main__':
    socketio.run(app)
