 import java.io.BufferedReader;
 import java.io.File;
 import java.io.FileInputStream;
 import java.io.IOException;
 import java.io.InputStreamReader;
 import java.io.OutputStreamWriter;
 import java.io.PrintWriter;
 import java.net.HttpURLConnection;
 import java.net.URL;
 import java.net.URLEncoder;
 import java.util.Calendar;
 import java.util.HashMap;
 import java.util.Map;
 import javax.crypto.Mac;
 import javax.crypto.spec.SecretKeySpec;
 
 import org.apache.commons.codec.binary.Base64;
 
 public class ACRCloudProtocolV2 {
 
 	private String encodeBase64(byte[] bstr) {  
 		Base64 base64 = new Base64();  
 		return new String(base64.encode(bstr));
     }  
 	
 	private String encryptByHMACSHA1(byte[] data, byte[] key) {
 		try {
 			SecretKeySpec signingKey = new SecretKeySpec(key, "HmacSHA1");
 			Mac mac = Mac.getInstance("HmacSHA1");
 			mac.init(signingKey);
 			byte[] rawHmac = mac.doFinal(data);
 			return encodeBase64(rawHmac);
 		} catch (Exception e) {
 			e.printStackTrace();
 		}
 		return "";
 	}
 	
 	private String postHttp(String url, Map<String, String> postParams, int timeout) {
 		PrintWriter out = null;
 		BufferedReader in = null;
 		OutputStreamWriter osw = null;
 		HttpURLConnection conn = null;
 		URL realUrl = null;
 		String result = "";
 		try {
 			realUrl = new URL(url);
 		    conn = (HttpURLConnection) realUrl.openConnection();  
 			conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");  
 			conn.setDoOutput(true);
 			conn.setDoInput(true);
 			conn.setConnectTimeout(timeout);
 			conn.setReadTimeout(timeout);
 
 			StringBuilder sbd = new StringBuilder();
 			for (String key : postParams.keySet()) {
 				String value = postParams.get(key);
 				sbd.append(key + "=" + URLEncoder.encode(value, "UTF-8") + "&");
 			}
 			String postData = sbd.substring(0, sbd.length() - 1);
 			
 			osw = new OutputStreamWriter(conn.getOutputStream());  
 		    osw.write(postData);  
 		    osw.flush();  		    
 			
 			if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
 				in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
 				String line;
 				while ((line = in.readLine()) != null) {
 					result += line;
 				}
 			}
 		} catch (Exception e) {
 			e.printStackTrace();
 		} finally {
 			try {
 				if (out != null) {
 					out.close();
 					out = null;
 				}
 				if (in != null) {
 					in.close();
 					in = null;
 				}
 				if (osw != null) {
 					osw.close(); 
 					osw = null;
 				}
 				if (conn != null) {
 					conn.disconnect();
 					conn = null;
 				}
 			} catch (IOException ex) {
 				ex.printStackTrace();
 			}
 		}
 		return result;
 	}
 	
 	private String getUTCTimeSeconds() {  
 	    Calendar cal = Calendar.getInstance();   
 	    int zoneOffset = cal.get(Calendar.ZONE_OFFSET);   
 	    int dstOffset = cal.get(Calendar.DST_OFFSET);    
 	    cal.add(Calendar.MILLISECOND, -(zoneOffset + dstOffset));    
 	    return cal.getTimeInMillis()/1000 + "";
 	}  
 	
  
     public String recognize(String host, String accessKey, String secretKey, byte[] queryData, String queryType, int timeout)
     {
     	String method = "POST";
     	String httpURL = "/v1/identify";
     	String dataType = queryType;
     	String sigVersion = "1";
     	String timestamp = getUTCTimeSeconds();
 
     	String reqURL = "http://" + host + httpURL;
 
     	String sigStr = method + "\n" + httpURL + "\n" + accessKey + "\n" + dataType + "\n" + sigVersion + "\n" + timestamp;
     	String signature = encryptByHMACSHA1(sigStr.getBytes(), secretKey.getBytes());
 
         Map<String, String> postParams = new HashMap<String, String>();
         postParams.put("access_key", accessKey);
         postParams.put("sample_bytes", queryData.length + "");
         postParams.put("sample", encodeBase64(queryData));
         postParams.put("timestamp", timestamp);
         postParams.put("signature", signature);
         postParams.put("data_type", queryType);
         postParams.put("signature_version", sigVersion);
 
         String res = postHttp(reqURL, postParams, timeout);
 
         return res;
     }
     
 	public static void main(String[] args) {
 		File file = new File("E://sample.wav");
 		byte[] buffer = new byte[1024 * 1024];
 		if (!file.exists()) {
 			return;
 		}
 		FileInputStream fin = null;
 		int bufferLen = 0;
 		try {
 			fin = new FileInputStream(file);
 			bufferLen = fin.read(buffer, 0, buffer.length);
 		} catch (Exception e) {
 			e.printStackTrace();
 		} finally {
 			try {
 				if (fin != null) {
 					fin.close();
 				}
 			} catch (IOException e) {
 				e.printStackTrace();
 			}
 		}
 		System.out.println("bufferLen=" + bufferLen);
 		
 		if (bufferLen <= 0)
 			return;
 		
 		byte[] postDatas = new byte[bufferLen];
 		System.arraycopy(buffer, 0, postDatas, 0, bufferLen);
 		ACRCloudProtocolV2 a = new ACRCloudProtocolV2();
 		
 		String result = a.recognize("ap-southeast-1.api.acrcloud.com", "xxxxxxxx", "xxxxxxxx", postDatas, "audio", 80000);
 		System.out.println(result);
 	}
 
 }
