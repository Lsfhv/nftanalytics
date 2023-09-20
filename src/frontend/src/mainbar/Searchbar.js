import './Searchbar.css';
function Searchbar() {
    function handleSubmit(e) {
        // console.log(e.);
        e.preventDefault();
        const formData = new FormData(e.target);
        var input = formData.get('input');
    }

    return (
        <form onSubmit={handleSubmit}>
            <input name='input' type='text' placeholder='Collections' className='search-bar'></input>
        </form>
    );
}



function SearchbarComponent() {
    return (
        <div className='search-bar-component'>
            <span className='place'>
                Place holder
            </span>
            <span className='place'> 
                Place holder
            </span>
            <span className='place'>
                Place holder
            </span>
            <span className='search-bar-span-container'>
                <Searchbar></Searchbar>
            </span>
        </div>
    );
}

export default SearchbarComponent;