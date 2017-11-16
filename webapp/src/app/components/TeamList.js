import React from 'react/addons';
import Team from './Team';

/*
 * @class Team
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

  /*
   * @method render
   * @returns {JSX}
   */
  render () {
    return <div className="cart">
      <table>
        {this.props.teams.map(function (item, key) {
          return <Team key={key} team={item} />;
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
