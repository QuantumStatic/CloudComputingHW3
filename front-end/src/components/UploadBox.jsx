import React, { Fragment, useState } from "react";
import "./UploadBox.css";
import { uploadPhoto } from "./../utlities.js";

const UploadBox = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [addedLabels, setAddedLabels] = useState("");

  const handleFileChange = (event) => {
    const reader = new FileReader();

    reader.onload = (loadEvent) => {
      const arrayBuffer = loadEvent.target.result;
      setSelectedFile(arrayBuffer);
    };

    reader.readAsArrayBuffer(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      console.log("No file chosen");
      return;
    }

    console.log("Uploading file:", selectedFile);
    uploadPhoto(selectedFile, addedLabels, "chair.png");
    setSelectedFile(null);
    // const fd = new FormData();
    // fd.append("file", selectedFile);
    // fd.append("x-amz-meta-customLabels", addedLabels);
  };

  return (
    <div className="flex-container">
      <div id="same-line-container">
        <label
          htmlFor="file-upload"
          className={"custom-file-upload backgroundcolour-font"}
        >
          Open File Browser
        </label>
        <input
          id="file-upload"
          type="file"
          onChange={handleFileChange}
          accept="image/*"
        />

        <div className="horizontal-spacer" />

        <div> {selectedFile ? selectedFile.name : ""} </div>
      </div>

      <div className="vertical-spacer" />

      <form>
        <label htmlFor="AdditionalLabelBox">Additional Labels:</label>
        <input
          type="text"
          id="AdditionalLabelBox"
          className={"backgroundcolour-font StandardBorderProperties"}
          value={addedLabels}
          onChange={(e) => setAddedLabels(e.target.value)}
          placeholder="Labels seperated by ';'"
        />
      </form>

      <div className="vertical-spacer" />
      <button id="SubmitButton" onClick={handleUpload} type="submit">
        Upload
      </button>
    </div>
  );
};

export default UploadBox;
