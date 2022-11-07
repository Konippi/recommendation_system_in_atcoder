import {useEffect, useState} from "react";
import axios, {AxiosResponse} from "axios";
import {ApiResponseType} from "../types/ApiResponseType";

const useApiData = () => {
    const [data, setData] = useState<ApiResponseType>();

    useEffect(() => {
        const getInfo = async() => {
            return await axios.get("http://localhost:8000/kkonishi");
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
