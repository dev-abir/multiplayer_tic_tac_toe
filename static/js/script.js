var socket = io();
var player_data;

// TODO: these should be const, but it gives error...
var CIRCLE_IMG_URL = "https://pic.onlinewebfonts.com/svg/img_416983.png";
var CROSS_IMG_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Red_X.svg/1200px-Red_X.svg.png";

// preload images
var img0 = new Image();
img0.setAttribute('src', CIRCLE_IMG_URL);
var img1 = new Image();
img1.setAttribute('src', CROSS_IMG_URL);
var b_dat = null;

socket.on('connect', function () {
	socket.emit('join', { uname: uname }, (res) => {
		console.log('ok');
	});
});

socket.on("message", function (message) {
	var msg = document.createElement('h2');
	var txt = document.createTextNode(message);
	msg.appendChild(txt);
	msg.setAttribute('id',"player_msg");
	document.getElementById('msg_scr').appendChild(msg);
	console.log(message);
});

socket.on("get_board", function (board_data) {
	b_dat = board_data;
	console.log(board_data);
	var x = 0;
	var charCodeA = 'A'.charCodeAt(0);
	for (var i = 0; i < board_data.length; ++i) {
		for (var j = 0; j < board_data[0].length; ++j) {
			var targetElement = document.getElementById('square' + String.fromCharCode(charCodeA + x));

			if (board_data[i][j] == 'o') {
				if (!targetElement.firstChild) { // if there's no symbol in the square
					// create new object, recycling old ones can cause problems...
					var circleImg = document.createElement("img");
					circleImg.setAttribute('class', 'game_circle');
					circleImg.setAttribute('src', CIRCLE_IMG_URL);
					targetElement.appendChild(circleImg);
				}
			} else if (board_data[i][j] == 'x') {
				if (!targetElement.firstChild) { // if there's no symbol in the square
					// create new object, recycling old ones can cause problems...
					var crossImg = document.createElement("img");
					crossImg.setAttribute('class', 'game_cross');
					crossImg.setAttribute('src', CROSS_IMG_URL);
					targetElement.appendChild(crossImg);
				}
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
	console.log(player_data);
	var msg = document.createElement('h2');
	var txt = document.createTextNode(player_data.uname+" is in the game");
	msg.appendChild(txt);
	msg.setAttribute('id',"player_msg");
	document.getElementById('msg_scr').appendChild(msg);
});

socket.on("game_draw", function (message) {
	console.log(message);
	var msg = document.createElement('h2');
	var txt = document.createTextNode("GAME DRAW!!\nrefreshing page within 3 seconds for a new game...");
	msg.appendChild(txt);
	msg.setAttribute('id',"player_msg");
	document.getElementById('msg_scr').appendChild(msg);
	setTimeout(function () {
		window.location.reload();
	}, 3 * 1000);
});

socket.on("game_won", function (message) {
	console.log(message);
	console.log("refreshing page within 3 seconds for a new game...");
	var msg = document.createElement('h2');
	var txt = document.createTextNode(message+" \n refreshing page within 3 seconds for a new game...");
	msg.appendChild(txt);
	msg.setAttribute('id',"player_msg");
	document.getElementById('msg_scr').appendChild(msg);
	setTimeout(function () {
		window.location.reload();
	}, 3 * 1000);
});

function fire(event, posX, posY) {
	console.log("turn", posX, posY);
	socket.emit("turn", {
		"posX": posX,
		"posY": posY,
		"room_id": player_data.room_id // TODO: cuz of cookie-related bug in the back-end, delete this after fix
	});
}
