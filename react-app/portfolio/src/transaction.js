import './App.css';
import { Component } from 'react';
//import {TransitionGroup} from 'react-transition-group';
import socketIOClient from "socket.io-client";
class Transaction extends Component {

    constructor() {
        super()
        this.state = {
            transactionData: []
        }
    }
    componentDidMount() {
    const url = "http://127.0.0.1:5000/"
    this.socket = socketIOClient(url)
      this.socket.on('transaction', data=> {
          console.log(data)
          this.updateTransactionValues(data)
      })
    }
    componentDidUnmount() {
        this.socket.off('transaction')
    }
    updateTransactionValues = (data) => {
        this.setState({
            transactionData:[...data,...this.state.transactionData ]
        })
    }

    render() {
        return (
            <div>
                {this.state.transactionData.map((obj) => {
                    
                    return(<div className="transaction">
                        
                    <div>{obj.tick}</div>
                    <div>{obj.operation}</div>
                    <div>{obj.qty}</div>
                    
                    </div>
                    
                    )
                })
                
                }           
            </div>
            
        )
    }
}

export default Transaction;