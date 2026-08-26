import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./Admin.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/";

const Admin = () => {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    first_name: "",
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [confirmDelete, setConfirmDelete] = useState({ isVisible: false, userId: null });

  const showNotification = (message, type = "success") => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  // const getCSRFToken = () => {
  //   const name = "csrftoken";
  //   return document.cookie
  //     .split("; ")
  //     .find((row) => row.startsWith(`${name}=`))
  //     ?.split("=")[1];
  // };

  const authorizedRequest = async (config) => {
    try {
      // const csrfToken = getCSRFToken();
      const token = localStorage.getItem('auth_token')
      const response = await axios({
        ...config,
        headers: {
          ...config.headers,
          'Authorization': `Token ${token}`
        },
        withCredentials: true,
      });
      return response;
    } catch (error) {
      console.error("Ошибка запроса:", error);
      throw error;
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const { username, password, email, first_name } = formData;

    if (!username || !password || !email || !first_name) {
      setError("Все поля обязательны для заполнения!");
      return;
    }

    setLoading(true);
    try {
      await authorizedRequest({
        method: "POST",
        url: `${API_URL}api_admin/persons/`,
        data: formData,
      });
      showNotification("Пользователь успешно зарегистрирован!");
      setFormData({ username: "", password: "", email: "", first_name: "" });
      fetchUsers();
    } catch (err) {
      setError("Ошибка при регистрации пользователя");
      console.error("Ошибка регистрации:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await authorizedRequest({
        method: "GET",
        url: `${API_URL}api_admin/persons/`,
      });
      setUsers(response.data || []);
    } catch (error) {
      console.error("Ошибка получения пользователей:", error);
      setError("Ошибка при загрузке пользователей");
    } finally {
      setLoading(false);
    }
  };

  
   const handleDeleteUser = async (userId) => {
    if (window.confirm("Вы уверены, что хотите удалить этого пользователя?")) {
      try {
        await authorizedRequest({
          method: "DELETE",
          url: `${API_URL}api_admin/persons/${userId}/`,
        });
        console.log("Пользователь успешно удалён.");
        fetchUsers()
        
      } catch (error) {
        console.error("Ошибка удаления пользователя:", error);
        console.log("Не удалось удалить пользователя.");
      }
    }
  };
    const toggleStaffStatus = async (userId, isStaff) => {
    try {
      await authorizedRequest({
        method: "PATCH",
        url: `${API_URL}api_admin/users/${userId}/update-status/`,
        data: { is_staff: !isStaff },
      });
      setUsers(
        users.map((user) =>
          user.id === userId ? { ...user, is_staff: !isStaff } : user
        )
      );
      showNotification("Статус сотрудника обновлён.");
    } catch (error) {
      console.error("Ошибка изменения статуса сотрудника:", error);
      showNotification("Ошибка при обновлении статуса.", "error");
    }
  };
  

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="admin-container">
      <h2>Управление пользователями</h2>
      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}

      <h3>Регистрация нового пользователя</h3>
      <form onSubmit={handleRegister}>
        <div>
          <label>Имя пользователя:</label>
          <input
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
          />
        </div>
        <div>
          <label>Полное имя:</label>
          <input
            type="text"
            value={formData.first_name}
            onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
          />
        </div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          />
        </div>
        <div>
          <label>Пароль:</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Регистрация..." : "Зарегистрировать"}
        </button>
      </form>

      <h3>Список пользователей</h3>
      {error && <p className="error-message">{error}</p>}
      {loading ? (
        <p>Загрузка...</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Имя пользователя</th>
              <th>Полное имя</th>
              <th>Email</th>
              <th>Администратор</th>
              <th>Файлы</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id}>
                <td>{user.username}</td>
                <td>{user.first_name || '-'}</td>
                <td>{user.email}</td>
                <td>
                  <button
                    onClick={() => toggleStaffStatus(user.id, user.is_staff)}
                  >
                    {user.is_staff ? "Снять" : "Назначить"}
                  </button>
                </td>
              
                <td>
                  <span>{user.file_count} файл(а)</span>, <span>{user.total_size} КB</span>
                  <br />
                  <button onClick={() => navigate(`/files/${user.username}`)}>
                    Управление файлами
                  </button>
                </td>
                <td>
                  <button onClick={() => handleDeleteUser(user.id)}>
                    Удалить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

    
    </div>
  );
};

export default Admin;
