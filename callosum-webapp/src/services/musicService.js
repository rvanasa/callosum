import axios from 'axios';
import {CONNECTION_HOST, sendMessage} from './connectionService';
// noinspection ES6CheckImport
import {parse} from 'papaparse';

const musicListPromise = axios.get(`//${CONNECTION_HOST}/static/features.csv`)
    .then(async response => {
        const result = await new Promise((complete, error) => {
            parse(response.data, {
                dynamicTyping: true,
                skipEmptyLines: true,
                header: true,
                complete,
                error,
            });
        });
        return result.data
            .filter(row => row.name !== 'default')
            .map(row => ({
                ...row,
                // id: i,
                // // name: headerCase(row.name || ''),
                // start: new Date(row.start),
                // end: new Date(row.end),
            }));
    });

export async function findMusicList() {
    return musicListPromise;
}

export async function selectSong(name) {
    await sendMessage({
        type: 'select',
        name,
    });
}