import React from 'react/addons';

/*
 * @class Team
 * @extends React.Component
 */
class Team extends React.Component {

  /*
   * @method shouldComponentUpdate
   * @returns {Boolean}
   */
  shouldComponentUpdate () {
    return React.addons.PureRenderMixin.shouldComponentUpdate.apply(this, arguments);
  }

  showPlayers () {
    this.props.showPlayers(this.props.team.name);
  }

  /*
   * @method render
   * @returns {JSX}
   */
  render () {
    return <tr className="item"><td>{this.props.team.name} <button onClick={this.showPlayers.bind(this)}>See players</button></td></tr>;
  }
}

// Prop types validation
Team.propTypes = {
  team: React.PropTypes.object.isRequired,
};

export default Team;
