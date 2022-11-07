import React from "react";
import ReactDOM from 'react-dom'
import {Home} from "./components/pages";
import {BrowserRouter, Route, Routes} from "react-router-dom";

ReactDOM.render(
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<Home />} />
        </Routes>
    </BrowserRouter>,
    document.getElementById("root")
);
