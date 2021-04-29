import './App.css';
import { Component } from 'react';
import Portfolio from './portfolio'
import Transaction from './transaction'
import socketIOClient from "socket.io-client";
class App extends Component {

  constructor() {
    super()
    this.state = {
      totalPortfolioValue: 0,
      portfolioValues: [],
      initialInvestment: 1000000,

    }

  }

  componentDidMount() {
    /*this.eventSource.addEventListener("portFolioValues", e =>
      this.updateState(JSON.parse(e.data)))*/
    const url = "/"
    this.socket = socketIOClient(url)

    this.socket.on("connect", () => {
      console.log("Socket Connected");
    });

    this.socket.on("portfolio", data => {
      console.log("hello")
      console.log(data);
      this.updateState(data)
    })  
  }

  componentDidUnmount() {
    this.socket.off("portfolio")
  }
  updateState = (data) => {
    this.setState({
      portfolioValues: [...this.state.portfolioValues, data],
      totalPortfolioValue: data["y"]
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
