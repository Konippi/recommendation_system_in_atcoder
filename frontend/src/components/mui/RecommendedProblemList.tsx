import React, {FC} from "react";
import {RecommendedProblemsType} from "../../types/RecommendedProblemsType";
import {Avatar, List, ListItem, ListItemAvatar, ListItemText} from "@mui/material";
import {AssignmentOutlined} from "@mui/icons-material";

type Props = {
    recommendedProblems: RecommendedProblemsType[];
};

const navigateToAtcoder = function(contest: string, diff: string) {
    if(diff === "Ex") diff = "H";
    const convertedDiff: string = diff.toLowerCase();
    window.open("https://atcoder.jp/contests/abc" + contest +
        "/tasks/abc" + contest + "_" + convertedDiff);
};

const RecommendedProblemList: FC<Props> = ({recommendedProblems}: Props) => {
    return (
        <List>
            {recommendedProblems.map(recommendedProblem => (
                <ListItem onClick={() => navigateToAtcoder(recommendedProblem.contest, recommendedProblem.problem.diff)}>
                    <ListItemAvatar>
                        <Avatar>
                            <AssignmentOutlined />
                        </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                        primary={`${recommendedProblem.problem.diff} - ${recommendedProblem.problem.title} ` +
                            `(AtCoder Beginner Contest ${recommendedProblem.contest})`}
                        secondary={`recommended point: ${recommendedProblem.user.cos_similarity.toFixed(3)}`}
                    />
                </ListItem>
            ))}
        </List>
    );
};

export default RecommendedProblemList;
