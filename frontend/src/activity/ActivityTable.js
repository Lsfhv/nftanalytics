import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import './ActivityTable.css';
function ActivityTable () {

    const params = useParams();

    const [transactions, setTransactions] = useState([]);

    useEffect(() =>{

        const ws = new WebSocket('ws://127.0.0.1:5000/trades'); 

        const collectionAddress = async () => {
            const response = await fetch('http://127.0.0.1:8080/getaddress?slug=' + params['slug']);            
            return response.json();
        }

        ws.onmessage = (event) => {
            let data = event.data;
            data = JSON.parse(data);

            // data = data.map(i => {
            //     let dateTime = new Date(i[7] * 1000);
            //     return [i[1], i[2], i[3], i[4] / 1e18, `${dateTime.getDay() + 1}/${dateTime.getMonth() + 1}/${dateTime.getFullYear()} ${dateTime.getHours()}:${dateTime.getMinutes()}:${dateTime.getSeconds()}`];
            // });

            data = data.map(i => {
                let dateTime = new Date(i[7] * 1000);
                return [i[1], i[2], i[3], i[4] / 1e18];
            });

            setTransactions(transactions => data);
        }
    
        ws.onopen = async () => {

            const address = (await collectionAddress())['address']

            ws.send(JSON.stringify({address: address}))
        }

        return () => {
            ws.close();
        }
    }, [params['slug']])

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
                        <tr>
                            {transaction.map(item=><td>{item}</td>)}
                        </tr>)}
                </tbody>
            </table>
        </div>
    );
}

export default ActivityTable;