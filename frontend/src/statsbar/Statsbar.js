import './Statsbar.css';
import { useParams } from 'react-router-dom';

function Statsbar() {
    const x = useParams();
    console.log("once");
    console.log(x);
    return (
        <>The stats bar</>
    );
}

export default Statsbar;