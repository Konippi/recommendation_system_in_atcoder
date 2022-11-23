import React, {FC, useMemo} from "react";
import {SubmissionsInfoType} from "../../types/SubmissionsInfoType";
import MaterialReactTable from "material-react-table";
import {Box} from "@mui/material";

type Props = {
    submissionsInfo: SubmissionsInfoType[];
};

type ConvertedSubmissionInfoType = {
    submissionDate: string;
    contest: string;
    problem: string;
    result: string;
};

const SubmissionsTable: FC<Props> = ({submissionsInfo}: Props) => {
    const columns = useMemo(() =>
        [
            {
                header: "Submission Date",
                accessorKey: "submissionDate",
                muiTableHeadCellProps: {sx: {color: "#FF3333"}},
                size: 150
            },
            {
                header: "Contest",
                accessorKey: "contest",
                muiTableHeadCellProps: {sx: {color: "#4B7BEC"}},
                size: 100
            },
            {
                header: "Problem",
                accessorKey: "problem",
                muiTableHeadCellProps: {sx: {color: "#45AAF2"}},
                size: 250
            },
            {
                header: "Result",
                accessorKey: "result",
                muiTableHeadCellProps: {sx: {color: "#20BF6B"}},
                size: 100,
                Cell: ({ cell }: {cell: any}) => (
                    <Box sx={() => ({
                        backgroundColor: cell.getValue() == "AC" ? "#5CB85C" : "#F0AD4E",
                        borderRadius: "8px",
                        color: "white",
                        font: "Arial",
                        maxHeight: "1rem",
                        maxWidth: "1.6rem",
                        p: "0.6rem",
                        textAlign: "center"
                    })}>
                        {cell.getValue()}
                    </Box>
                )
            }
        ],[]);

    const convertedSubmissionInfo: Partial<ConvertedSubmissionInfoType>[] = [];

    // convert api response type into table type
    submissionsInfo.map(submissions => {
        const contest = submissions.contest;
        submissions.submissions.map(submission => {
            const submissionDate: string = submission.date;
            const problem: string = submission.problem;
            const result: string = submission.result;
            convertedSubmissionInfo.push({submissionDate, contest, problem, result});
        })
    });

    // sort by submissionDate
    convertedSubmissionInfo.sort((i, j) => {
        if(i.submissionDate! < j.submissionDate!) return 1;
        if(i.submissionDate! > j.submissionDate!) return -1;
        return 0;
    })

    return (
        <MaterialReactTable
            columns={columns}
            data={convertedSubmissionInfo}
            enableFullScreenToggle={false}
            enableDensityToggle={false}
            muiTableContainerProps={{
                sx: {maxHeight: '280px' }
            }}
        />
    );
};

export default SubmissionsTable;