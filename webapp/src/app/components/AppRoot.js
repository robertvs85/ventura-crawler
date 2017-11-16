import React from 'react/addons';
import axios from 'axios';
import TeamList from './TeamList';

import config from '../../../config/app';

/*
 * @class AppRoot
 * @extends React.Component
 */
class AppRoot extends React.Component {

  constructor(props) {
    super(props);

    this.props.state = {
      teams: []
    };
  }

  /*
   * AppRootly PureRenderMixin
   *
   * in React 0.13 there is no way to attach mixins to ES6 classes
   * this is a workaround to solve this
   * http://facebook.github.io/react/blog/2015/01/27/react-v0.13.0-beta-1.html#mixins
   *
   * @method shouldComponentUpdate
   * @returns {Boolean}
   */
  shouldComponentUpdate () {
    return React.addons.PureRenderMixin.shouldComponentUpdate.apply(this, arguments);
  }

  componentDidMount() {
  	var config = {
	  headers: {
	  	'Access-Control-Allow-Methods': 'GET,PUT,PATCH,POST,DELETE',
	  	'Access-Control-Allow-Origin': '*',
	  	'Content-Type': 'application/json'
	  }
	};
    axios({
    	url: `http://localhost:8888/teams`,
    	headers: {"Access-Control-Allow-Origin": "*"},
    	method: 'GET'
    })
      .then(res => {
      	console.log("HELLOOOOO")
        const teams = res.teams;
        this.setState({ teams });
      });
  }

  /*
   * @method render
   * @returns {JSX}
   */
  render () {
    return <div className="appRoot">
      <h1>{config.title}</h1>
      <TeamList teams={this.props.state.teams} />
    </div>;
  }
}

// Prop types validation
AppRoot.propTypes = {
  state: React.PropTypes.object.isRequired,
};

export default AppRoot;
