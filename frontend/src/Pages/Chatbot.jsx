import React, { useState, useEffect } from "react";
import { Box, Container, Button } from "@mui/material";
import axios from "axios";
import Navbar from "../Components/Navbar";
import Leftside from "../Components/Leftside";
import Rightside from "../Components/Rightside";
import PromptBox from "../Components/PromptBox";

const API_URL = "http://127.0.0.1:8000";
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

const promptOptionsMap = {
  "1": {
    "Web Agent": {
       "Convert Version ASP.NET 4.8 Version to ASP.NET 8": [
        { value: "convert_asp.net_4.8_to_8.j2", label: "ASP.NET 4.8 Version to ASP.NET 8" }],
       
      "Convert ASP.NET Version 8 to React": [
        { value: "convert_asp.net_to_jwt.j2", label: "Convert Asp.net to Jwt" },
        { value: "convert_asp.net_to_react.j2", label: "Convert Asp.net to React Components" },
      ],

      "Authenticate & Automate": [
        { value: "Authentication_Integration.j2", label: "Authentication Integration" },
        { value: "Automate_Form_Handling.j2", label: "Automate Form Handling" },
        { value: "State_Management.j2", label: "State Management" },
        {value:"Routing_Setup.j2",label: "RoutingSetup"}
      ],

      " CSS Optimization ": [
        { value: "Optimize_Css.j2", label: "Optimize CSS" }],
    },
    "DB Agent": {
      "Migrate Legacy SQL to Azure SQL": [
        { value: "migrate_legacy_azure.j2", label: "Migrate Legacy SQL to Azure SQL" },
        { value: "optimize_performance.j2", label: "Optimize Performance" },
      ],
      "Optimize SQL Queries": [
        { value: "add_try_catch.j2", label: "Add Try Catch" },
        { value: "analyze_security_risks.j2", label: "Analyze Security Risks " },
        { value: "best_practices.j2", label: "Best Practices" },
       
      
      ],
    },

    "Test Agent": {
      "Write React Unit Tests": [
        { value: "Convert_ReactPage_to_Playwright.j2", label: "Convert React Page to Playwright" },
        { value: "generate_multistep_feature_file.j2", label: "Generate Multistep Feature File Test" },
      ],
      "Advance Tests": [
        { value: "generate_advanced_integration_test.j2", label: "Generate Advanced Integration Test" },
        { value: "generate_advanced_unit_test.j2", label: "Generate Advanced Unit" },
      ],

    },

    "DevOps Agent": {
      "Jenkins pipeline into GitHub Actions workflow": [
        { value: "jenkins_pipeline.j2", label: "Jenkine Pipeline" },
        
      ],
      "Terraform configuration into GitHub Actions workflow": [
        { value: "terraform_module.j2", label: "Terraform configuration" },
        
      ],
      "Devops Infra": [
        { value: "devops_infra.j2", label: "Devops Infra" },
        
      ],
      "Transform Infra": [
        { value: "transform_infra.j2", label: "Transform Infra" },
      ],
    }
  },
  "2": {
    "Web Agent": {
      "Convert Mulesoft to Springboot": [
        { value: "convert_mulesoft_to_springboot.j2", label: "Convert Mulesoft to Springboot" },
        // { value: "convert_asp.net_to_react.j2", label: "Convert Asp.net to React Components" },
      ],
      "Html to React": [
        { value: "convert_html_to_react.j2", label: "HTML Conversion to React" },
      ],
    //  "Convert ASP.NET Versions to Another ASP.NET Version": [
    //     { value: "convert_asp.net_4.8_to_8.j2", label: "ASP.NET 4.8 Version to ASP.NET 8" }],
    },
    "DB Agent": {
      "Refactor and Transform SQL": [
      { value: "refactor_procedure.j2", label: "Refactor Procedure" },
      { value: "transform_identity.j2", label: "Transform Identity" },
      ],
      "optimize_performance.j2": [
        { value: "Index Usage", label: "Analyze index performance" },
        { value: "Query Tuning", label: "Use EXPLAIN plans" },
      ],
    },

    "Test Agent": {
      "API Regression Tests": [
        { value: "generate_unit_tests.j2", label: "Write Unit Test" },
      ],
      "UI Test Automation": [
        { value: "generate_ui_tests.j2", label: "Generate UI Tests" },
      ],
    },

    "DevOps Agent": {

      "Infrastructure as Code": [ 
        {
        value: "infrastructure_as_code.j2",
        label: "Infrastructure as Code",
      },
      ],
      },
  
  },
};

