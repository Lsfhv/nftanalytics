import './Searchbar.css';
import { useNavigate } from 'react-router-dom';
function Searchbar() {

    const navigate = useNavigate();
    
    async function handleSubmit(event) {   
        if (event.key == 'Enter') {
            event.preventDefault();
            const input = event.target.value;
            event.target.value = '';
            
            // const x = "http://127.0.0.1:5000/slug/" + input;
            // const response = await fetch(x);
            // // const data = await response.json();
            // const data = await response.json();
            
            // console.log(await data);
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