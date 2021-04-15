<?php

$http_method = "POST";
$http_uri = "/v1/identify";
$data_type = "audio";
$signature_version = "1" ;
$timestamp = time() ;


// Replace "###...###" below with your project's host, access_key and access_secret.
$requrl = "http://###YOUR_HOST###/v1/identify";
$access_key =  '###YOUR_ACCESS_KEY###';
$access_secret =  '###YOUR_ACCESS_SECRET###';

$string_to_sign = $http_method . "\n" . 
                  $http_uri ."\n" . 
                  $access_key . "\n" . 
                  $data_type . "\n" . 
                  $signature_version . "\n" . 
                  $timestamp;
$signature = hash_hmac("sha1", $string_to_sign, $access_secret, true);

$signature = base64_encode($signature);

// suported file formats: mp3,wav,wma,amr,ogg, ape,acc,spx,m4a,mp4,FLAC, etc 
// File size: < 1M , You'de better cut large file to small file, within 15 seconds data size is better
$file = $argv[1];
//$filesize = filesize($file);
//$cfile = new CURLFile($file, "mp3", basename($argv[1]));
$content = file_get_contents($argv[1]);
$filesize = strlen($content);

$postfields = array(
               "sample" => $content, 
               "sample_bytes"=>$filesize, 
               "access_key"=>$access_key, 
               "data_type"=>$data_type, 
               "signature"=>$signature, 
               "signature_version"=>$signature_version, 
               "timestamp"=>$timestamp);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $requrl);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

$result = curl_exec($ch);
echo $result;
//$response = curl_exec($ch);
//if ($response == true) {
//    $info = curl_getinfo($ch);
//} else {
//    $errmsg = curl_error($ch);
//    print $errmsg;
//}
curl_close($ch);
?>
