import React from "react";
import ReactDOM from 'react-dom'
import {Home} from "./components/pages";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Layout} from "./components/layouts";

ReactDOM.render(
    <BrowserRouter>
        <Routes>
            <Route path="/" element={
                <Layout>
                    <Home />
                </Layout>}
            />
        </Routes>
    </BrowserRouter>,
    document.getElementById("root")
);
