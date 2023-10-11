import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import './ActivityTable.css';
function ActivityTable () {

    const params = useParams();

    const [transactions, setTransactions] = useState([]);

    useEffect(() =>{

        const ws = new WebSocket('ws://127.0.0.1:8080/trades'); 

        const collectionAddress = async () => {
            const response = await fetch('http://127.0.0.1:8080/getaddress?slug=' + params['slug']);            
            return response.json();
        }

        ws.onmessage = (event) => {
            let data = event.data;
            data = JSON.parse(data);
            data = data.map(i => {
                return [i['txHash'], i['src'].slice(0,7), i['dst'].slice(0,7), i['token_id'], i['value'] / 1e18];
            });
            setTransactions(transactions => data);
        }
    
        ws.onopen = async () => {
            const address = (await collectionAddress())['address']

            ws.send(JSON.stringify({address: address}))
        }

        return () => {
            ws.close(1000);
        }
    }, [params['slug']])

    function handleRowClick(event, index) {
        const nw = window.open("https://etherscan.io/tx/" +transactions[index][0]);
    }

    return (
        <div className="trades-container">
            <table className="trades">
                <thead>
                    <tr>
                        <th>Source</th>
                        <th>Destination</th>
                        <th>Token Id</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    {transactions.map((transaction, i)=>
                        <tr onClick={e => handleRowClick(e, i)}>
                            {transaction.slice(1).map(item=><td>{item}</td>)}
                        </tr>)}
                </tbody>
            </table>
        </div>
    );
}

export default ActivityTable;