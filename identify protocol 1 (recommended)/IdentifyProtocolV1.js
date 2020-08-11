var url = require('url');
var fs = require('fs');
var crypto = require('crypto');
//npm install request
var request = require('request');

// Replace "###...###" below with your project's host, access_key and access_secret.
var defaultOptions = {
  host: '###YOUR_HOST###',
  endpoint: '/v1/identify',
  signature_version: '1',
  data_type:'audio',
  secure: true,
  access_key: '###YOUR_ACCESS_KEY###',
  access_secret: '###YOUR_ACCESS_SECRET###'
};

function buildStringToSign(method, uri, accessKey, dataType, signatureVersion, timestamp) {
  return [method, uri, accessKey, dataType, signatureVersion, timestamp].join('\n');
}

function sign(signString, accessSecret) {
  return crypto.createHmac('sha1', accessSecret)
    .update(Buffer.from(signString, 'utf-8'))
    .digest().toString('base64');
}

/**
 * Identifies a sample of bytes
 */
function identify(data, options, cb) {

  var current_data = new Date();
  var timestamp = current_data.getTime()/1000;

  var stringToSign = buildStringToSign('POST',
    options.endpoint,
    options.access_key,
    options.data_type,
    options.signature_version,
    timestamp);

  var signature = sign(stringToSign, options.access_secret);

  var formData = {
    sample: data,
    access_key:options.access_key,
    data_type:options.data_type,
    signature_version:options.signature_version,
    signature:signature,
    sample_bytes:data.length,
    timestamp:timestamp,
  }
  request.post({
    url: "http://"+options.host + options.endpoint,
    method: 'POST',
    formData: formData
  }, cb);
}

function identify_v2(data, options, cb) {
    //npm install form-data
    var FormData = require('form-data');
    //npm install node-fetch
    var fetch = require('node-fetch');

    var current_data = new Date();
    var timestamp = current_data.getTime()/1000;
    
    var stringToSign = buildStringToSign('POST',
        options.endpoint,
        options.access_key,
        options.data_type,
        options.signature_version,
        timestamp);
    
    var signature = sign(stringToSign, options.access_secret);
    
    var form = new FormData();
    form.append('sample', data);
    form.append('sample_bytes', data.length);
    form.append('access_key', options.access_key);
    form.append('data_type', options.data_type);
    form.append('signature_version', options.signature_version);
    form.append('signature', signature);
    form.append('timestamp', timestamp);
 
    fetch("http://"+options.host + options.endpoint, 
        {method: 'POST', body: form })
        .then((res) => {return res.text()})
        .then((res) => {cb(res, null)})
        .catch((err) => {cb(null, err)});
}

var bitmap = fs.readFileSync('sample.wav');

identify(Buffer.from(bitmap), defaultOptions, function (err, httpResponse, body) {
  if (err) console.log(err);
  console.log(body);
});

//identify_v2(Buffer.from(bitmap), defaultOptions, function (res, err) {
//    if (!err) {
//        console.log(res);
//    } else {
//        console.log(err);
//    }
//}); 
