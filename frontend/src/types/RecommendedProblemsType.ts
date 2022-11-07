export type RecommendedProblemsType = {
    contest: string;
    problem: {
        diff: string;
        title: string;
    };
    user: {
        name: string;
        cos_similarity: number;
    };
};
