import logo from './logo.svg';
import './App.css';
import './Taskbar.js';
import Taskbar from './Taskbar.js';

import SearchbarComponent from './mainbar/Searchbar';
import Statsbar from './statsbar/Statsbar';

import { BrowserRouter, Routes, Route, Link, useParams } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <div><SearchbarComponent></SearchbarComponent></div>
            <main>
                <Routes>
                    <Route path='/' element={<div>Just the home pages</div>}></Route>
                    <Route path='/:collection' element={<Statsbar></Statsbar>}></Route>
                </Routes>
            </main>
        </BrowserRouter>
    );
}

export default App;
