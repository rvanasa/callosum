import React, {useContext} from 'react';
import {selectSong} from '../services/musicService';
import styled from 'styled-components';
import {SelectionContext} from '../contexts/SelectionContext';
import classNames from 'classnames';

const Container = styled.div`
    font-family: Lato, sans-serif;
    font-weight: 400;
    font-style: normal;
    border-radius: 2px;
    background: #FFF2;
    cursor: pointer;
    user-select: none;

    //&:hover {
    //    background: #FFF5;
    //}

    //&:active {
    //    color: #555;
    //    background: #FFF;
    //}

    &.selected {
        color: #000;
        background: #EEE;
        cursor: default;
    }
`;

export default function MusicItem({music}) {

    const {selected, setSelected} = useContext(SelectionContext);

    const isSelected = music.name === selected;

    const handleClick = () => {
        // if(isSelected) {
        //     return;
        // }
        setSelected(music.name);
        selectSong(music.name)
            .catch(err => {
                // TODO
                console.error(err);
            });
    };

    return (
        <Container
            className={classNames('d-flex px-3 py-2 my-2 align-items-center', isSelected && 'selected')}
            onClick={handleClick}>
            <div className="h4 mb-0 flex-grow-1">{music.artist}</div>
            <div className="h6 mb-0 text-end text-muted">{music.song}</div>
        </Container>
    );
}
