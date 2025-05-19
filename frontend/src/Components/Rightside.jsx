import { Box } from "@mui/material";
import React from "react";
import ClearHistory from "./ClearHistory";
import Feedback from "./Feedback";

function Rightside({ ratingValue, setRatingValue, comment, setComment }) {
  return (
    <Box style={{ width: "100%", background: "#e5e4ec" }}>
      <ClearHistory />
      <Feedback
        ratingValue={ratingValue}
        setRatingValue={setRatingValue}
        comment={comment}
        setComment={setComment}
      />
    </Box>
  );
}

export default Rightside;
