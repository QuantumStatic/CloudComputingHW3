import React, { Fragment, useState } from "react";
import { Grid } from "react-visual-grid";

import "./SearchArea.css";
import { getPhotos } from "./../utlities.js";

function extractPhotos(links) {
  let photoGroups = [];
  if (links.length % 2 === 0) {
    for (let i = 0; i < links.length; i += 2) {
      photoGroups.push([
        { imgSrc: links[i], key: i },
        {
          imgSrc: links[i + 1],
          key: i + 1,
        },
      ]);
    }
  } else {
    for (let i = 0; i < links.length - 1; i += 2) {
      photoGroups.push([
        { imgSrc: links[i], key: i },
        {
          imgSrc: links[i + 1],
          key: i + 1,
        },
      ]);
    }

    photoGroups.push([
      {
        imgSrc: links[links.length - 1],
        key: links.length - 1,
      },
    ]);
  }

  return photoGroups;
  // return [
  //   [
  //     { "imgSrc":"https://assbucket2.s3.amazonaws.com/img4.png",
  //       "key":0
  //     },
  //     { "imgSrc":"https://assbucket2.s3.amazonaws.com/img5.png",
  //       "key":1
  //     }
  //   ],
  //   [
  //     {
  //       "imgSrc":"https://assbucket2.s3.amazonaws.com/img9.png",
  //       "key":"2"
  //     }
  //   ]
  // ]
}

const SearchArea = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [photos, setPhotos] = useState([]);

  const handleSearch = async () => {
    // let response = getPhotos(searchTerm);
    let response = null;
    const links = [
      "https://assbucket2.s3.amazonaws.com/dogandcat.png",
      "https://assbucket2.s3.amazonaws.com/catphoto.png",
      "https://assbucket2.s3.amazonaws.com/dog.png",
      "https://assbucket2.s3.amazonaws.com/fish.png"
  ];
    setPhotos(extractPhotos(links));
    console.log(response);
  };

  return (
    <div id="SearchAreaContainer">
      <div id="SearchBarContainer" className="search-area-flex-item">
        <input
          type="text"
          id="SearchBar"
          className="backgroundcolour-font StandardBorderProperties"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search photos..."
        />
        <button id="SearchButton" onClick={handleSearch}>
          <img id="SearchButtonImg" src="src/assets/search.png" alt="Search" />
        </button>
      </div>

      <div className="gallery search-area-flex-item">
        {photos.map((photoGroup, idx) => {
          return (
            <div className="pics-row" key={photoGroup[0].key}>
              <img
                className="row-img"
                src={photoGroup[0].imgSrc}
                alt={`img ${idx}`}
              />
              {photoGroup[1] ? (
                <img
                  className="row-img"
                  src={photoGroup[1].imgSrc}
                  alt={`img ${idx}`}
                />
              ) : null}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default SearchArea;
