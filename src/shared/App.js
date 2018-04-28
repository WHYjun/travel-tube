import React, { Component } from 'react';
import { Route } from 'react-router-dom';
import { Home, Tour } from '../pages';


class App extends Component {
    render() {
        return (
            <div>
                <Route exact path="/" component={Home}/>
                <Route path="/tour" component={Tour}/>
            </div>
        );
    }
}

export default App;