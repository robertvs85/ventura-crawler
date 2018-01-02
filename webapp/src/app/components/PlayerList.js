import React from 'react/addons';
import Player from './Player';

/*
 * @class PlayerList
 * @extends React.Component
 */
class PlayerList extends React.Component {

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
    return <div className="player_list column">
      <ul>
        {this.props.players.map(function (item, key) {
          return <Player key={key} player={item} />;
        })}
      </ul>
    </div>;
  }
}

// Prop types validation
PlayerList.propTypes = {
  players: React.PropTypes.object.isRequired,
};

export default PlayerList;
