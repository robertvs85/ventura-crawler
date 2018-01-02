import React from 'react/addons';

/*
 * @class Player
 * @extends React.Component
 */
class Player extends React.Component {

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
    return <li className="player_item">
      <span className="player_nickname">{this.props.player.nickname}</span> -
      <span className="player_number"> {this.props.player.number}</span> -
      <span className="player_fullname"> {this.props.player.full_name}</span></li>;
  }
}

// Prop types validation
Player.propTypes = {
  player: React.PropTypes.object.isRequired,
};

export default Player;
