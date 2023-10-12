import './CollectionsTable.css';

import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
function CollectionTable() {

    const [collections, setCollections] = useState([]);
    const navigate = useNavigate();
    useEffect(() => {

        const getCollections = async () => {
            let r = await fetch("http://127.0.0.1:8080/getcollections");
            return r.json()
        }

        const c = async () => {
            let data = await getCollections();
            setCollections(collections => data);
        }
        c()
    }, []);

    function handleClick(event, index) {
        const slug = collections[index]['collectionSlug']
        navigate('/' + slug)
    }

    return (
        <>
            <table className='collections-table'>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Owners</th>
                        <th>Supply</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        collections.map((collection, i) => 
                            <tr onClick={e => handleClick(e,i)}>
                                <td>{collection['collectionName']}</td>
                            </tr>
                        )
                    }
                </tbody>
            </table>
        </>
    )
}

export default CollectionTable;