require 'openssl'
require 'base64'
require 'net/http/post/multipart'

# Replace "###...###" below with your account access_key and access_secret.
requrl = "https://api.acrcloud.com/v1/audios"
access_key = "###YOUR_ACCESS_KEY###"
access_secret = "###YOUR_ACCESS_SECRET###"

http_method = "POST"
http_uri = "/v1/audios"
data_type = "audio"
signature_version = "1"
timestamp = Time.now.utc().to_i.to_s

string_to_sign = http_method+"\n"+http_uri+"\n"+access_key+"\n"+signature_version+"\n"+timestamp

digest = OpenSSL::Digest.new('sha1')
signature = Base64.encode64(OpenSSL::HMAC.digest(digest, access_secret, string_to_sign))

file_name = ARGV[0]
sample_bytes = File.size(file_name)
title = "TEST"
audio_id = "123"
bucket = "Your bucket name"

header = {:signature => signature, "access-key" => access_key, :timestamp => timestamp, "signature-version" => "1"}

url = URI.parse(requrl)
puts(url.path)
File.open(file_name) do |file|
  req = Net::HTTP::Post::Multipart.new url.path,
    "audio_file" => UploadIO.new(file, "audio/mp3", file_name),
    "title" =>title,
    "audio_id"=>audio_id,
    "bucket_name"=>bucket,
    "data_type"=> "audio"
  req.add_field(:signature, signature.strip)
  req.add_field("access-key", access_key)
  req.add_field(:timestamp, timestamp)
  req.add_field("signature-version", "1")

  res = Net::HTTP.start(url.host, url.port, use_ssl: true) do |http|
    http.request(req)
  end
  puts(res.body)
end
