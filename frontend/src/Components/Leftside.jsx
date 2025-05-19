import React from "react";
import { Box, Typography } from "@mui/material";
import Controls from "./Controls";
import Chat from "./Chat";
import styles from "./Chat.module.css";

const Leftside = ({
  // Chat message bubbles for <Chat />
  message,             // message = [{ role, content }]
  onSend,              // function to update `message` in parent
  content,
  setContent,

  // Agent & prompt selection
  selectedPrompt,
  selectedAgent,

  // Full chatHistory for QA-style listing
  chatHistory = [],    // [{ user, agent }, ...]
  setChatHistory,      // to update history in parent

  // Optional: for loading control
  isDisabled = false,

  // Optional: to update editable code/prompt areas
  setEditablePrompt,
  setSqlCode,
}) => {
  return (
    <Box className={styles.LeftsideWrapper}>
      <span
        style={{
          width: "100%",
          background: "#a9d5e8",
          paddingLeft: 15,
          paddingRight: 15,
          margin: 20,
          borderRadius: 5,

        }}
      >
        Hi! Welcome to UHC Product Knowledge Chatbot
      </span>
      {/* Message bubbles like Chat UI */}
      <Box
        style={{
          width: "960px",
          flexGrow: 1,
          background: "white",
          margin: 10,
          borderRadius: 10,
          height: "400px",
          paddingTop: 10,
          overflowY: "auto",
          boxSizing: "border-box",
        }}
      >


        <Chat
          message={message}
          onSend={onSend}
          content={content}
          setContent={setContent}
        />
      </Box>

      {/* Full QA-style chat history (optional) */}
      <Box className={styles.ChatHistory}>
        {[...chatHistory].reverse().map((item, idx) => (
          <Box key={idx} className={styles.ChatBlock}>
            <Typography variant="subtitle2" className={styles.UserLabel}>
              User&nbsp;{chatHistory.length - idx}:
            </Typography>
            <pre className={styles.UserMsg}>{item.user}</pre>

            <Typography variant="subtitle2" className={styles.AgentLabel}>
              Agent Output:
            </Typography>
            <pre className={styles.AgentMsg}>{item.agent}</pre>
          </Box>
        ))}
      </Box>

      {/* Prompt input + Execute button */}
      <Controls
        isDisabled={isDisabled}
        content={content}
        setContent={setContent}
        onSend={onSend}
        selectedPrompt={selectedPrompt}
        selectedAgent={selectedAgent}
        setEditablePrompt={setEditablePrompt}
        setSqlCode={setSqlCode}
        setChatHistory={setChatHistory}
      />
    </Box>
  );
};

export default Leftside;
