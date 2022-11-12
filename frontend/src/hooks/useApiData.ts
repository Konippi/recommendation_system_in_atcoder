import {useEffect, useState} from "react";
import axios from "axios";
import {ApiResponseType} from "../types/ApiResponseType";

const useApiData = (userName: string) => {
    const [data, setData] = useState<ApiResponseType>();

    useEffect(() => {
        const getInfo = async() => {
            return await axios.get(`http://localhost:8000/${userName}`);
        };
        getInfo()
            .then(res => {
                setData(res.data);
            })
            .catch(error => alert(error));
    }, []);

    return data;
};

export default useApiData;
