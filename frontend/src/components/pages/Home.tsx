import React, {FC} from "react";
import {RecommendedProblemList, SubmissionsTable} from "../mui";
import {useApiData} from "../../hooks";
import {ApiResponseType} from "../../types/ApiResponseType";
import {Box, CircularProgress} from "@mui/material";

type Props = {
    userName?: string;
};

const Home: FC<Props> = ({userName}: Props) => {
    const data: ApiResponseType | undefined = useApiData(userName!);

    return (
        <>
            {data ?
                <div>
                    <div className={"list"}>
                        <h2>Recommended Problems</h2>
                        <RecommendedProblemList recommendedProblems={data.api_response.recommended_problems} />
                    </div>
                    <hr />
                    <div className={"table"}>
                        <h2>Your Submissions</h2>
                        <SubmissionsTable submissionsInfo={data.api_response.submissions_info} />
                    </div>
                </div>:
                <Box sx={{display: "flex", justifyContent: "center", marginTop: "20%"}}>
                    <CircularProgress />
                </Box>
            }
        </>
    )
};

export default Home;