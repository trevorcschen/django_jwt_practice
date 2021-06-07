import './styles/App.css';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom'
import Login from './components/Login'
import SignUp from './components/SignUp'
import Home from './components/Home'
import {useEffect, useState} from 'react'
import AuthService from './services/authService'

function App() {
  const [isAuth , setAuth] = useState(false)
  console.log(isAuth)
  const handleLogOut = () =>
    {
      console.log('logout')
      AuthService.logout({setAuth})

    }
  useEffect(() =>
  {
    console.log('validating')
    AuthService.validateAuth({setAuth})
  }, [])
  return (
<Router>
    <div className="App">
      <nav className="navbar navbar-expand-lg navbar-light fixed-top">
        <div className="container">
          
          <Link className="navbar-brand" to={"/sign-in"}>positronX.io</Link>
          <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
            <ul className="navbar-nav ml-auto">
              {isAuth === false &&
              <div style={{display:'flex'}}>
                  <li className="nav-item">
                        <Link className="nav-link" to={"/sign-in"}>Login</Link>
                  </li>
                  <li className="nav-item">
                        <Link className="nav-link" to={"/sign-up"}>Sign up</Link>
                  </li>
              </div>
              }
              
              {isAuth && 
              <li className="nav-item">
                <Link className="nav-link" to="/sign-in" onClick={handleLogOut}>Log out</Link>
              </li>
              }
            </ul>
          </div>
        </div>
      </nav>

      <div className="auth-wrapper">
        <div className="auth-inner">
          <Switch>
            <Route exact path='/' component={Home} />
            <Route exact path="/sign-in" render={() => <Login isAuth ={isAuth} handleAuth = {setAuth} />} />
            <Route path="/sign-up" component={SignUp} />
            {/* <Route path="/home" component={Home} /> */}
          </Switch>
        </div>
      </div>
    </div></Router>

  );
}


export default App;
