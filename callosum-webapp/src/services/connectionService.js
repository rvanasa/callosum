import {io} from 'socket.io-client';

export const CONNECTION_HOST = 'localhost:5000';

const client = io(CONNECTION_HOST);

export async function sendMessage(msg) {
    client.emit('msg', msg);
}
