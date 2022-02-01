import React from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';

import MainPage from './MainPage'
import TeamPage from './TeamPage';

const ourroutes = () => {
  return (
    <div>
    <Routes> {/* The Switch decides which component to show based on the current URL.*/}
      <Route path='/TeamPage' component={TeamPage}/>
    </Routes>
    </div>
  );
}

export default ourroutes;