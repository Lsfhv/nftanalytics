import './Searchbar.css';
import { useNavigate } from 'react-router-dom';
function Searchbar() {

    const navigate = useNavigate();
    
    async function handleSubmit(event) {   
        if (event.key == 'Enter') {
            event.preventDefault();
            const input = event.target.value;

            let response = await fetch("http://127.0.0.1:8080/getaddress?slug=" + input)
            response = await response.json()
            if (response['address'] != '') {
                event.target.value = '';
                navigate('/' + input);
            } 
        } 
    }

    return (
        <form onKeyDown={handleSubmit}>
            <input id='1' type='text' placeholder='Collections' className='search-bar' autoComplete='off'></input>
        </form>
    );
}

function SearchbarComponent() {
    const navigate = useNavigate();
    function homeClick() {
        navigate('/')
    }

    return (
        <div className='search-bar-component'>
            <span className='place' onClick={homeClick}>NFT Analytics</span>
            <span className='place'>
                Place Holder
            </span>
            <span className='place'> 
                Place holder
            </span>
            <span className='place'>
                Place holder
            </span>
            <span className='place' >
                <Searchbar></Searchbar>
            </span>
        </div>
    );
}

export default SearchbarComponent;