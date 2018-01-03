import React from 'react/addons';
import axios from 'axios';
import TeamList from './TeamList';
import PlayerList from './PlayerList';
import Grid from 'react-bootstrap/lib/Grid';
import Row from 'react-bootstrap/lib/Row';

import config from '../../../config/app';

/*
 * @class AppRoot
 * @extends React.Component
 */
class AppRoot extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      teams: [],
      players: []
    };

    this.showPlayers = this.showPlayers.bind(this);
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

  showPlayers(team) {
  	axios({
    	url: `/soccer_api/players/` + team + `/`,
    	method: 'GET'
    })
      .then(res => {
        var players = res.data.players;
        this.setState({'players':players});
      });
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
    return <Grid className="appRoot">
        <h1 className="header text-primary">{config.title}</h1>
        <Row>
          <TeamList showPlayers={this.showPlayers} teams={this.state.teams} />
          <PlayerList players={this.state.players} />
        </Row>
    </Grid>;
  }
}

// Prop types validation
AppRoot.propTypes = {
  state: React.PropTypes.object.isRequired,
};

export default AppRoot;
