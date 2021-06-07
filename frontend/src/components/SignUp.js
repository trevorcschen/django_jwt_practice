import {useEffect, useState} from 'react';
import axios from 'axios'

const SignUp = () => {
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.withCredentials = true;
    let axiosConfig = {
        headers: {
            'Content-Type': 'application/json;charset=UTF-8',
        }
      };
    useEffect(() => 
    {
        axios.get("http://127.0.0.1:8000/api/v1/articles", axiosConfig)
        .then((response) => console.log(response.data))
        .catch((err) => console.log(err))
        // console.log("login here")
    }, [])
    return ( 
        <form>
                <h3>Sign Up</h3>

                <div className="form-group input-spacing">
                    <label>First name</label>
                    <input type="text" className="form-control" placeholder="First name" />
                </div>

                <div className="form-group input-spacing">
                    <label>Last name</label>
                    <input type="text" className="form-control" placeholder="Last name" />
                </div>

                <div className="form-group input-spacing">
                    <label>Email address</label>
                    <input type="email" className="form-control" placeholder="Enter email" />
                </div>

                <div className="form-group input-spacing">
                    <label>Password</label>
                    <input type="password" className="form-control" placeholder="Enter password" />
                </div>

                <button type="submit" className="btn btn-primary btn-block input-spacing">Sign Up</button>
                <p className="forgot-password text-right">
                    Already registered <a href="#">sign in?</a>
                </p>
            </form>
     );
}
 
export default SignUp;