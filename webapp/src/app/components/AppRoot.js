import React from 'react/addons';
import axios from 'axios';
import TeamList from './TeamList';
import PlayerList from './PlayerList';

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

        function compare(a,b) {
          if (isNaN(a.number) || a.number == null)
            return -1
          if (isNaN(b.number) || b.number == null)
            return 1

          if (parseInt(a.number) < parseInt(b.number))
            return -1;
          if (parseInt(a.number) > parseInt(b.number))
            return 1;
          return 0;
        }

        players.sort(compare);

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
    return <div className="appRoot">
      <h1 class="header">{config.title}</h1>
      <TeamList showPlayers={this.showPlayers} teams={this.state.teams} />
      <PlayerList players={this.state.players} />
    </div>;
  }
}

// Prop types validation
AppRoot.propTypes = {
  state: React.PropTypes.object.isRequired,
};

export default AppRoot;
