import React from 'react/addons';

/*
 * @class Item
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

  /*
   * @method render
   * @returns {JSX}
   */
  render () {
    return <tr className="item"><td>{this.props.team.name}</td></tr>;
  }
}

// Prop types validation
Team.propTypes = {
  team: React.PropTypes.object.isRequired,
};

export default Team;
