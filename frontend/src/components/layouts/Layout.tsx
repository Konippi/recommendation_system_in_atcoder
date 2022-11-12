import Header from "../common/Header";
import React, {cloneElement, FC, memo, ReactElement} from "react";

type Props = {
    children: ReactElement;
};

const Layout : FC<Props>= memo(({children}: Props) => {
    const response: string | null = window.prompt("Your Name in AtCoder?");
    const userName: string = response === null ? "" : response;
    const additionalProps = {userName: userName};
    const newChildren = cloneElement(children, additionalProps);

    return (
        <div>
            <Header userName={userName}/>
            <main>
                <div>
                    {newChildren}
                </div>
            </main>
        </div>
    )
});

export default Layout;
