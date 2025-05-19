
import React, { useEffect, useState, useRef } from "react";
import { Box, FormControl, MenuItem, Select, Typography } from "@mui/material";
import ButtonComp from "./Button";
import DropdownWithSearch from "./DropdownWithSearch";

 
const agentIdToNameMap = {
  101: "DB Agent",
  102: "Web Agent",
  103: "Test Agent",
  104: "DevOps Agent",
  201: "DB Agent",
  202: "Web Agent",
  203: "Test Agent",
  204: "DevOps Agent",
};

// Dynamic map of user story options based on appId and agent
const promptMap = {
  "1": {
    "Web Agent": ["Convert ASP.NET 4.8 Version to ASP.NET 8","Convert ASP.NET Version 8 to React","Authenticate & Automate"," CSS Optimization "],
    "DB Agent": ["Migrate Legacy SQL to Azure SQL","Optimize SQL Queries"],
    "Test Agent": ["Write React Unit Tests", "Advance Tests"],
    "DevOps Agent": ["Jenkins pipeline into GitHub Actions workflow","Terraform configuration into GitHub Actions workflow","Devops Infra", "Transform Infra"],

  },
  "2": {
    "Web Agent": ["Convert Mulesoft to Springboot","Html to React"],
    "DB Agent": ["Refactor and Transform SQL", "optimize_performance"],
    "Test Agent": ["API Regression Tests", "UI Test Automation"],
    "DevOps Agent": ["Infrastructure as Code", "CI/CD Pipelines"],
  },
};

function PromptBox({
  promptOptions,
  setPromptOptions,
  selectedPromptOption,
  setSelectedPromptOption,
  selUserStory,
  setSelUserStory,
  selApplicationName,
  selDropdownVal,
}) {
  const fileInputRef = useRef();
  const [fileName, setFileName] = useState("");
  const [userStoryList, setUserStoryList] = useState([]);

  useEffect(() => {
    if (selApplicationName && selDropdownVal) {
      const agentName = agentIdToNameMap[selDropdownVal];
      const applicationPrompts = promptMap[selApplicationName];
      const prompts = applicationPrompts ? applicationPrompts[agentName] || [] : [];
      const formattedList = prompts.map((title, idx) => ({
        id: title,
        title,
      }));
      setUserStoryList(formattedList);
    } else {
      setUserStoryList([]);
    }
  }, [selDropdownVal, selApplicationName]);

  return (
    <Box style={{ width: "100%", background: "white", height: "76vh", margin: 5, borderRadius: 10, padding: 10 }}>
      <Typography>Select User Story</Typography>
      <FormControl fullWidth size="small" style={{ background: "white", borderRadius: 10, maxWidth: 350 }}>
        <Select
          value={selUserStory}
          onChange={(e) => setSelUserStory(e.target.value)}
          displayEmpty
          inputProps={{ "aria-label": "Select User Story" }}
        >
          <MenuItem value="">Select Option</MenuItem>
          {userStoryList.map((item) => (
            <MenuItem key={item.id} value={item.title}>{item.title}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <Typography style={{ marginTop: 20 }}>Select Common Prompt</Typography>
      <DropdownWithSearch
        promptOptions={promptOptions}
        setPromptOptions={setPromptOptions}
        selectedPromptOption={selectedPromptOption}
        setSelectedPromptOption={setSelectedPromptOption}
      />

      <Typography style={{ marginTop: 20 }}>Select File:</Typography>
      <ButtonComp onClick={() => fileInputRef.current.click()} text="Upload File" />
      <input
        onChange={(event) => {
          setFileName(event.target.files);
        }}
        multiple={false}
        ref={fileInputRef}
        type="file"
        hidden
      />
      {fileName && <Typography>{fileName[0]?.name}</Typography>}
    </Box>
  );
}

export default PromptBox;