import React from 'react';
import Navbar from './NavBar/index';
import { BrowserRouter as Router, Routes, Route}from 'react-router-dom';

import MainPage from './Pages/MainPage';
import TeamPage from './Pages/TeamPage';

  
function App() {
return (
    <Router>
      <Navbar/>
      <Routes>
          <Route exact path='/' exact element={<MainPage />} />
          <Route path='/TeamPage' element={<TeamPage/>} />
      </Routes>
    </Router>
);
}
  
export default App;