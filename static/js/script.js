var socket = io();
var player_data;

socket.on('connect', function () {
	socket.emit('join', { uname: new Date().toLocaleTimeString() }, (res) => {
		console.log('ok');
	});
});

socket.on("message", function (message) {
	console.log(message);
});

socket.on("get_board", function (board_data) {
	var img = document.createElement('img');
	console.log(board_data);

	var x = 0;
	var charCodeA = 'A'.charCodeAt(0);
	for (var i = 0; i < board_data.length; ++i) {
		for (var j = 0; j < board_data[0].length; ++j) {
			var targetElement = document.getElementById('square' + String.fromCharCode(charCodeA + x));

			if (board_data[i][j] == 'o') {
				img.setAttribute('class', 'game_circle');
				img.setAttribute('src', "https://pic.onlinewebfonts.com/svg/img_416983.png");
				if (!targetElement.firstChild) // if there's no symbol in the square
					targetElement.appendChild(img);
				console.log(board_data[i][j], i, j, x, 'square' + String.fromCharCode(charCodeA + x));
			} else if (board_data[i][j] == 'x') {
				img.setAttribute('class', 'game_cross');
				img.setAttribute('src', "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Red_X.svg/1200px-Red_X.svg.png");
				if (!targetElement.firstChild) // if there's no symbol in the square
					targetElement.appendChild(img);
				console.log(board_data[i][j], i, j, x, 'square' + String.fromCharCode(charCodeA + x));
			} else {
				// for '-', clear the square...
				while (targetElement.firstChild) {
					targetElement.removeChild(targetElement.lastChild);
				}
			}
			++x;
		}
	}
});

socket.on("player_data", function (data) {
	player_data = data;
	console.log("player char", player_data.game_character);
});

function fire(event, posX, posY) {
	console.log("turn", posX, posY);
	socket.emit("turn", { "posX": posX, "posY": posY });
}
// TODO: also it has game_draw, game_won events.......