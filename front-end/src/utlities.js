import apigClientFactory from "./sdk/apigClient.js";

console.log("Loading API Gateway SDK");

var sdk = apigClientFactory.newClient({});

console.log("API Gateway SDK loaded");

export function uploadPhoto(image, labels, filename) {
  console.log("Uploading photo");
  var params = {
    "x-amz-meta-customLabels": labels,
    filename: filename,
    bucketname: "assbucket2",
    "Content-Type": "image/png",
    "Accept": "*/*",
  };
  var body = image;
  var additionalParams = {};
  return sdk.uploadBucketnameFilenamePut(params, body, additionalParams);
}

export function getPhotos(query) {
  console.log("Getting photos");
  var params = { q: query };
  var body = {};
  var additionalParams = {};
  return sdk.searchGet(params, body, additionalParams);
}
