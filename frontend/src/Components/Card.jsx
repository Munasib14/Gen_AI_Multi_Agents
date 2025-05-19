import { Box } from "@mui/material";
import React from "react";

function Card({ height, children }) {
  return (
    <Box
      style={{
        background: "white",
        margin: 5,
        borderRadius: 10,
        height: height,
        alignContent: "center",
      }}
    >
      {children}
    </Box>
  );
}

export default Card;
