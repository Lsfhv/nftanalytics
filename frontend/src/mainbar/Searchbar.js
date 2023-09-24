import './Searchbar.css';
import { useNavigate } from 'react-router-dom';
function Searchbar() {

    const navigate = useNavigate();
    
    function handleSubmit(event) {   
        if (event.key == 'Enter') {
            event.preventDefault();
            const input = event.target.value;
            navigate('/' + input);
        } 
    }

    return (
        <form onKeyDown={handleSubmit}>
            <input id='1' type='text' placeholder='Collections' className='search-bar' autoComplete='off'></input>
        </form>
    );
}

function SearchbarComponent() {
    return (
        <div className='search-bar-component'>
            <span className='place'>NFT Analytics</span>
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