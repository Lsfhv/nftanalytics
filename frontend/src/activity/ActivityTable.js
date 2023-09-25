import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
function ActivityTable () {

    const params = useParams();

    const [transactions, setTransactions] = useState([]);

    const getActivity = async () => {

        const response = await fetch('http://127.0.0.1:5000/activity/' + params['slug']);
        let now = Date.now() / 1000;
        let data = await response.json();
        data = await data.result;
        data = data.map(i => i.slice(2));
        data = data.map(i => [i[0], i[1].substring(2, 8), i[2].substring(2,8), i[3] + i[4] + i[5], (now - i[6]) / 60 ]);

        setTransactions(transactions => data);
        return data;
    }

    useEffect(() =>{
        getActivity()
    }, [params['slug']])

    return (
        <div>
            <div>The activity table.</div>
            <table>
                <thead>
                    <tr>
                        <th>id</th>
                        <th>From</th>
                        <th>To</th>
                        <th>value</th>
                        <th>time</th>
                    </tr>
                </thead>
                <tbody>
                    {transactions.map(transaction=> <tr>
                        
                        {transaction.map(item=><td>{item}</td>)}
                    </tr>)}
                </tbody>

            </table>
        </div>
    );
}

export default ActivityTable;