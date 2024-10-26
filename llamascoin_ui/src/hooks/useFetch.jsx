import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

export const useFetch = (url, method = "GET", body = null) => {
  const { authData } = useAuth(); 
  const [status, setStatus] = useState("loading"); 
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setStatus("loading");
      try {
        const options = {
          method,
          url,
          headers: {
            Authorization: `Bearer ${authData.accessToken}`,
            "Content-Type": "application/json", 
          },
          data: body, // Para POST, PUT, DELETE, etc.
        };

        const response = await axios(options);
        setData(response.data);
        setStatus("success");
      } catch (error) {
   
        setStatus("error"); 
      }
    };

    fetchData();
  }, [url, method, body]); 

  return { status, data }; 
};
