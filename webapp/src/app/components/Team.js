import React from 'react/addons';

/*
 * @class Team
 * @extends React.Component
 */
class Team extends React.Component {

  constructor(props) {
    super(props);
  }

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
    return <a className={this.props.active ? 'active list-group-item': 'list-group-item'} onClick={this.showPlayers.bind(this)}>{this.props.team.name}</a>;
  }
}

// Prop types validation
Team.propTypes = {
  team: React.PropTypes.object.isRequired,
};

export default Team;
