import React from 'react/addons';
import Team from './Team';
import Col from 'react-bootstrap/lib/Col';

/*
 * @class TeamList
 * @extends React.Component
 */
class TeamList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      selected: null,
    };
  }


  showPlayers(team) {
    this.state.selected = team;
    this.setState(this.state)
  	this.props.showPlayers(team);
  }

  /*
   * @method render
   * @returns {JSX}
   */
  render () {
  	var that = this;
    return <Col sm={2} className="team_list" >
      <h2 className="text-info">Teams</h2>
      <div className="list-group">
        {this.props.teams.map(function (item, key) {
          return <Team showPlayers={that.showPlayers.bind(that)} team={item}
            active={that.state.selected == item.name? true: false}/>;
        })}
      </div>
    </Col>;
  }
}

// Prop types validation
TeamList.propTypes = {
  teams: React.PropTypes.object.isRequired,
};

export default TeamList;
