import './Searchbar.css';
function Searchbar() {
    function handleSubmit(event) {   
        if (event.key == 'Enter') {
            event.preventDefault();
            const input = event.target.value;
            console.log(input);
        } 
    }

    return (
        <form onKeyDown={handleSubmit} >
            <input id='1' type='text' placeholder='Collections' className='search-bar'></input>
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