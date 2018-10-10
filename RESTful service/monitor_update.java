
import java.io.File;
import java.io.IOException;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

// import commons-codec-<version>.jar, download from http://commons.apache.org/proper/commons-codec/download_codec.cgi
import org.apache.commons.codec.binary.Base64;

// import HttpClient,  download from http://hc.apache.org/downloads.cgi
/**
 *   
 *   commons-codec-1.1*.jar
 *   commons-logging-1.*.jar
 *   httpclient-4.*.jar
 *   httpcore-4.*.jar
 *   httpmime-4.*.jar
 * 
 * */
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.entity.ContentType;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

public class Update_monitor {

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

	private String getUTCTimeSeconds() {
		Calendar cal = Calendar.getInstance();
		int zoneOffset = cal.get(Calendar.ZONE_OFFSET);
		int dstOffset = cal.get(Calendar.DST_OFFSET);
		cal.add(Calendar.MILLISECOND, -(zoneOffset + dstOffset));
		return cal.getTimeInMillis() / 1000 + "";
	}

	private String putHttp(String url, Map<String, String> putParams,
                           Map<String, String> headerParams, int timeout) {
		String result = null;

		CloseableHttpClient httpClient = HttpClients.createDefault();
		try {
			HttpPut httPut = new HttpPut(url);

			if (headerParams != null) {
				for (String key : headerParams.keySet()) {
					String value = headerParams.get(key);
					httpPut.addHeader(key, value);
				}
			}

                        JSONObject jsonObject = JSONObject.fromObject(putParams);
                        String jsonString = jsonObject.toString();

                        StringEntity params = new StringEntity(jsonString, "UTF-8");
                        params.setContentType("application/json");

			RequestConfig requestConfig = RequestConfig.custom()
					.setConnectionRequestTimeout(timeout)
					.setConnectTimeout(timeout).setSocketTimeout(timeout)
					.build();
			httpPut.setConfig(requestConfig);

			HttpResponse response = httpClient.execute(httpPut);

			System.out.println(response.getStatusLine().getStatusCode());

			HttpEntity entity = response.getEntity();
			result = EntityUtils.toString(entity);
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				httpClient.close();
			} catch (IOException e) {
			}
		}
		return result;
	}

    public String update(String streamID, String streamUrl, String streamName, String region, String realtime,
                         String record, String accessKey, String accessSecret){
        String result = null;
        String reqUrl = "https://api.acrcloud.com/v1/monitor-streams/"+streamID;
        String htttMethod = "PUT";
        String httpAction = "/v1/monitor-streams/"+streamID;
        String signatureVersion = "1";
        String timestamp = this.getUTCTimeSeconds();

 		String sigStr = htttMethod + "\n" + httpAction + "\n" + accessKey
				+ "\n" + signatureVersion + "\n" + timestamp;
		String signature = encryptByHMACSHA1(sigStr.getBytes(),
				accessSecret.getBytes());

		Map<String, String> headerParams = new HashMap<String, String>();
		headerParams.put("access-key", accessKey);
		headerParams.put("signature-version", signatureVersion);
		headerParams.put("signature", signature);
		headerParams.put("timestamp", timestamp);

		Map<String, String> postParams = new HashMap<String, String>();
		postParams.put("stream_name", streamName);
		postParams.put("url", streamUrl);
		postParams.put("region", region);
		postParams.put("realtime", realtime);
		postParams.put("record", record);

		result = this.putHttp(reqUrl, postParams, headerParams, 8000);

		return result;
    }
	/**
	 * @param args
	 */
	public static void main(String[] args) {
                String streamID = "";
		String streamUrl = "";
		String streamName = "";
		String region = "";
		String realtime = "";
		String record = "";
		String accessKey = "";
                String accessSecret = "";

		Update_monitor ua = new Update_monitor();

		String result = ua.update(streamID, streamUrl, streamName, region, realtime,
                                  record, accessKey, accessSecret);
		if (result == null) {
			System.out.println("upload error");
		}

		System.out.println(result);
	}
}
