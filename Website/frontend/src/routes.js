import React from 'react';
import { Routes, Route, BrowserRouter, IndexRoute} from 'react-router-dom';

import MainPage from './Pages/MainPage'
import TeamPage from './Pages/TeamPage';
import Project from './Pages/Project';
import Diagrams from './Pages/Diagrams';
import Documents from './Pages/Documents';

const ourroutes = () => {
  return (
    <div>
      <BrowserRouter>
      <Routes> {/* The Switch decides which component to show based on the current URL.*/}
        <IndexRoute component={MainPage}/>
        <Route path='/TeamPage' component={TeamPage}/>
        <Route path='/Project' component={Project}/>
        <Route path='/Diagrams' component={Diagrams}/>
        <Route path='/Documents' component={Documents}/>
      </Routes>
      </BrowserRouter>
    
    </div>
  );
}

export default ourroutes;