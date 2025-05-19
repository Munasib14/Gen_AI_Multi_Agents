import React from "react";
import {
  AppBar,
  Box,
  FormControl,
  MenuItem,
  Select,
  Toolbar,
  Typography,
} from "@mui/material";

// Application list
const applicationList = [{ id: 1, name: "MAPS" },
{ id: 2, name: "ACET" }
];

// Web agents linked to applications
const webAgentList = [
  { id: 101, name: "DB Agent", applicationId: 1 },
  { id: 102, name: "Web Agent", applicationId: 1 },
  { id: 103, name: "Test Agent", applicationId: 1 },
  { id: 104, name: "DevOps Agent", applicationId: 1 },
  { id: 201, name: "DB Agent", applicationId: 2 },
  { id: 202, name: "Web Agent", applicationId: 2 },
  { id: 203, name: "Test Agent", applicationId: 2 },
  { id: 204, name: "DevOps Agent", applicationId:2 },
];

function Navbar({
  selDropdownVal,
  setSelDropdownVal,
  selApplicationName,
  setSelApplicationName,
}) {
  // Filter agents based on selected application
  const filteredWebAgents = webAgentList.filter(
    (agent) => agent.applicationId === selApplicationName
  );

  return (
    <AppBar position="static" style={{ background: "#1565c0" }}>
      <Toolbar>
        <Box
          style={{
            width: "70%",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
          }}
        >
          <Typography variant="h6">UHC Chatbot Demo</Typography>
          <Typography
            variant="h6"
            color="black"
            style={{ marginRight: "10px" }}
          >
            Maps Chatbot
          </Typography>
          <Box style={{ width: "30%" }}>
            <FormControl
              fullWidth
              style={{ background: "white", borderRadius: 10 }}
            >
              <Select
                value={selApplicationName}
                onChange={(e) => {
                  setSelApplicationName(e.target.value);
                  setSelDropdownVal(""); // Reset agent dropdown
                }}
                displayEmpty
                inputProps={{ "aria-label": "Select Application" }}
              >
                <MenuItem value="">Select Application</MenuItem>
                {applicationList.map((item) => (
                  <MenuItem key={item.id} value={item.id}>
                    {item.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </Box>

        <Box style={{ width: "30%" }}>
          <FormControl
            fullWidth
            style={{ background: "white", marginLeft: 10, borderRadius: 10 }}
          >
            <Select
              value={selDropdownVal}
              onChange={(e) => {
                setSelDropdownVal(e.target.value); // This should update the agent ID
              }}
              displayEmpty
              inputProps={{ "aria-label": "Select Agent" }}
              disabled={!selApplicationName} // Only allow agent selection if an application is selected
            >
              <MenuItem value="">Select  Agent</MenuItem>
              {filteredWebAgents.map((item) => (
                <MenuItem key={item.id} value={item.id}>
                  {item.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;


// useEffect(() => {
//   // Fetch data from dummy API
//   axios
//     .get("https://jsonplaceholder.typicode.com/users")
//     .then((response) => {
//       setDropdownList(response.data);
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//     });
// }, []);