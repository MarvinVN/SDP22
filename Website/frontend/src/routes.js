import React from 'react';
import { Switch, Route } from 'react-router-dom';

import App from './Mainpage';
//import nextpage from './nextpage';

const Main = () => {
  return (
    <Switch> {/* The Switch decides which component to show based on the current URL.*/}
      <Route exact path='/' component={App}></Route>
      {/*<Route exact path='/nextpage' component={nextpage}></Route>*/}
    </Switch>
  );
}

export default Main;