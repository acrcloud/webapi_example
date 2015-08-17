using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using System.Net;
using System.Web;
using System.IO;
using System.Security.Cryptography;
using System.Diagnostics;

namespace ACRCloudWebAPITest
{
   class ACRCloudProtocolV1
   {
       public static string postHttp(string url, IDictionary<string, Object> postParams, int timeout)
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
                   var header = string.Format(filePartHeader, "sample", "sample");
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
               request.Timeout = timeout;
               request.Method = "POST";              
               request.ContentType = "multipart/form-data; boundary=" + BOUNDARYSTR;

               memStream.Position = 0;
               byte[] tempBuffer = new byte[memStream.Length];
               memStream.Read(tempBuffer, 0, tempBuffer.Length);

               writer = request.GetRequestStream();
               writer.Write(tempBuffer, 0, tempBuffer.Length);
               writer.Close();
               writer = null;

               response = (HttpWebResponse)request.GetResponse();
               myReader = new StreamReader(response.GetResponseStream(), Encoding.UTF8);
               result = myReader.ReadToEnd();
           }
           catch (WebException e)
           {
               Debug.WriteLine("timeout:\n" + e.ToString());
           }
           catch (Exception e)
           {
               Debug.WriteLine("other excption:" + e.ToString());
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

       public static string encryptByHMACSHA1(string input, string key)
       {
           HMACSHA1 hmac = new HMACSHA1(System.Text.Encoding.UTF8.GetBytes(key));
           byte[] stringBytes = Encoding.UTF8.GetBytes(input);
           byte[] hashedValue = hmac.ComputeHash(stringBytes);
           return encodeToBase64(hashedValue);
       }

       public static string encodeToBase64(byte[] input)
       {
           string res = Convert.ToBase64String(input, 0, input.Length);
           return res;
       }

       public static string recognize(string host, string accessKey, string secretKey, byte[] queryData, string queryType, int timeout = 8000)
       {
           string method = "POST";
           string httpURL = "/v1/identify";
           string dataType = queryType;
           string sigVersion = "1";
           string timestamp = ((int)DateTime.UtcNow.Subtract(new DateTime(1970, 1, 1, 0, 0, 0, DateTimeKind.Utc)).TotalSeconds).ToString();

           string reqURL = "http://" + host + httpURL;

           string sigStr = method + "\n" + httpURL + "\n" + accessKey + "\n" + dataType + "\n" + sigVersion + "\n" + timestamp;
           string signature = encryptByHMACSHA1(sigStr, secretKey);

           var dict = new Dictionary<string, object>();
           dict.Add("access_key", accessKey);
           dict.Add("sample_bytes", queryData.Length.ToString());
           dict.Add("sample", queryData);
           dict.Add("timestamp", timestamp);
           dict.Add("signature", signature);
           dict.Add("data_type", queryType);
           dict.Add("signature_version", sigVersion);

           string res = postHttp(reqURL, dict, timeout);

           return res;
       }
   } 
   class Program
   {
       static void Main(string[] args)
       {
           using (FileStream fs = new FileStream(@"E:\sample.wav", FileMode.Open))
           {
               using (BinaryReader reader = new BinaryReader(fs))
               {
                   byte[] datas = reader.ReadBytes((int)fs.Length);
                   // Replace "xxxxxxxx" below with your project's access_key and access_secret.
                   string result = ACRCloudProtocolV1.recognize("ap-southeast-1.api.acrcloud.com", "xxxxxxxx", "xxxxxxxx", datas, "audio");
                   Console.WriteLine(result);
               }
           }
           
           Console.ReadLine();
       }
   }
}
