import './App.css';
import { Component } from 'react';
//import {TransitionGroup} from 'react-transition-group';
class Transaction extends Component {

    constructor() {
        super()
        this.state = {
            transactionData: []
        }
        this.eventSource = new EventSource("http://127.0.0.1:5000/events");
    }
    componentDidMount() {
        this.eventSource.addEventListener("transactionValues", e =>
      this.updateTransactionValues(JSON.parse(e.data)))
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