<?php
    $request_url = 'https://api.acrcloud.com/v1/audios';
    $http_method = 'POST';
    $http_uri = '/v1/audios';
    $timestamp = time();
    $signature_version = '1';
    /*
    This demo shows how to use the RESTful API to upload an audio file ( "data_type":"audio" ) into your bucket.
    You can find account_access_key and account_access_secret in your account page.
    Log into http://console.acrcloud.com -> "Account" (top right corner) -> "RESTful API Keys" -> "Create Key Pair". 
    Be Careful, they are different with access_key and access_secret of your project.
    */
    $account_access_key = '0780b60d5696d6e2';
    $account_access_secret = '8e5c66ff23918fe6c70b92d580fa38e7';

    $string_to_sign = $http_method . "\n" .
                      $http_uri ."\n" .
                      $account_access_key . "\n" .
                      $signature_version . "\n" .
                      $timestamp;
    $signature = hash_hmac("sha1",$string_to_sign,$account_access_secret,true);
    $signature = base64_encode($signature);
    // suported file formats: mp3,wav,wma,amr,ogg, ape,acc,spx,m4a,mp4,FLAC, etc 
    $file = $argv[1];
    if(class_exists('\CURLFile'))
        $cfile = new CURLFile($file, "audio/mp3", basename($argv[1]));
    else
        $cfile = '@' . $file;
    $postfields = array(
        'audio_file' => $cfile,
        'title' => 'test',
        'audio_id' => '1234',
        'bucket_name' => '',
        'data_type'=>'fingerprint',
        'custom_key[0]' => 'key1',
        'custom_value[0]' => 'value1',
        'custom_key[1]' => 'key2',
        'custom_value[1]' => 'value2',
    );
    $headerArray = array();
    $headers = array(
        'access-key' => $account_access_key,
        'timestamp' => $timestamp,
        'signature-version' => '1',
        'signature' => $signature
    );
    foreach( $headers as $n => $v ) {
        $headerArr[] = $n .':' . $v;
    }
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $request_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headerArr);
    $response = curl_exec($ch);
    var_dump($response);
    curl_close($ch);
?>
