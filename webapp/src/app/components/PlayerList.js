import React from 'react/addons';
import Player from './Player';
import Table from 'react-bootstrap/lib/Table';
import Col from 'react-bootstrap/lib/Col';

/*
 * @class PlayerList
 * @extends React.Component
 */
class PlayerList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
       columns: [
        'nickname','position','number', 'full_name', 'birth_date','city', 'nationality',
        'Altura', 'Peso', 'Minutos', 'Goles', 'Asistencias', 'Tiros'
       ],
       columnLabels: {
         'nickname': 'Name',
         'position': 'Position',
         'number': 'Number',
         'full_name': 'Full Name',
         'birth_date': 'Birth Date',
         'city': 'Birth City',
         'nationality': 'Nationality',
         'Altura': 'Height',
         'Peso': 'Weight',
         'Minutos': 'Minutes',
         'Goles': 'Goals',
         'Asistencias': 'Assists',
         'Tiros': 'Shots'
       }
    }
  }

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
    return <Col sm={10} className="player_detailed_list">
      <h2 className="text-info">Players</h2>
      <Table responsive condensed bordered hover>
        <thead>
          <tr>
            {this.state.columns.map(function (item, key) {
            return <th>{that.state.columnLabels[item]}</th>;
            })}
          </tr>
        </thead>
        <tbody>
          {this.props.players.map(function (item, key) {
            if(item.position != 'Entrenador')
              return <Player key={key} player={item} columns={that.state.columns}/>;
          })}
        </tbody>
      </Table>
    </Col>;
  }
}

// Prop types validation
PlayerList.propTypes = {
  players: React.PropTypes.object.isRequired,
};

export default PlayerList;
