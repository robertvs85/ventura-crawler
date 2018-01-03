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
    var that = this;
    return <tr className="detailed_player_item">
      {this.props.columns.map(function (item, key) {
        return <td>{that.props.player[item]?that.props.player[item]:that.props.player.football_stats[item]}</td>;
      })}
      </tr>;
  }
}

// Prop types validation
Player.propTypes = {
  player: React.PropTypes.object.isRequired,
};

export default Player;
