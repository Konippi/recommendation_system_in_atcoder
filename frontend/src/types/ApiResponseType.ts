import {SubmissionsInfoType} from "./SubmissionsInfoType";
import {RecommendedProblemsType} from "./RecommendedProblemsType";

export type ApiResponseType = {
    api_response: {
        submissions_info: SubmissionsInfoType[];
        recommended_problems: RecommendedProblemsType[];
    };
};
