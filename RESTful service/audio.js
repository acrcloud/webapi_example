var url = require('url');
var path = require('path');
var fs = require('fs');
var crypto = require('crypto');
//npm install request
var request = require('request');

var defaultOptions = {
  host: 'api.acrcloud.com',
  endpoint: '/v1/audios',
  signature_version: '1',
  secure: true,
  access_key: 'xxx',
  access_secret: 'xxxxx'
};

function buildStringToSign(method, uri, accessKey, signatureVersion, timestamp) {
  return [method, uri, accessKey, signatureVersion, timestamp].join('\n');
}

function sign(signString, accessSecret) {
  return crypto.createHmac('sha1', accessSecret)
    .update(Buffer.from(signString, 'utf-8'))
    .digest().toString('base64');
}

/**
 * Identifies a sample of bytes
 */
function upload(file_path, bucket, title, audio_id, data_type="fingerprint", custom_fields=None, cb) {
  var current_data = new Date();
  var timestamp = current_data.getTime()/1000;

  var stringToSign = buildStringToSign('POST',
    defaultOptions.endpoint,
    defaultOptions.access_key,
    defaultOptions.signature_version,
    timestamp);
  console.log(stringToSign)

  var signature = sign(stringToSign, defaultOptions.access_secret);
  console.log(signature)

  var headers = {
    'access-key': defaultOptions.access_key,
    'signature-version': defaultOptions.signature_version,
    'signature': signature,
    'timestamp':timestamp
  };
  var formData = {
    'audio_file': {
        'value':  fs.createReadStream(file_path),
        'options': {
            'filename': path.basename(file_path),
            'contentType': 'fingerprint/lo'
        }
    },
    'data_type':data_type,
    'bucket_name':bucket,
    'title':title,
    'audio_id':audio_id,
  }
  if (custom_fields) {
        keys = []
        values = []
        for (var k in custom_fields) {
            keys.push(k)
            values.push(custom_fields[k])
        }
        formData['custom_key[]'] = keys
        formData['custom_value[]'] = values
  }

  request.post({
    url: "https://"+defaultOptions.host + defaultOptions.endpoint,
    method: 'POST',
    headers: headers,
    formData: formData
  }, cb);
}

function get_audio(acr_id, cb) {
  var current_data = new Date();
  var timestamp = current_data.getTime()/1000;

  var endpoint = defaultOptions.endpoint+"/"+acr_id

  var stringToSign = buildStringToSign('GET',
    endpoint,
    defaultOptions.access_key,
    defaultOptions.signature_version,
    timestamp);

  var signature = sign(stringToSign, defaultOptions.access_secret);

  var headers = {
    'access-key': defaultOptions.access_key,
    'signature-version': defaultOptions.signature_version,
    'signature': signature,
    'timestamp':timestamp
  };

  request.get({
    url: "https://"+defaultOptions.host + endpoint,
    method: 'GET',
    headers: headers,
  }, cb);
}

var title = "test"
var audio_id = "test"
var bucket_name = "eu-test"
var data_type = "fingerprint"
var file_path = '1040210008.mp3.wav.lo';
var custom_fields = {"key1":"value1"}

upload(file_path, bucket_name, title, audio_id, data_type, custom_fields , function (err, httpResponse, body) {
  if (err) console.log(err);
  console.log(body);
});

get_audio("4b616d1b695bf4c35ed5103f9cbdd507", function(err, httpResponse, body){
    console.log(body);
});