export default function Chatbot() {
  const [selDropdownVal, setSelDropdownVal] = useState("");
  const [dropdownList, setDropdownList] = useState([]);
  const [ratingValue, setRatingValue] = useState(0);
  const [comment, setComment] = useState("");
  const [message, setMessage] = useState([]);
  const [content, setContent] = useState("");
  const [selUserStory, setSelUserStory] = useState("");
  const [userStoryList, setUserStoryList] = useState([]);
  const [promptOptions, setPromptOptions] = useState([]);
  const [selectedPromptOption, setSelectedPromptOption] = useState(null);
  const [selApplicationName, setSelApplicationName] = useState("");
  const [fileContent, setFileContent] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [sqlCode, setSqlCode] = useState("");
  const [pushStatus, setPushStatus] = useState("");

  useEffect(() => {
    const agentName = agentIdToNameMap[selDropdownVal];
    const appId = String(selApplicationName);

    if (appId && agentName && selUserStory) {
      const prompts = promptOptionsMap?.[appId]?.[agentName]?.[selUserStory] || [];
      setPromptOptions(prompts);
    } else {
      setPromptOptions([]);
    }
  }, [selApplicationName, selDropdownVal, selUserStory]);

  useEffect(() => {
    const fetchPrompt = async () => {
      if (!selectedPromptOption?.value || !agentIdToNameMap[selDropdownVal]) return;

      try {
        const res = await axios.get(`${API_URL}/get-prompt`, {
          params: {
            prompt_name: selectedPromptOption.value,
            agent_type: agentIdToNameMap[selDropdownVal],
          },
        });

        const content = res?.data?.prompt_content || "";
        setFileContent(content);
        setSqlCode(content);
      } catch (error) {
        console.error("Error fetching prompt:", error);
        setFileContent("-- ⚠️ Unable to fetch prompt.");
      }
    };

    fetchPrompt();
  }, [selectedPromptOption, selDropdownVal]);

  const addMessage = (message) => {
    setMessage((prev) => [...prev, message]);
  };


  const handleRun = async () => {
    if (!sqlCode.trim()) {
      alert("⚠️ Please enter code.");
      return;
    }

    let endpoint = "";
    let payload = {};

    const selectedAgent = agentIdToNameMap[selDropdownVal];

    if (selectedAgent === "DB Agent") {
      endpoint = `${API_URL}/run-db-agent/`;
      payload = {
        sql_code: sqlCode,
        prompt_name: selectedPromptOption?.value || "transform_identity.j2",
      };
    } else if (selectedAgent === "Web Agent") {
      endpoint = `${API_URL}/run-web-agent/`;
      payload = {
        html_code: sqlCode,
        prompt_name: selectedPromptOption?.value || "convert_asp_net_to_react.j2",
      };
    } else if (selectedAgent === "Test Agent") {
      endpoint = `${API_URL}/run-test-agent/`;
      payload = {
        source_code: sqlCode,
        prompt_name: selectedPromptOption?.value || "Convert_ReactPage_to_Playwright.j2",
      };
    } else if (selectedAgent === "Devops Agent") {
      endpoint = `${API_URL}/run-devops-agent/`;
      payload = {
        infra_description: sqlCode,
        prompt_name: selectedPromptOption?.value || "jenkins_pipeline.j2",
      };
    }else {
      alert("⚠️ Unsupported agent selected.");
      return;
    }

    try {
      const res = await axios.post(endpoint, payload);
      console.log("ChatBoat response:", res); 
      let agentResponse;

      if (selectedAgent !== "DevOps Agent") {
        agentResponse = res?.data?.result?.output || "⚠️ No output returned.";
      } else {
        agentResponse = res?.data?.result?.Devops_output || "⚠️ No output returned.";
      }
      console.log(agentResponse)

      setChatHistory((prev) => [...prev, { user: sqlCode, agent: agentResponse }]);
      setSqlCode("");
    } catch (err) {
      const errorMsg = "❌ Error: " + (err?.response?.data?.detail || err.message);
      setChatHistory((prev) => [...prev, { user: sqlCode, agent: errorMsg }]);
    }
  };

   

  const handleDownload = () => {
    if (chatHistory.length === 0) {
      alert("⚠️ No converted output to download.");
      return;
    }

    const latestAgentOutput = chatHistory[chatHistory.length - 1].agent;

    const blob = new Blob([latestAgentOutput], {
      type: "text/plain;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "converted_code.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <Container maxWidth="xl" style={{ width: "100vw", padding: 0 }}>
      <Navbar
        selDropdownVal={selDropdownVal}
        setSelDropdownVal={setSelDropdownVal}
        dropdownList={dropdownList}
        setDropdownList={setDropdownList}
        selApplicationName={selApplicationName}
        setSelApplicationName={setSelApplicationName}
      />
      <Box style={{ display: "flex" }}>
        <Box style={{ height: "35.94em", width: "70%", display: "flex", background: "#e5e4ec" }}>
          <Leftside
            message={message}
            onSend={addMessage}
            content={sqlCode}
            setContent={setSqlCode}
            selectedPrompt={selectedPromptOption?.value || ""}
            selectedAgent={agentIdToNameMap[selDropdownVal] || ""}
            setEditablePrompt={setFileContent}
            setSqlCode={setSqlCode}
            setChatHistory={setChatHistory}
          />
        </Box>
        <Box
          style={{
            height: "90vh",
            width: "30%",
            background: "#e5e4ec",
            display: "flex",
            flexDirection: "column",
            padding: "8px",
          }}
        >
          {selDropdownVal === "" ? (
            <Rightside
              ratingValue={ratingValue}
              setRatingValue={setRatingValue}
              comment={comment}
              setComment={setComment}
            />
          ) : (
            <>
              <PromptBox
                promptOptions={promptOptions}
                setPromptOptions={setPromptOptions}
                selectedPromptOption={selectedPromptOption}
                setSelectedPromptOption={setSelectedPromptOption}
                selUserStory={selUserStory}
                setSelUserStory={setSelUserStory}
                selApplicationName={selApplicationName}
                selDropdownVal={selDropdownVal}
              />
              {/* <Button variant="contained" onClick={handleRun}>Run</Button> */}
              {/* <Button variant="outlined" onClick={handleDownload} style={{ marginTop: "10px" }}>Download</Button> */}
            </>
          )}
        </Box>
      </Box>
    </Container>
  );
}
