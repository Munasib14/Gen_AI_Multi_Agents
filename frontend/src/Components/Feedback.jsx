import React from "react";
import { Box, Divider, Rating, TextField, Typography } from "@mui/material";
import Card from "./Card";
import ButtonComp from "./Button";

function Feedback({ ratingValue, setRatingValue, comment, setComment }) {
  const handleChange = (event, newValue) => {
    setRatingValue(newValue);
  };

  return (
    <Card
      height={"76vh"}
      children={
        <Box style={{ padding: 20 }}>
          <Typography variant="h5" style={{ color: "#2e5e95" }}>
            Feedback
          </Typography>
          <Divider style={{ marginTop: 20, marginBottom: 20 }} />
          <Box style={{ display: "flex" }}>
            <Typography
              variant="subtitle1"
              style={{ color: "black", fontWeight: 500, marginRight: 30 }}
            >
              Rating
            </Typography>
            <Rating
              name="simple-controlled"
              value={ratingValue}
              onChange={handleChange}
            />
          </Box>
          <Typography
            variant="subtitle1"
            style={{
              color: "black",
              fontWeight: 500,
              marginRight: 30,
              marginTop: 10,
            }}
          >
            Comment
          </Typography>
          <TextField
            multiline
            rows={7}
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            style={{ marginBottom: "7vh", marginTop: 20, width: 325 }}
          />

          <Box style={{ justifyContent: "center", display: "flex" }}>
            <ButtonComp
              text="Submit"
              onClick={() => console.log("submit feedback")}
            />
          </Box>
        </Box>
      }
    />
  );
}

export default Feedback;
