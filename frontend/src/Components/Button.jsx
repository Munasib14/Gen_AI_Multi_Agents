import { Button } from "@mui/material";
import React from "react";

function ButtonComp({ text, onClick, margin = 0 }) {
  return (
    <Button
      variant="contained"
      onClick={onClick}
      color="primary"
      style={{ borderRadius: 15, margin: margin }}
    >
      {text}
    </Button>
  );
}

export default ButtonComp;
