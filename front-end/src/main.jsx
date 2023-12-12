import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

// import "./sdk/lib/axios/dist/axios.standalone.js"
// import "./sdk/lib/CryptoJS/rollups/hmac-sha256.js"
// import "./sdk/lib/CryptoJS/rollups/sha256.js"
// import "./sdk/lib/CryptoJS/components/hmac.js"
// import "./sdk/lib/CryptoJS/components/enc-base64.js"
// import "./sdk/lib/url-template/url-template.js"
// import "./sdk/lib/apiGatewayCore/sigV4Client.js"
// import "./sdk/lib/apiGatewayCore/apiGatewayClient.js"
// import "./sdk/lib/apiGatewayCore/simpleHttpClient.js"
// import "./sdk/lib/apiGatewayCore/utils.js"

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
