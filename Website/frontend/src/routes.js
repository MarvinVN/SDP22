import React from 'react';
import { Routes, Route, BrowserRouter, IndexRoute} from 'react-router-dom';

import MainPage from './Pages/MainPage'
import TeamPage from './Pages/TeamPage';

const ourroutes = () => {
  return (
    <div>
      <BrowserRouter>
      <Routes> {/* The Switch decides which component to show based on the current URL.*/}
        <IndexRoute component={MainPage}/>
        <Route path='/TeamPage' component={TeamPage}/>
      </Routes>
      </BrowserRouter>
    
    </div>
  );
}

export default ourroutes;