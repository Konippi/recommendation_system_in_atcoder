import React, {FC} from "react";
import {AccountCircle} from "@mui/icons-material";

type Props = {
  userName: string;
};

const Header: FC<Props> = (props: Props) => {
    const {userName} = props;

    return (
        <header>
            <div className={"header-box"}>
                <AccountCircle className={"person-icon"} />
                <span>{userName}</span>
            </div>
        </header>
    )
}

export default Header;
