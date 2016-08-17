using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;


using System.Diagnostics;
using System.IO;

using System.Web;
using System.Security.Cryptography;
using System.Net;

namespace ACRCloudUploadFile
{
    class ACRCloudUploadFile
    {
        public static string PostHttp(string url, IDictionary<string, Object> headerParams, IDictionary<string, Object> postParams, int timeoutSecond)
        {
            string result = "";
            string BOUNDARYSTR = "acrcloud***copyright***2015***" + DateTime.Now.Ticks.ToString("x");
            string BOUNDARY = "--" + BOUNDARYSTR + "\r\n";
            var ENDBOUNDARY = Encoding.ASCII.GetBytes("--" + BOUNDARYSTR + "--\r\n\r\n");

            var stringKeyHeader = BOUNDARY +
                           "Content-Disposition: form-data; name=\"{0}\"" +
                           "\r\n\r\n{1}\r\n";
            var filePartHeader = BOUNDARY +
                            "Content-Disposition: form-data; name=\"{0}\"; filename=\"{1}\"\r\n" +
                            "Content-Type: application/octet-stream\r\n\r\n";

            var memStream = new MemoryStream();
            foreach (var item in postParams)
            {
                if (item.Value is string)
                {
                    string tmpStr = string.Format(stringKeyHeader, item.Key, item.Value);
                    byte[] tmpBytes = Encoding.UTF8.GetBytes(tmpStr);
                    memStream.Write(tmpBytes, 0, tmpBytes.Length);
                }
                else if (item.Value is byte[])
                {
                    var header = string.Format(filePartHeader, "audio_file", "audio_file");
                    var headerbytes = Encoding.UTF8.GetBytes(header);
                    memStream.Write(headerbytes, 0, headerbytes.Length);
                    byte[] sample = (byte[])item.Value;
                    memStream.Write(sample, 0, sample.Length);
                    memStream.Write(Encoding.UTF8.GetBytes("\r\n"), 0, 2);
                }
            }
            memStream.Write(ENDBOUNDARY, 0, ENDBOUNDARY.Length);

            HttpWebRequest request = null;
            HttpWebResponse response = null;
            Stream writer = null;
            StreamReader myReader = null;
            try
            {
                request = (HttpWebRequest)WebRequest.Create(url);
                request.Timeout = timeoutSecond * 1000;
                request.Method = "POST";
                foreach (var item in headerParams)
                {
                    if (item.Value is string)
                    {
                        request.Headers.Add(item.Key+":"+item.Value);
                    }
                }
                request.ContentType = "multipart/form-data; boundary=" + BOUNDARYSTR;

                memStream.Position = 0;
                byte[] tempBuffer = new byte[memStream.Length];
                memStream.Read(tempBuffer, 0, tempBuffer.Length);

                writer = request.GetRequestStream();
                writer.Write(tempBuffer, 0, tempBuffer.Length);
                writer.Flush();
                writer.Close();
                writer = null;

                response = (HttpWebResponse)request.GetResponse();
                myReader = new StreamReader(response.GetResponseStream(), Encoding.UTF8);
                result = myReader.ReadToEnd();
            }
            catch (WebException e)
            {
                Console.WriteLine("timeout:\n" + e.ToString());
            }
            catch (Exception e)
            {
                Console.WriteLine("other excption:" + e.ToString());
            }
            finally
            {
                if (memStream != null)
                {
                    memStream.Close();
                    memStream = null;
                }
                if (writer != null)
                {
                    writer.Close();
                    writer = null;
                }
                if (myReader != null)
                {
                    myReader.Close();
                    myReader = null;
                }
                if (request != null)
                {
                    request.Abort();
                    request = null;
                }
                if (response != null)
                {
                    response.Close();
                    response = null;
                }
            }

            return result;
        }

        public static string EncryptByHMACSHA1(string input, string key)
        {
            HMACSHA1 hmac = new HMACSHA1(System.Text.Encoding.UTF8.GetBytes(key));
            byte[] stringBytes = Encoding.UTF8.GetBytes(input);
            byte[] hashedValue = hmac.ComputeHash(stringBytes);
            return EncodeToBase64(hashedValue);
        }

        public static string EncodeToBase64(byte[] input)
        {
            string res = Convert.ToBase64String(input, 0, input.Length);
            return res;
        }

        public static string Upload(IDictionary<string, Object> audioParams, IDictionary<string, Object> userParams, int timeoutSecond)
        {
            string reqUrl = "https://api.acrcloud.com/v1/audios";
            string httpMethod = "POST";
            string httpAction = "/v1/audios";
            string signatureVersion = "1";
            string accessKey = (string)audioParams["access_key"];
            string accessSecret = (string)audioParams["access_secret"];
            string audioId = (string)audioParams["audio_id"];
            string audioTitle = (string)audioParams["audio_title"];
            string bucketName = (string)audioParams["bucket_name"];
            string dataType = (string)audioParams["data_type"];
            byte[] audioData = (byte[])audioParams["audio_data"];
            string timestamp = ((int)DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc)).TotalSeconds).ToString();

            string sigStr = httpMethod + "\n" + httpAction + "\n" + accessKey + "\n" + signatureVersion + "\n" + timestamp;
            string signature = EncryptByHMACSHA1(sigStr, accessSecret);

            Console.WriteLine(signature);

            var headerParams = new Dictionary<string, object>();
            headerParams.Add("access-key", accessKey);
            headerParams.Add("signature-version", signatureVersion);
            headerParams.Add("signature", signature);
            headerParams.Add("timestamp", timestamp);

            var postParams = new Dictionary<string, object>();
            postParams.Add("title", audioTitle);
            postParams.Add("audio_id", audioId);
            postParams.Add("bucket_name", bucketName);
            postParams.Add("data_type", dataType);
            postParams.Add("audio_file", audioData);

            if (userParams != null) {
			    int i = 0;
                foreach (var item in userParams)
                {
                    postParams.Add("custom_key[" + i + "]", item.Key);
                    postParams.Add("custom_value[" + i + "]", item.Value);
                    i++;
                }
		    }

            string res = PostHttp(reqUrl, headerParams, postParams, timeoutSecond);

            return res;
        }

        static void Main(string[] args)
        {
            string audioId = "XXX";
            string audioTitle = "xxx";
            string dataPath = "./a.mp3";
            string dataType = "audio"; // audio & fingerprint
            string bucketName = "<your bucket name>";
            string accessKey = "<your console access_key>";
            string accessSecret = "<your console access_secret>";

            var userParams = new Dictionary<string, object>();
            userParams.Add("<user-defined-key1>", "<user-defined-value1>");
            userParams.Add("<user-defined-key2>", "<user-defined-value2>");

            var audioParams = new Dictionary<string, object>();
            audioParams.Add("access_key", accessKey);
            audioParams.Add("access_secret", accessSecret);
            audioParams.Add("audio_id", audioId);
            audioParams.Add("audio_title", audioTitle);
            audioParams.Add("bucket_name", bucketName);
            audioParams.Add("data_type", dataType);
            

            using (FileStream fs = new FileStream(dataPath, FileMode.Open))
            {
                using (BinaryReader reader = new BinaryReader(fs))
                {
                    byte[] datas = reader.ReadBytes((int)fs.Length);
                    audioParams.Add("audio_data", datas);

                    // default timeout 10 seconds
                    string result = ACRCloudUploadFile.Upload(audioParams, userParams, 10);
                    Console.WriteLine(result);
                    Console.ReadLine();
                }
            }
        }
    }
}
