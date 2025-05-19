import React, { useState } from "react";
import "../App.css";
import { useNavigate } from "react-router";
import {
  Box,
  FormControl,
  IconButton,
  InputAdornment,
  InputLabel,
  Link,
  OutlinedInput,
  TextField,
  Typography,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import ButtonComp from "../Components/Button";

export default function Signin() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [emailErr, setEmailErr] = useState("");
  const [passwordErr, setPasswordErr] = useState("");

  const emailLocal = localStorage.getItem("Email");
  const passwordLocal = localStorage.getItem("Password");

  const handleSignin = () => {
    if (JSON.stringify(email) === emailLocal) {
      if (JSON.stringify(password) === passwordLocal) {
        navigate("/Chatbot");
      } else {
        setPasswordErr("Invalid password");
      }
    } else {
      setEmailErr("Invalid email");
    }
  };

  const handleClear = () => {
    setEmail("");
    setPassword("");
    setPasswordErr("");
    setEmailErr("");
  };

  const handleClickShowPassword = () => setShowPassword((show) => !show);

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const handleMouseUpPassword = (event) => {
    event.preventDefault();
  };

  return (
    <Box>
      <Typography variant="h5" style={{ marginBottom: 20 }}>
        Signin Details
      </Typography>
      <Box
        component="form"
        sx={{ "& .MuiTextField-root": { m: 1, width: "50ch" } }}
        noValidate
        autoComplete="off"
      >
        <TextField
          id="outlined-error"
          label="Email"
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          error={emailErr}
        />
      </Box>
      <Box>
        <FormControl sx={{ m: 1, width: "50ch" }} variant="outlined">
          <InputLabel htmlFor="outlined-adornment-password">
            Password
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            type={showPassword ? "text" : "password"}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label={
                    showPassword ? "hide the password" : "display the password"
                  }
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  onMouseUp={handleMouseUpPassword}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            error={passwordErr}
          />
        </FormControl>
      </Box>
      <Box
        style={{
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-around",
          margin: 20,
        }}
      >
        <ButtonComp text={"Submit"} onClick={handleSignin} />
        <ButtonComp text={"Cancel"} onClick={handleClear} />
      </Box>
      <Box style={{ display: "flex", flexDirection: "row" }}>
        <Typography>Already haven't an account?</Typography>
        <Link href="/"> Signup</Link>
      </Box>
    </Box>
  );
}
