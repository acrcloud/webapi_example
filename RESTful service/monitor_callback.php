<?php
    $request_url = "https://api.acrcloud.com/v1/monitors/your_project_key/callback";
    $http_method = 'POST';
    $http_uri = '/v1/monitors/your_project_key/callback';
    $timestamp = time();
    $signature_version = '1';
    /*
    This demo shows how to use the RESTful API to upload an audio file ( "data_type":"audio" ) into your bucket.
    You can find account_access_key and account_access_secret in your account page.
    Log into http://console.acrcloud.com -> "Account" (top right corner) -> "RESTful API Keys" -> "Create Key Pair". 
    Be Careful, they are different with access_key and access_secret of your project.
    */
    $account_access_key = 'xxxxxxx';
    $account_access_secret = 'xxxxxxxx';

    $string_to_sign = $http_method . "\n" .
                      $http_uri ."\n" .
                      $account_access_key . "\n" .
                      $signature_version . "\n" .
                      $timestamp;
    $signature = hash_hmac("sha1",$string_to_sign,$account_access_secret,true);
    $signature = base64_encode($signature);

    $postfields = array(
        'callback_url' => 'http://www.your_url.com',
        'post_type' =>'json'
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
