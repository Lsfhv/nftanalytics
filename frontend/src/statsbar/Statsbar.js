import './Statsbar.css';
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';


function Statsbar(x) {
    const params = useParams();
    
    const [_15m, set15m] =  useState(0);
    const [_1H, set1H] = useState(0);
    const [_1D, set1D] = useState(0);
    const [_1W, set1W] = useState(0);

    const [collection, setCollection] = useState('');

    const msg = {
        address: params['collection'],
        params: ["15m", "1H", "1D", "1W"]
    }
    useEffect(() => {
        const ws = new WebSocket('ws://127.0.0.1:5000/volume');

        const collectionName = async () => {
            const response = await fetch(
                'http://127.0.0.1:5000/slug/' + params['collection']);
            const data = await response.json();
            

            setCollection(collection => data.slug);
        };

        collectionName();

        ws.onopen = () => {
            ws.send(JSON.stringify(msg));
        };
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            switch (data.timeperiod) {
                case '15m':
                    set15m(_15m => data.volume);
                    break;
                case '1H':
                    set1H(_1H => data.volume);
                    break;
                case '1D':
                    set1D(_1D => data.volume);
                    break;
                case '1W':
                    set1W(_1W => data.volume);    
                default:
                    break;
            }
        }
    }, [params['collection']]);

    return (
        <div className='stats'>
            <span className='stats-component'>{collection}</span>
            <span className='stats-component'>15 Minutes: {_15m}</span>
            <span className='stats-component'>1 Hour: {_1H}</span>
            <span className='stats-component'>1 Day: {_1D}</span>
            <span className='stats-component'>1 Week: {_1W}</span>
        </div>
    );
}

export default Statsbar;