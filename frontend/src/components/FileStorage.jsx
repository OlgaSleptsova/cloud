import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import "./FileStorage.css";
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/";
const FileStorage = () => {
    const { userId } = useParams();
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [editingFileId, setEditingFileId] = useState(null);
    
    const [selectedFile, setSelectedFile] = useState(null);
    const [comment, setComment] = useState('');
    const [uploadStatus, setUploadStatus] = useState(null);
    const [loadingFiles, setLoadingFiles] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
      
    const [newComment, setNewComment] = useState('');
    const [linkCopied, setLinkCopied] = useState(false);

    axios.defaults.withCredentials = true;

    // const getCSRFToken = () => {
    //     const csrfCookie = document.cookie
    //         .split("; ")
    //         .find((row) => row.startsWith("csrftoken="));
    //     return csrfCookie ? csrfCookie.split("=")[1] : null;
    // };

    const authorizedRequest = async (config) => {
        try {
            // const csrfToken = getCSRFToken();
            const token = localStorage.getItem('auth_token')
            const headers = {
                ...config.headers,
                'Authorization': `Token ${token}`
            };

            const response = await axios({
                ...config,
                withCredentials: true,
                headers,
            });
            return response;
        } catch (error) {
            if (error.response?.status === 401) {
                console.log(
                    "Необходима аутентификация. Пожалуйста, войдите в систему."
                );
            } else if (error.response?.status === 403) {
                console.log("Доступ запрещён. Проверьте CSRF или права доступа.");
            }
            throw error;
        }
    };

    const fetchFiles = async () => {
        setLoading(true);
        try {
            const response = await authorizedRequest({
                method: "GET",
            
                url:`${API_URL}api_admin/persons/files/${userId}/`
            });
            setFiles(response.data.files || []);
        } catch (error) {
            console.error("Ошибка получения файлов:", error);
            setError("Ошибка при загрузке файлов.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFiles();
    }, [userId]);

    const handleViewFile = (fileUrl) => {
    const fullUrl = `${API_URL}${fileUrl}`;
    window.open(fullUrl, "_blank");
  };
    
    const handleRenameFile = async (fileId, oldFileName) => {
    const newFileName = prompt("Введите новое имя файла:", oldFileName);
    if (newFileName && newFileName !== oldFileName) {
      try {
        await authorizedRequest({
          method: "PUT",
          url: `${API_URL}api_files/files/rename/${fileId}/`,
          data: { name: newFileName },
        });
        console.log("Имя файла обновлено.");
        fetchFiles();
      } catch (error) {
        console.error("Ошибка обновления имени файла:", error);
        console.log("Не удалось обновить имя файла.");
      }
    }
  };

    const handleUpdateComment = async (fileId) => {
    if (!newComment) {
      console.log("Комментарий не может быть пустым.");
      return;
    }

    const updatedFiles = files.map((file) =>
      file.id === fileId ? { ...file, comment: newComment } : file
    );
    setFiles(updatedFiles);

    try {
      await authorizedRequest({
        method: "PATCH",
        url: `${API_URL}api_files/files/comment/${fileId}/`,
        data: { comment: newComment },
      });
      console.log("Комментарий обновлён.");
      setEditingFileId(null);
      setNewComment("");
    } catch (error) {
      console.error("Ошибка обновления комментария:", error);
      console.log("Не удалось обновить комментарий.");
    }
  };

    const handleDownloadFile  = async (fileId,fileName) => {
    try {
      const response = await fetch(`${API_URL}api_files/download_file/${fileId}/`); // Замените на URL сервера

      if (!response.ok) throw new Error('Ошибка при скачивании файла');

      // Получаем бинарные данные (Blob)
      const blob = await response.blob();
      
      // Создаем временную ссылку
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
       link.download = fileName;
        link.click();}
        catch (error) {
   console.error('Ошибка:', error);
  }}

 

  
  
  

  const handleGenerateLink = async (fileId) => {
    try {
      const response = await authorizedRequest({
        method: "GET",
        url: `${API_URL}api_files/file_link/${fileId}/`,
      });
      console.log("Server Response:", response.data);
      console.log("Generated file link:", response.data.link);

      if (response.data.link) {
        const fullUrl = `${API_URL}api_files/pablic/${response.data.link}`;
       

        if (navigator.clipboard) {
          navigator.clipboard.writeText(fullUrl)
            .then(() => {
              console.log("Ссылка скопирована в буфер обмена!");
              setLinkCopied(true);
              setTimeout(() => setLinkCopied(false), 3000);
            })
            .catch((error) => {
              console.error("Ошибка при копировании ссылки:", error);
            });
        } else {
          const textArea = document.createElement("textarea");
          textArea.value = fullUrl;
          document.body.appendChild(textArea);
          textArea.select();
          document.execCommand("copy");
          document.body.removeChild(textArea);
          console.log("Ссылка скопирована в буфер обмена!");
          setLinkCopied(true);
          setTimeout(() => setLinkCopied(false), 3000);
        }
      } else {
        console.log("Ошибка: Не удалось получить ссылку.");
      }
    } catch (error) {
      console.error("Ошибка генерации ссылки:", error);
      console.log("Не удалось получить ссылку.");
    }
  };


    const handleDelete = async (fileId) => {
        if (window.confirm("Вы уверены, что хотите удалить этот файл?")) {
            try {
                //const csrfToken = getCSRFToken();
                const token = localStorage.getItem('auth_token')
                console.log(token);

                await axios.delete(`${API_URL}api_files/files/delete/${fileId}/`, {
                    headers: {
                         'Authorization': `Token ${token}`
                    },
                    withCredentials: true,
                });
                console.log("Файл успешно удалён.");
                fetchFiles();
            } catch (error) {
                if (error.response?.status === 403) {
                    console.error("Доступ запрещён. Проверьте CSRF или права доступа.");
                    alert("У вас нет прав на удаление этого файла.");
                } else {
                    console.error("Ошибка удаления файла:", error);
                }
            }
        }
    };

    return (
        <div className="file-storage-container">
            <h2>Управление файлами пользователя {userId}</h2>
            {error && <p className="error-message">{error}</p>}
            {loading ? (
                <p>Загрузка...</p>
            ) : files.length === 0 ? (
                <p>Нет загруженных файлов.</p>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>Название файла</th>
                            <th>Комментарий</th>
                            <th>Размер</th>
                            <th>Дата загрузки</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody>
                        {files.map((file) => (
                            <tr key={file.id}>
                                <td>{file.name}</td>
                                <td> {editingFileId === file.id ? (
                    <div>
                      <input
                        type="text"
                        value={newComment}
                        onChange={(e) => setNewComment(e.target.value)}
                      />
                      <button onClick={() => handleUpdateComment(file.id)}>Сохранить комментарий</button>
                    </div>
                  ) : (
                    file.comment
                  )}</td>
                                <td>{file.size} KB</td>
                                <td>{new Date(file.uploaded_at).toLocaleDateString()}</td>
                                <td>
                                    <button onClick={() => handleDelete(file.id)}>
                                        Удалить
                                    </button>
                                    <button onClick={() => handleViewFile(file.file)}>Просмотр</button>
                                    <button onClick={() => handleRenameFile(file.id, file.name)}>Переименовать файл</button>
                                    <button onClick={() => setEditingFileId(file.id)}>Редактировать комментарий</button>
                                    <button onClick={() => handleDownloadFile(file.id,file.name)}>Скачать</button>
                                    <button onClick={() => handleGenerateLink(file.id)}>Скачать ссылку</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default FileStorage;