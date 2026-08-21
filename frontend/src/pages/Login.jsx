import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { useDispatch } from "react-redux";
import { setAuthState } from "../store/authSlice";
import "./Login.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/";

axios.defaults.withCredentials = true;


const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  

  const getCSRFToken = () => {
    const name = "csrftoken";
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith(`${name}=`))
      ?.split("=")[1];

    if (!csrfToken) {
      console.error("CSRF токен не найден в куках!");
    }

    return csrfToken;
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
    const response = await fetch(`${API_URL}api/api-token-auth/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('auth_token', data.token); // Сохраняем токен
      console.log('Успешный вход!', data.token);
      const response_user = await fetch(`${API_URL}api_admin/user/me/${data.token}/`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json',
        
                'Authorization': `Token ${data.token}`,     
      },
       
    });
   
    const data2 = await response_user.json();
  console.log(data2.username)
    dispatch(
        setAuthState({
          isAuthenticated: true,
          user: {
            username:data2.username,
            role:data2.role,
          },
        })
      );

    
    



     if (data2.role === "admin") {
       console.log("Перенаправление на Admin");
       navigate("/Admin");


      } else {
      console.log("Перенаправление на UserPage");
      navigate("/UserPage");
      }
  


      
    } else {
      console.error('Ошибка авторизации');
    }

    // try {
    //   const csrfToken = getCSRFToken();
    //   console.log(csrfToken)
      

    //   const response = await axios.post(
    //     `${API_URL}/api/auth/login/`,
    //     { username, password },
    //     {
    //       headers: {
    //         "X-CSRFToken": csrfToken,
    //       },
    //       withCredentials: true,
    //     }
    //   );

    //   console.log("Успешный вход:", response.data);
    //   console.log("Успешный вход:", response.data.username);
     

      // dispatch(
      //   setAuthState({
      //     isAuthenticated: true,
      //     user: {
      //       username:data2.username,
      //       role:data2.role,
      //     },
      //   })
      // );

      // if (response.data.role === "admin") {
      //   console.log("Перенаправление на Admin");
      //   navigate("/Admin");
      // } else {
      //   console.log("Перенаправление на UserPage");
      //   navigate("/UserPage");
      // }
    } catch (error) {
      console.error("Ошибка входа:", error);
      setError(
        error.response?.data?.error || "Ошибка входа, проверьте логин и пароль."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <h2>Вход</h2>

      {/* Отображение сообщений об успехе или ошибке */}
      {error && <div className="message error">{error}</div>}

      <form onSubmit={handleSubmit} className="login-form">
        <div className="input-container">
          <input
            type="text"
            placeholder="Логин"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className={`input-field ${error ? "input-error" : ""}`}
            required
          />
        </div>
        <div className="input-container">
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={`input-field ${error ? "input-error" : ""}`}
            required
          />
        </div>
        <button type="submit" className="submit-button" disabled={loading}>
          {loading ? "Загрузка..." : "Войти"}
        </button>
      </form>
    </div>
  );
};

export default Login;
