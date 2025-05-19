import React, { useState } from "react";
import "../App.css";
import { useNavigate } from "react-router";
import { emailRegex, passwordRegex } from "../Utils";
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

export default function Signup() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [emailErr, setEmailErr] = useState("");
  const [passwordErr, setPasswordErr] = useState("");

  const handleSignup = () => {
    if (!emailRegex.test(email)) {
      setEmailErr("Invalid Email Address");
    } else if (!passwordRegex.test(password)) {
      setPasswordErr(
        "Invalid password. It should be at least 6 characters long and include at least one lowercase letter, one uppercase letter, one digit, and one special character."
      );
    } else {
      localStorage.setItem("Email", JSON.stringify(email));
      localStorage.setItem("Password", JSON.stringify(password));
      // SIGNUP API CALL
      navigate("/Signin");
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
        Signup Details
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
        <ButtonComp text={"Submit"} onClick={handleSignup} />
        <ButtonComp text={"Cancel"} onClick={handleClear} />
      </Box>
      <Box style={{ display: "flex", flexDirection: "row" }}>
        <Typography>Already have an account?</Typography>
        <Link href="/signin"> Signin</Link>
      </Box>
    </Box>
  );
}
