import './App.css';
import { Component } from 'react';
import Portfolio from './portfolio'
import Transaction from './transaction'
class App extends Component {

  constructor() {
    super()
    this.state = {
      totalPortfolioValue: 0,
      portfolioValues: [],
      initialInvestment: 1000000,
      
    }
    this.eventSource = new EventSource("http://127.0.0.1:5000/events");

  }

  componentDidMount() {
    this.eventSource.addEventListener("portFolioValues", e =>
      this.updateState(JSON.parse(e.data)))
  }

  updateState = (data) => {
    this.setState({
      portfolioValues:[...this.state.portfolioValues, data],
      totalPortfolioValue:data["y"]
    })
  }

  thousandsSeparator(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  render() {
    return (
      <div className="App" >
        <div className="heading">
          AI Portfolio Manager
     </div>
        <div className="investment">
          <div>Initial investment</div>
          <div>${this.thousandsSeparator(this.state.initialInvestment)}</div>
        </div>
        <div className="portfolio-value">
          <div>Current Portfolio value</div>
          <div>${this.thousandsSeparator(this.state.totalPortfolioValue)}</div>
        </div>
        <div className="portfolio-graph">
          <Portfolio
            portfolioValues={this.state.portfolioValues}
            />
        </div>
        <div className="transaction-box">
        <Transaction />
     </div>
      </div>
    )
  }
}

export default App;
