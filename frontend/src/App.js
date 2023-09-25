import './App.css';
import './Taskbar.js';

import SearchbarComponent from './mainbar/Searchbar';
import Statsbar from './statsbar/Statsbar';
import React from 'react';

import { BrowserRouter, Routes, Route, Link, useParams } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <div><SearchbarComponent></SearchbarComponent></div>
            <main>
                <Routes>
                    <Route path='/' element={<div>Just the home pages</div>}></Route>
                    <Route path='/:slug' element={<Statsbar/>}></Route>
                    <Route path='/x' element={<div>zee</div>}></Route>
                </Routes>
            </main>
        </BrowserRouter>
    );
}

export default App;
