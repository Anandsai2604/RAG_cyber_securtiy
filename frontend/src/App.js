import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginRegister from './cyber/login';
import Home from './cyber/home';
import Main from './cyber/main';
import Question from './cyber/qna';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginRegister />} />
                <Route path="/home" element={<Home />} />
                <Route path="/main" element={<Main />} />
                <Route path="/qna" element={<Question />} />
            </Routes>
        </Router>
    );
}

export default App;
