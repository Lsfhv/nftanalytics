import './App.css';
import './Taskbar.js';
import './styles/TableStyles.css'

import SearchbarComponent from './mainbar/Searchbar';
import Statsbar from './statsbar/Statsbar';
import React from 'react';
import ActivityTable from './activity/ActivityTable';

import CollectionTable from './collections/CollectionsTable';

import { BrowserRouter, Routes, Route, Link, useParams } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <div><SearchbarComponent></SearchbarComponent></div>
            <main>
                <Routes>
                    <Route path='/' element={
                        <CollectionTable></CollectionTable>
                    }></Route>
                    <Route path='/:slug' element={
                        <div>
                            <div><Statsbar></Statsbar></div>
                            <div><ActivityTable></ActivityTable></div>
                        </div>
                    }></Route>
                </Routes>
            </main>
        </BrowserRouter>
    );
}

export default App;
