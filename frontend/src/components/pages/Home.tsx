import React, {FC, ReactElement} from "react";
import {RecommendedProblemList, SubmissionsTable} from "../mui";
import {useApiData} from "../../hooks";
import {ApiResponseType} from "../../types/ApiResponseType";

type Props = {
    userName: string;
};

const Home: FC<Props> = ({userName}: Props) => {
    const data: ApiResponseType | undefined = useApiData(userName);

    return (
        <>
            {data &&
                <>
                    <div className={"list"}>
                        <h2>Recommended Problems</h2>
                        <RecommendedProblemList recommendedProblems={data.api_response.recommended_problems} />
                    </div>
                    <hr />
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