import React from 'react/addons';
import Team from './Team';

/*
 * @class TeamList
 * @extends React.Component
 */
class TeamList extends React.Component {

  /*
   * @method shouldComponentUpdate
   * @returns {Boolean}
   */
  shouldComponentUpdate () {
    return React.addons.PureRenderMixin.shouldComponentUpdate.apply(this, arguments);
  }

  showPlayers(team) {
  	this.props.showPlayers(team);
  }

  /*
   * @method render
   * @returns {JSX}
   */
  render () {
  	var that = this;
    return <div className="team_list column">
      <table>
        {this.props.teams.map(function (item, key) {
          return <Team showPlayers={that.showPlayers.bind(that)} key={key} team={item} />;
        })}
      </table>
    </div>;
  }
}

// Prop types validation
TeamList.propTypes = {
  teams: React.PropTypes.object.isRequired,
};

export default TeamList;
