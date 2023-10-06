import './Statsbar.css';
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';

function Statsbar() {
    const params = useParams();
    
    const [_15m, set15m] = useState(0);
    const [_1H, set1H] = useState(0);
    const [_1D, set1D] = useState(0);
    const [_1W, set1W] = useState(0);

    const [collection, setCollection] = useState('Loading');

    const msg = {
        slug: params['slug'],
        params: ["15m", "1H", "1D", "1W"]
    }
    useEffect(() => {
        const collectionName = async () => {
            const response = await fetch(
                'http://127.0.0.1:8080/getdisplayname?slug=' + params['slug']);
            const data = await response.json();
            
            setCollection(collection => data['display_name']);
        };

        collectionName();

    }, [params['slug']]);

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