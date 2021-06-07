import axios from 'axios'

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;
let axiosConfig = {
    headers: {
        'Content-Type': 'application/json;charset=UTF-8',
    }
  };
const validateAuth = ({setAuth}) =>
{
    axios.post("http://127.0.0.1:8000/validate/user/", axiosConfig)
    .then((res) => {
        console.log(res.data)
        localStorage.setItem('isAuthenticated', true)
        setAuth(true)

    })
    .catch((err) => {
        console.log(err)
        localStorage.removeItem('isAuthenticated')
        setAuth(false)
    })
}

const logout = ({setAuth}) =>
{
    let temp = true
    axios.post("http://127.0.0.1:8000/logout/", axiosConfig)
    .then((res) => 
    {
        console.log('logout')
        console.log(res.data)
        localStorage.removeItem('isAuthenticated')
        setAuth(false)
        temp = false
    })
    .catch((err) => console.log (err))
    return temp
}

const authServices  = 
{
    validateAuth,
    logout
}

export default authServices