// Chat.jsx

import React from "react";
import { Box, Typography } from "@mui/material";

const Chat = ({ message = [], content, setContent }) => {
  return (
    <Box
      sx={{
        padding: 2,
        display: "flex",
        flexDirection: "column",
        gap: 2,
        overflowY: "auto",
        height: "100%",
      }}
    >
      {message.map((msg, idx) => (
        <Box
          key={idx}
          sx={{
            alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
            backgroundColor: msg.role === "user" ? "#DCF8C6" : "#E6E6E6",
            borderRadius: 2,
            padding: 1.5,
            maxWidth: "70%",
            whiteSpace: "pre-wrap",
          }}
        >
          <Typography variant="subtitle2" color="textSecondary">
            {msg.role === "user" ? "User" : "Agent"}
          </Typography>
          <Typography variant="body1">{msg.content}</Typography>
        </Box>
      ))}
    </Box>
  );
};

export default Chat;
