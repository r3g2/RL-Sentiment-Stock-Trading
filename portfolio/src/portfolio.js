import './App.css';
import { Component } from 'react';
import {ResponsiveLine} from '@nivo/line';

class Portfolio extends Component {

    constructor(props) {
      super(props)
       
    }
  
    render() {
      return (
        <div style={{ maxWidth: "97%", margin: "0 auto", height: "100%" }}>
            {console.log(this.props.portfolioValues)}
         {this.props.portfolioValues&&<ResponsiveLine
        curve="monotoneX"
          data={[
            {
              id: "repos",
              color: '#0077B5',
              data: this.props.portfolioValues
            }
          ]}
          axisBottom={{
            orient: 'bottom',
            legend: 'time',
            legendOffset: 36,
            legendPosition: 'middle'
        }}
        axisLeft={{
            orient: 'left',
            legend: 'Portfolio Values',
            legendOffset: -50,
            legendPosition: 'middle'
        }}
          margin={{ top: 10, right: 25, bottom: 40, left: 60 }}
          xScale={{ type: "point" }}
          yScale={{
            type: "linear",
            min: "auto",
            max: "auto"
          }}
           colors='#0077B5' 
          enableArea={false}
          useMesh={true}
          enablePoint={false}
          pointSize={1}
          enableGridX={false}
        />}
        </div>
      )
    }
}

export default Portfolio;
