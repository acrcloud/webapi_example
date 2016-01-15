var url = require('url');
var crypto = require('crypto');
//npm install request
var request = require('request');

var defaultOptions = {
  host: 'api.acrcloud.com',
  endpoint: '/v1/monitor-streams',
  signature_version: '1',
  access_key: '<your account access key>',
  access_secret: '<your account secret key>'
};

function buildStringToSign(method, uri, accessKey, signatureVersion, timestamp) {
  return [method, uri, accessKey, signatureVersion, timestamp].join('\n');
}

function sign(signString, accessSecret) {
  return crypto.createHmac('sha1', accessSecret)
    .update(new Buffer(signString, 'utf-8'))
    .digest().toString('base64');
}

function add_stream(stream_url, stream_name, project_name, options, cb) {

  var current_data = new Date();
  var timestamp = current_data.getTime()/1000;

  var stringToSign = buildStringToSign('POST',
    options.endpoint,
    options.access_key,
    options.signature_version,
    timestamp);

  var signature = sign(stringToSign, options.access_secret);

  var form = {
    url:stream_url,
    stream_name:stream_name,
    project_name:project_name,
  };
  var headers = {
    'access-key': options.access_key, 
    'signature-version': options.signature_version, 
    'signature': signature, 
    'timestamp':timestamp
  };
  request.post({
    url: "https://"+options.host + options.endpoint,
    method: 'POST',
    form: form,
    headers: headers
  }, cb);
}


add_stream("http://127.0.0.1", "test", "monitor_test", defaultOptions, function (err, httpResponse, body) {
  if (err) console.log(err);
  console.log(body);
});
