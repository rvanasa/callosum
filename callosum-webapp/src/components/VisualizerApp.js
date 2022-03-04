import React, {useState} from 'react';
import Visualizer from './Visualizer';
import {Button} from 'react-bootstrap';

// Deprecated

export default function VisualizerApp() {
    const [started, setStarted] = useState(false);

    return (
        <div>
            {started ? (
                <Visualizer/>
            ) : (
                <div className="d-inline-block mx-auto">
                    <Button
                        size="lg"
                        variant="outline-primary"
                        style={{margin: 100, padding: '30vh 30vw'}}
                        onMouseDown={() => setStarted(true)}>
                        Start
                    </Button>
                </div>
            )}
        </div>
    );
}
