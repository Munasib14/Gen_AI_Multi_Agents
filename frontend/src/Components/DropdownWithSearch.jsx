import { Box, TextareaAutosize } from "@mui/material";
import React, { useState } from "react";
import CreatableSelect from "react-select/creatable";
import ButtonComp from "./Button";
import styles from "./Chat.module.css";

const DropdownWithSearch = ({
  promptOptions,
  setPromptOptions,
  selectedPromptOption,
  setSelectedPromptOption,
}) => {
  const [editValue, setEditValue] = useState("");

  const handleCreateOption = (inputValue) => {
    const newOption = { value: inputValue, label: inputValue };
    setPromptOptions([...promptOptions, newOption]);
  };

  const handleDeleteOption = () => {
    if (selectedPromptOption) {
      setPromptOptions(
        promptOptions.filter(
          (option) => option.value !== selectedPromptOption.value
        )
      );
      setSelectedPromptOption(null);
    }
  };

  const handleEditOption = () => {
    if (selectedPromptOption?.value && editValue.trim() !== "") {
      setPromptOptions(
        promptOptions.map((option) =>
          option.value === selectedPromptOption.value
            ? { ...option, label: editValue, value: editValue }
            : option
        )
      );
      setSelectedPromptOption(null);
      setEditValue("");
    }
  };

  return (
    <Box style={{ maxWidth: 350 }}>
      <CreatableSelect
        options={promptOptions}
        onCreateOption={handleCreateOption}
        onChange={setSelectedPromptOption}
        value={selectedPromptOption}
        isClearable
        isSearchable
      />
      {selectedPromptOption?.value == null ? (
        <></>
      ) : (
        <>
          <Box className={styles.TextAreaContainerSearch}>
            <TextareaAutosize
              minRows={8}
              maxRows={8}
              className={styles.TextAreaSearch}
              value={editValue || selectedPromptOption?.value}
              onChange={(e) => setEditValue(e.target.value)}
            />
          </Box>

          <Box
            style={{
              marginTop: 20,
              justifyContent: "space-evenly",
              display: "flex",
            }}
          >
            <ButtonComp onClick={handleDeleteOption} text={"Delete Option"} />
            <ButtonComp onClick={handleEditOption} text={"Edit Option"} />
          </Box>
        </>
      )}
    </Box>
  );
};

export default DropdownWithSearch;
