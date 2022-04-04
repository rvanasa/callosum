import {io} from 'socket.io-client';

// const urlParams = new URLSearchParams(window.location.search); // TODO: refactor

// export const CONNECTION_URI = `${urlParams.get('host') || 'localhost'}:${urlParams.get('port') || 5000}`;

// const client = io(CONNECTION_URI);
const client = io('https://room-relay.herokuapp.com');

client.on('connect', () => {
    client.emit('join', 'callosum');
});

export async function sendMessage(msg) {
    client.emit('msg', msg);
}
