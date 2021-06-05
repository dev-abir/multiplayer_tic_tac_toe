import json
import os

from flask import Flask, request, session, escape, render_template, redirect
from flask_socketio import SocketIO, emit, send
from wtforms import Form, StringField, validators

from Room import Room, Player

app = Flask(__name__, static_url_path='', static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "secret!"  # TODO: in production?
# socketio = SocketIO(app, logger=True, engineio_logger=True)
socketio = SocketIO(app)

rooms = [Room()]


class UserDataForm(Form):
    uname = StringField('uname', [validators.Length(min=1, max=25)])


@socketio.event
def join(message):
    # TODO: for now, forcefully put 'x' as game character
    global player_count  # TODO: may be a bad hack?
    new_player = Player(uname=_sanitize_str(
        message["uname"]), game_character='x', ws_sid=request.sid)
    session["player_uid"] = new_player.uid
    _allot_room(new_player)


@socketio.event
def turn(json_str):
    posX = json_str["posX"]
    posY = json_str["posY"]
    # weird bug... session cookie doesn't mutate(in the _allot_room function)
    # room_id = session["room_id"]
    room_id = json_str["room_id"]

    player_uid = session["player_uid"]
    room = None
    for _room in rooms:
        if _room.room_id == room_id:
            room = _room
            break
    player = room.player1 if player_uid == room.player1.uid else room.player2
    message = room.add_turn(this_player_id=player_uid,
                            character=player.game_character, posX=posX, posY=posY)
    if message is not None:
        send(message)
    else:
        room.broadcast_board()
        game_state = room.game.game_state()
        if game_state == 'w':
            room.broadcast_event("game_won", f"{player.uname} won.")
        elif game_state == 'd':
            room.broadcast_event("game_draw", '')


@socketio.on("disconnect")
def on_disconnect():
    # TODO: expecting cookie isn't tampered with
    player_uid = session['player_uid']
    room_id = session["room_id"]

    for room in rooms:
        if room.room_id == room_id:
            room.game.reset_game()
            if room.player1 is not None and room.player1.uid == player_uid:
                if room.player2 is not None:  # TODO: to delete empty rooms (test it once)
                    send(f"Player {room.player1.uname} is disconnected.\n"
                         "Please wait for new players to join.\n"
                         "Sorry, your game character will be 'x' from now...", to=room.player2.ws_sid)
                    room.player2.game_character = 'x'  # TODO: hard code for now...
                    room.player1 = None
                    _allot_room(room.player2)
                else:
                    rooms.remove(room)
                return
            elif room.player2 is not None and room.player2.uid == player_uid:
                if room.player1 is not None:  # TODO: to delete empty rooms (test it once)
                    send(f"Player {room.player2.uname} is disconnected.\n"
                         "Please wait for new players to join.\n"
                         "Sorry, your game character will be 'x' from now...", to=room.player1.ws_sid)
                    room.player1.game_character = 'x'  # TODO: hard code for now...
                    room.player2 = None
                    _allot_room(room.player1)
                else:
                    rooms.remove(room)
                return

    print(f"[warning] Player with uid {player_uid} isn't deleted.")


@socketio.on("disconnect")
def on_disconnect():
    # TODO: expecting cookie isn't tampered with
    player_uid = session['player_uid']
    room_id = session["room_id"]

    for room in rooms:
        if room.room_id == room_id:
            room.game.reset_game()
            if (room.player1 is not None and
                    room.player1.uid == player_uid and
                    room.player2 is not None):
                send(f"Player {room.player1.uname} is disconnected.\n"
                     "Please wait for new players to join.\n", to=room.player2.ws_sid)
                alone_player = room.player2
                rooms.remove(room)
                _allot_room(alone_player)
            elif (room.player2 is not None and
                  room.player2.uid == player_uid and
                  room.player1 is not None):
                send(f"Player {room.player2.uname} is disconnected.\n"
                     "Please wait for new players to join.\n", to=room.player1.ws_sid)
                alone_player = room.player1
                rooms.remove(room)
                _allot_room(alone_player)


def _allot_room(player):
    for room in rooms:
        if room.add_player(player):
            # FIXME: cannot edit session cookie directly...
            session["room_id"] = room.room_id

            player.room_id = room.room_id
            room.broadcast_player_data()
            return  # if add player is success, exit from this func

    # if no rooms are empty, create a new one...
    new_room = Room(player1=player)
    session["room_id"] = new_room.room_id
    player.room_id = new_room.room_id
    rooms.append(new_room)
    emit("player_data", player.to_dict(), to=player.ws_sid)
    send("Please wait for new players to join.")


def _sanitize_str(string):
    return escape(str(string).strip())


@app.route('/')
def entry():
    return app.send_static_file("index.html")


@app.route('/game', methods=['POST', 'GET'])
def enter_game():
    # TODO: create separate template dir
    form = UserDataForm(request.form)
    if form.validate():
        # TODO: set player data through cookie here, instead
        # of getting through ws in join event...
        return render_template("game.html", uname=form.uname.data)  # TODO: don't use a form class, something simpler?
    return redirect('/')


if __name__ == '__main__':
    # using port for Heroku...
    if os.environ.get("PORT"):
        socketio.run(app, host="0.0.0.0", port=os.environ["PORT"])
    else:
        socketio.run(app, host="0.0.0.0", port=5000)
