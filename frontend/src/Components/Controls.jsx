import { Box, TextareaAutosize } from "@mui/material";
import React, { useEffect, useRef } from "react";
import axios from "axios";
import styles from "./Chat.module.css";
import ButtonComp from "./Button";

const API_URL = "http://127.0.0.1:8000";

function Controls({
  isDisabled = false,
  content,
  setContent,
  onSend, // optional external handler
  selectedPrompt,
  selectedAgent,
  setEditablePrompt,
  setSqlCode,
  setChatHistory,
}) {
  const textareaRef = useRef(null);

  // Auto-focus on textarea
  useEffect(() => {
    if (!isDisabled && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [isDisabled]);

  // Fetch prompt content when selection changes
  useEffect(() => {
    const fetchPrompt = async () => {
      if (!selectedPrompt || !selectedAgent) return;

      try {
        const res = await axios.get(`${API_URL}/get-prompt`, {
          params: {
            prompt_name: selectedPrompt,
            agent_type: selectedAgent,
          },
        });

        const fetchedContent = res?.data?.prompt_content || "";
        setEditablePrompt?.(fetchedContent);
        setSqlCode?.(fetchedContent);
        setContent?.(fetchedContent);
      } catch (error) {
        console.error("Error fetching prompt:", error);
        const fallback = "-- ⚠️ Unable to fetch prompt.";
        setEditablePrompt?.(fallback);
        setSqlCode?.(fallback);
        setContent?.(fallback);
      }
    };

    fetchPrompt();
  }, [selectedPrompt, selectedAgent]);

  // Run the agent
  const handleRun = async () => {
    const inputCode = content?.trim();
    if (!inputCode) {
      alert("⚠️ Please enter code.");
      return;
    }

    let endpoint = "";
    let payload = {};

    switch (selectedAgent) {
      case "DB Agent":
        endpoint = `${API_URL}/run-db-agent/`;
        payload = {
          sql_code: inputCode,
          prompt_name: selectedPrompt || "transform_identity.j2",
        };
        break;
      case "Web Agent":
        endpoint = `${API_URL}/run-web-agent/`;
        payload = {
          html_code: inputCode,
          prompt_name: selectedPrompt || "convert_asp_net_to_react.j2",
        };
        break;
      case "Test Agent":
        endpoint = `${API_URL}/run-test-agent/`;
        payload = {
          source_code: inputCode,
          prompt_name: selectedPrompt || "Convert_ReactPage_to_Playwright.j2",
        };
        break;
      case "DevOps Agent":
        endpoint = `${API_URL}/run-devops-agent/`;
        payload = {
          infra_description: inputCode,
          prompt_name: selectedPrompt || "jenkins_pipeline.j2",
        };
        break;
      default:
        alert("⚠️ Unsupported agent selected.");
        return;
    }

    try {
      const res = await axios.post(endpoint, payload);

      let agentResponse;

      if (selectedAgent !== "DevOps Agent") {
        agentResponse = res?.data?.result?.output || "⚠️ No output returned.";
      } else {
        agentResponse = res?.data?.result?.Devops_output || "⚠️ No output returned.";
      }

      // Add to QA-style history
      setChatHistory?.((prev) => [...prev, { user: inputCode, agent: agentResponse }]);
      setContent?.(""); // Clear input

      // Send messages to Chat-style component
      onSend?.({ role: "user", content: inputCode });
      onSend?.({ role: "agent", content: agentResponse });
    } catch (error) {
      console.error("Error running agent:", error);
      const errorMsg = "⚠️ Failed to get response from agent.";

      setChatHistory?.((prev) => [
        ...prev,
        { user: inputCode, agent: errorMsg },
      ]);

      onSend?.({ role: "user", content: inputCode });
      onSend?.({ role: "agent", content: errorMsg });
    }
  };

  const handleContentChange = (event) => {
    setContent(event.target.value);
  };

  const handleContentSend = () => {
    if (content.length > 0) {
      handleRun();
    }
  };

  const handleEnterPress = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleContentSend();
    }
  };

  return (
    <Box className={styles.Controls}>
      <Box className={styles.TextAreaContainer}>
        <TextareaAutosize
          ref={textareaRef}
          className={styles.TextArea}
          disabled={isDisabled}
          placeholder="Message AI Chatbot"
          value={content}
          minRows={1}
          maxRows={4}
          onChange={handleContentChange}
          onKeyDown={handleEnterPress}
        />
      </Box>
      <ButtonComp
        className={styles.Button}
        disabled={isDisabled}
        onClick={handleContentSend}
        text="Enter"
      />
    </Box>
  );
}

export default Controls;
