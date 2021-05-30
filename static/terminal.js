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
socket.on("get_board", function (data) {
    console.log(data);
});
socket.on("player_data", function (data) {
    player_data = data
    console.log(player_data);
});
socket.emit("turn", { "posX": 0, "posY": 0 })
socket.emit("turn", { "posX": 0, "posY": 0 })