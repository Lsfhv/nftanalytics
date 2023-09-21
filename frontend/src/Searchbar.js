function Searchbar() {
    return (
        <input
            type="text"
            placeholder='Collections'
            className = 'search-bar'
        />
    );
}

function SearchbarComponent() {
    return (
        <div className='search-bar-component'>
            <Searchbar></Searchbar>
        </div>
    );
}

export default SearchbarComponent;