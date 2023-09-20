import logo from './logo.svg';
import './App.css';
import './Taskbar.js';
import Taskbar from './Taskbar.js';

import SearchbarComponent from './mainbar/Searchbar';

function App() {
    return (
        <div className='main'>
            <div><SearchbarComponent></SearchbarComponent></div>
            <div>Another one</div>
        </div>
    )
}

export default App;
