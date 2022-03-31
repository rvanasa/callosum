import axios from 'axios';
import {CONNECTION_URI, sendMessage} from './connectionService';
// noinspection ES6CheckImport
import {parse} from 'papaparse';

const musicListPromise = axios.get(`//${CONNECTION_URI}/static/features.csv`)
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
    })
    .catch(err => {
        console.error(err);
        return [{
            id: 0,
            name: 'Test 123',
            song: 'Test 123',
            artist: 'Test Artist',
            danceability: 0,
            energy: 0,
            liveness: 0,
            valence: 0,
        }, {
            id: 0,
            name: 'Test 456',
            song: 'Test 456',
            artist: 'Another Artist',
            danceability: 0,
            energy: 0,
            liveness: 0,
            valence: 0,
        }];
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