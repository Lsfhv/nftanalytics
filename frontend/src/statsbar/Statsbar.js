import './Statsbar.css';
import { useParams } from 'react-router-dom';

function Statsbar() {
    const collection = useParams();
    // console.log(collection['collection']);
    return (
        <div>
            The stats bar.
        </div>
    );
}

export default Statsbar;