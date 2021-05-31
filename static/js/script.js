var socket = io();
var player_data;
var board_data = null;
socket.on('connect', function () {
	socket.emit('join', { uname: new Date().toLocaleTimeString() }, (res) => {
		console.log('ok');
	});
});
socket.on("message", function (message) {
	console.log(message);
});
socket.on("get_board", function (data) {
	board_data = data;
	console.log(board_data);
});
socket.on("player_data", function (data) {
	player_data = data
	console.log(player_data);
});

var fireB = () => {
	var posx = 0;
	var posy = 1;
	if (board_data == null) {
		socket.emit("turn", { "posX": 0, "posY": 0 })
	}
	else if (board_data[posx][posy] == 'x' || board_data[posx][posy] == 'y') {
		socket.emit("turn", { "posX": posx, "posY": posy })
	}
	else {
		socket.emit("turn", { "posX": posx, "posY": posy });
		var img = document.createElement('img');
		img.setAttribute('class', 'game_circle');
		img.setAttribute('src', 'https://pic.onlinewebfonts.com/svg/img_416983.png');
		document.getElementById('squareB').appendChild(img);
	}

}
socket.emit("turn", { "posX": 0, "posY": 0 })
socket.emit("turn", { "posX": 0, "posY": 0 })


// also it has game_draw, game_won events.......