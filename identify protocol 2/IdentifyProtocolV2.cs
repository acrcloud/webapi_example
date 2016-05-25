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
class IdentifyProtocolV2
   {
      public static string postHttp(string url, IDictionary<string, string> datas, int timeout)
      {
          string result = "";
          if (url == null || url == "" || datas == null)
          {
              return result;
          }
          List<string> arrDatas = new List<string>();
          foreach (var item in datas)
          {
              arrDatas.Add(item.Key + "=" + HttpUtility.UrlEncode(item.Value));
          }
          string postDatas = string.Join("&", arrDatas.ToArray());
          HttpWebRequest request = null;
          HttpWebResponse response = null;
          Stream writer = null;
          StreamReader myReader = null;
          try
          {
              request = (HttpWebRequest)WebRequest.Create(url);
              request.Timeout = timeout;
              request.Method = "POST";
              request.ContentType = "application/x-www-form-urlencoded";
              byte[] postDatasBytes = System.Text.Encoding.UTF8.GetBytes(postDatas);
              request.ContentLength = postDatasBytes.Length;
              writer = request.GetRequestStream();
              writer.Write(postDatasBytes, 0, postDatasBytes.Length);
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

           var dict = new Dictionary<string, string>();
           dict.Add("access_key", accessKey);
           dict.Add("sample_bytes", queryData.Length.ToString());
           dict.Add("sample", encodeToBase64(queryData));
           dict.Add("timestamp", timestamp);
           dict.Add("signature", signature);
           dict.Add("data_type", queryType);
           dict.Add("signature_version", sigVersion);

           string res = postHttp(reqURL, dict, timeout);
           Debug.WriteLine("adf =" + encodeToBase64(queryData).Length);
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
                  // Replace "###...###" below with your project's access_key and access_secret.
                  string result = IdentifyProtocolV2.recognize("###YOUR_HOST", "###YOU_ACCESS_KEY###", "###YOUR_ACCESS_SECRET###", datas, "audio");
                  Console.WriteLine(result);
              }
          }
          
          Console.ReadLine();
      }
  }
}
