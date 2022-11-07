import {SubmissionInfoType} from "./SubmissionInfoType";
import {RecommendedProblemsType} from "./RecommendedProblemsType";

export type ApiResponseType = {
    api_response: {
        submission_info: SubmissionInfoType[];
        recommended_problems: RecommendedProblemsType[];
    };
};
