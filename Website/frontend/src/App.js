import React from 'react';
import Navbar from './NavBar/index';
import { BrowserRouter as Router, Routes, Route}from 'react-router-dom';

import MainPage from './Pages/MainPage';
import TeamPage from './Pages/TeamPage';
import Project from './Pages/Project';
import Documents from './Pages/Documents';
import Diagrams from './Pages/Diagrams'; 


function App() {
return (
    <Router>
      <Navbar/>
      <Routes>
          <Route exact path='/' exact element={<MainPage />} />
          <Route path='/TeamPage' element={<TeamPage/>} />
          <Route exact path='/Documents' exact element={<Documents />} />
          <Route exact path='/Diagrams' exact element={<Diagrams />} />
          <Route exact path='/Project' exact element={<Project />} />
      </Routes>
    </Router>
);
}
  
export default App;