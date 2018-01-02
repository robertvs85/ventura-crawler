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

    this.state = {
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
    axios({
    	url: `/soccer_api/teams`,
    	method: 'GET'
    })
      .then(res => {
        var teams = res.data.teams;

        function compare(a,b) {
          if (a.name < b.name)
            return -1;
          if (a.name > b.name)
            return 1;
          return 0;
        }

        teams.sort(compare);

        this.setState({'teams':teams});
      });
  }

  /*
   * @method render
   * @returns {JSX}
   */
  render () {
    return <div className="appRoot">
      <h1>{config.title}</h1>
      <TeamList teams={this.state.teams} />
    </div>;
  }
}

// Prop types validation
AppRoot.propTypes = {
  state: React.PropTypes.object.isRequired,
};

export default AppRoot;
