import React, {useEffect, useState} from 'react';
import {findMusicList} from '../services/musicService';
import styled, {keyframes} from 'styled-components';
import MusicItem from './MusicItem';
import {SelectionContext} from '../contexts/SelectionContext';
import shuffle from '../utils/shuffle';
import classNames from 'classnames';

const startAnimation = keyframes`
    0% {
        opacity: 0;
    }
`;

const shuffleAnimation = keyframes`
    0% {
        opacity: .5;
        transform: scale(1);
    }
    10% {
        transform: scale(.99);
    }
`;

// Main header
const StyledHeader = styled.h1`
    font-family: Futura, Jost, sans-serif;
    color: #EEE;
    text-align: center;
    font-size: 8rem;
    //font-weight: 100;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0;
    user-select: none;
    cursor: pointer;
    animation: ${startAnimation} 1s forwards ease-out;

    &.shuffle {
        animation: ${shuffleAnimation} 1s forwards ease-out;
    }
`;

// Everything below the header
const StyledContent = styled.div`
    margin: auto;
    max-width: 60rem;
`;

// Scroll area for song options
const StyledItemContainer = styled.div`
    max-height: 26rem;
    overflow-y: auto;
`;

export default function App() {
    const [searchText, setSearchText] = useState('');
    const [musicList, setMusicList] = useState([]);
    const [selected, _setSelected] = useState(null);
    const [shuffleKey, setShuffleKey] = useState(0);

    useEffect(() => {
        findMusicList()
            .then(musicList => setMusicList(shuffle([...musicList])))
            .catch(err => console.error(err));
    }, []);

    // if(err) {
    //     return (
    //         <div className="h1 pt-5 mt-5 text-center">Something unexpected happened!</div>
    //     );
    // }

    const filterMusic = music => {
        if(!searchText) {
            return true;
        }
        const text = searchText.toLowerCase().trim();
        const parts = [music.genre, music.artist, music.song];
        return parts.some(part => String(part ?? '').toLowerCase().includes(text));
    };

    const setSelected = selected => {
        _setSelected(selected);
        // setShuffleKey(Math.random());
    };

    const shuffleMusic = () => {
        setMusicList(shuffle([...musicList]));
        setShuffleKey(Math.random());
        setSearchText('');
    };

    // let scrollRef;
    // const sortMusic = () => {
    //     const target = musicList.find(music => music.name === selected);
    //     if(!target) {
    //         return;
    //     }
    //     setShuffleKey(null);
    //     setSearchText('');
    //     setMusicList(musicList
    //         .map(music => ({
    //             ...music,
    //             distance: /*Math.sqrt*/(
    //                 (target.danceability - music.danceability) ** 2 +
    //                 (target.energy - music.energy) ** 2 +
    //                 (target.liveness - music.liveness) ** 2 +
    //                 (target.valence - music.valence) ** 2
    //             ),
    //         }))
    //         .sort((a, b) => a.distance - b.distance));
    //     if(scrollRef) {
    //         scrollRef.scrollTop = 0;
    //     }
    // };

    return (
        <SelectionContext.Provider value={{selected, setSelected}}>
            <div className="mx-2 mt-3 mt-md-4">
                <StyledHeader
                    key={shuffleKey}
                    className={classNames('mb-3 text-center', shuffleKey && 'shuffle')}
                    // onClick={() => selected && shuffleKey ? sortMusic() : shuffleMusic()}>
                    onClick={() => shuffleMusic()}>
                    Callosum
                </StyledHeader>
                <StyledContent>
                    <div className="py-2">
                        <input
                            type="text"
                            className="form-control form-control-lg rounded-0"
                            placeholder="search for music..."
                            value={searchText}
                            onFocus={e => e.target.select()}
                            onChange={e => setSearchText(e.target.value)}
                        />
                    </div>
                    <StyledItemContainer
                        // ref={ref => scrollRef = ref}
                        className="pe-2">
                        {musicList
                            .filter(filterMusic)
                            .map(music => (
                                <MusicItem key={music.name} music={music}/>
                            ))}
                    </StyledItemContainer>
                </StyledContent>
            </div>
        </SelectionContext.Provider>
    );
}
