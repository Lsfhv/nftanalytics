import './Statsbar.css';
import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';

const FIFTEENMINUTES = 15 * 60;
const ONEHOUR = 60 * 60; 
const ONEDAY = 24 * ONEHOUR;
const ONEWEEK = 7 * ONEDAY;

function Statsbar() {
    const params = useParams();
    
    const [_15m, set15m] = useState(0);
    const [_1H, set1H] = useState(0);
    const [_1D, set1D] = useState(0);
    const [_1W, set1W] = useState(0);

    const [collection, setCollection] = useState('Loading');

    useEffect(() => {
        const setCollectionName = async () => {
            const response = await fetch(
                'http://127.0.0.1:8080/getdisplayname?slug=' + params['slug']);
            const data = await response.json();
            
            setCollection(collection => data['display_name']);
        };
        const collectionAddress = async () => {
            const response = await fetch('http://127.0.0.1:8080/getaddress?slug=' + params['slug']);            
            return response.json();
        }

        const ws = new WebSocket('ws://127.0.0.1:8080/volume');
        
        ws.onopen = async () => {
            const address = (await collectionAddress())['address']

            ws.send(JSON.stringify({address: address, timePeriods: [
                FIFTEENMINUTES, 
                ONEHOUR, 
                ONEDAY, 
                ONEWEEK
            ]}))
        }

        ws.onmessage = (event) => {
            let data = event.data;
            data = JSON.parse(data);

            if (data['timePeriod'] == FIFTEENMINUTES) {
                set15m(_15m => (data['volume'] / 1e18).toFixed(2))
            } else if (data['timePeriod'] == ONEHOUR) {
                set1H(_1H=>(data['volume'] / 1e18).toFixed(2))
            } else if (data['timePeriod'] == ONEDAY) {
                set1D(_1D => (data['volume'] / 1e18).toFixed(2));
            } else if (data['timePeriod'] == ONEWEEK){
                set1W(_1W => (data['volume'] / 1e18).toFixed(2));
            }
        } 

        setCollectionName();

        return () => {
            ws.close();
        }

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