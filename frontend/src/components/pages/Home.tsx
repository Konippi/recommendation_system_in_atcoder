import React, {FC} from "react";
import {RecommendedProblemList, SubmissionsTable} from "../mui";
import {useApiData} from "../../hooks";
import {ApiResponseType} from "../../types/ApiResponseType";

const Home: FC = () => {
    const data: ApiResponseType | undefined = useApiData();

    return (
        <>
            {data &&
                <>
                    <div className={"list"}>
                        <h2>Recommended Problems</h2>
                        <RecommendedProblemList recommendedProblems={data.api_response.recommended_problems} />
                    </div>
                    <div className={"table"}>
                        <h2>Your Submissions</h2>
                        <SubmissionsTable submissionInfo={data.api_response.submission_info} />
                    </div>
                </>
            }
        </>
    )
};

export default Home;