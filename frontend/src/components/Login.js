import {useEffect, useState} from 'react';
import axios from 'axios'
import { useHistory } from "react-router-dom";

const Login = ({isAuth, handleAuth}) => {
    const history = useHistory();
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.withCredentials = true;
        // const [credentials, setCredentials] = useState({"email": "admin@admin.com", "password": "admin"})
    const [credentials , setCredentials] = useState({})

    let axiosConfig = {
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
            // 'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIyMjI4MTg0LCJqdGkiOiI4YTY5YWVhYWJlNDY0YjI1YTk0ODEwOGEzOWRiYjFiOSIsInVzZXJfaWQiOjEsIm5hbWUiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIiwicGFzc3dvcmQiOiJwYmtkZjJfc2hhMjU2JDI2MDAwMCR5NHBOUlV4ZWZmTkZGUktHZmF2dHI5JE1pNXE2UXpkQmF0aDdBSW51RGk3VmFnNE03TzRtTHh2bnhBbU9IZ0ZmUVU9IiwiaXNfc3RhZmYiOnRydWV9.ykA7th-QW_z2hF5y7YvF8_tHVXY4BHiW2hFE679D_DA"
        }
      };

    useEffect(() => 
    {

        axios.get("http://127.0.0.1:8000/api/v1/articles", axiosConfig)
        .then((response) => console.log(response.data))
        .catch((err) => console.log(err))
        // console.log("login here")
    }, [])
    const handlerLogin = (e) =>
    {
        e.preventDefault()
        axios.post("http://127.0.0.1:8000/login/", credentials, axiosConfig)
        .then((res) => {
            console.log(res.data)
            history.push('/')
            localStorage.setItem('isAuthenticated' , true)
            handleAuth(true)
        })
        .catch((err) => console.log(err))
        .finally(alert('ss'))
    }
    return ( 
        <form onSubmit= {handlerLogin}>
            <h3>Sign In</h3>
            <div className="form-group input-spacing">
                <label htmlFor="">Email Address</label>
                <input type="email" placeholder="Enter email" className="form-control" onChange={e =>  setCredentials((prevState) => ({...prevState, email: e.target.value }))}/>
            </div>

            <div className="form-group input-spacing">
                <label htmlFor="">Password</label>
                <input type="password" placeholder="Enter password" className="form-control" onChange={e =>  setCredentials((prevState) => ({...prevState, password: e.target.value }))} />
            </div>

            <div className="form-group input-spacing">
                <div className="custom-control custom-checkbox">
                    <input type="checkbox" className="custom-control-input" id="customCheck1" />
                    <label className="custom-control-label" htmlFor="customCheck1" >Remember me</label>
                </div>
            </div>

            <button type="submit" className="btn btn-primary btn-block input-spacing">Submit</button>
            <p className="forgot-password text-right">
                Forgot <a href="a">password?</a>
            </p>

        </form>
        // <div>
        //     <h3>React Login Component</h3>
        // </div>
    );
}
 
export default Login;