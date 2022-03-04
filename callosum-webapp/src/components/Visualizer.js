import React from 'react';

const audioUrl = process.env.PUBLIC_URL + '/audio/A.ogg';

const [xCount, yCount] = [40, 40];

const mod = (a, b) => ((a % b) + b) % b;

const round = (a, d) => {
    const factor = 10 ** d;
    return Math.round(a * factor) / factor;
};

export default function Visualizer() {

    const rows = [];
    const items = [];
    for(let y = 0; y < yCount; y++) {
        const row = [];
        for(let x = 0; x < xCount; x++) {
            const item = {
                bind(ref) {
                    if(!ref) {
                        return;
                    }
                    this._ref = ref;
                },
                update(frequencies) {
                    const [xf, yf] = [x / xCount, y / yCount];
                    const [xc, yc] = [2 * xf - 1, 2 * yf - 1];
                    const r = Math.sqrt(xc ** 2 + yc ** 2);
                    const ct = Math.floor(frequencies.length / yCount);
                    const maxCt = y / yCount * frequencies.length;
                    let f = 0;
                    for(let i = Math.floor(yf * ct); i < maxCt; i++) {
                        f += frequencies[i];
                    }
                    f /= ct;
                    if(this._ref) {
                        const h = xf;
                        const s = Math.sqrt(r);
                        const l = f;
                        this._ref.style.background = `hsl(${round(mod(h, 1) * 360, 5)}deg, ${round(mod(s, 1) * 100, 5)}%, ${round(mod(l, 1) * 100, 5)}%)`;
                    }
                },
            };
            row.push(item);
            items.push(item);
        }
        rows.push(row);
    }

    const audio = new Audio(audioUrl);

    const context = new window.AudioContext();
    const source = context.createMediaElementSource(audio);

    const analyser = context.createAnalyser();
    source.connect(analyser);
    analyser.connect(context.destination);

    const filter = context.createBiquadFilter();
    filter.type = 'highpass';
    filter.frequency.value = 1e-5;
    filter.connect(analyser);

    // const osc = context.createOscillator();
    // osc.connect(filter);
    // osc.start(context.currentTime + 2);
    // osc.stop(context.currentTime + 4);

    audio.play().catch(console.error);//

    const frequencies = new Float32Array(analyser.frequencyBinCount);

    const redraw = () => {
        for(const item of items) {
            item.update(frequencies);
        }
    };

    const update = () => {
        analyser.getFloatTimeDomainData(frequencies);
        console.log(frequencies.length, frequencies);////
        redraw();
    };

    setInterval(update, 10);

    return (
        <div className="d-flex flex-column mt-4">
            {rows.map((row, i) => (
                <div key={i} className="d-flex justify-content-center">
                    {row.map((item, j) => (
                        <div
                            key={j}
                            ref={ref => item.bind(ref)}
                            style={{
                                display: 'inline-block',
                                width: 10,
                                height: 10,
                                margin: '1px',
                                // background: item.color,
                            }}/>
                    ))}
                </div>
            ))}
        </div>
    );
}
