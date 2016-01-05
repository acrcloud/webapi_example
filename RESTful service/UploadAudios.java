
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

public class UploadAudios {

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

	private String postHttp(String url, Map<String, Object> postParams,
			Map<String, String> headerParams, int timeout) {
		String result = null;

		if (postParams == null) {
			return result;
		}

		CloseableHttpClient httpClient = HttpClients.createDefault();
		try {
			HttpPost httpPost = new HttpPost(url);

			if (headerParams != null) {
				for (String key : headerParams.keySet()) {
					String value = headerParams.get(key);
					httpPost.addHeader(key, value);
				}
			}

			MultipartEntityBuilder mEntityBuilder = MultipartEntityBuilder
					.create();
			for (String key : postParams.keySet()) {
				Object value = postParams.get(key);
				if (value instanceof String || value instanceof Integer) {
					ContentType contentType = ContentType.create("text/plain", "UTF-8");
					StringBody stringBody = new StringBody(value+"", contentType);
					mEntityBuilder.addPart(key, stringBody);
				} else if (value instanceof File) {
					mEntityBuilder.addBinaryBody(key, (File) value);
				}
			}

			httpPost.setEntity(mEntityBuilder.build());

			RequestConfig requestConfig = RequestConfig.custom()
					.setConnectionRequestTimeout(timeout)
					.setConnectTimeout(timeout).setSocketTimeout(timeout)
					.build();
			httpPost.setConfig(requestConfig);

			HttpResponse response = httpClient.execute(httpPost);

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

	public String upload(String audioId, String audioTitle, String dataPath,
			String dataType, String bucketName, String accessKey,
			String accessSecret, Map<String, String> userParams) {
		String result = null;
		String reqUrl = "https://api.acrcloud.com/v1/audios";
		String htttMethod = "POST";
		String httpAction = "/v1/audios";
		String signatureVersion = "1";
		String timestamp = this.getUTCTimeSeconds();

		File file = new File(dataPath);
		if (!file.exists()) {
			return null;
		}

		String sigStr = htttMethod + "\n" + httpAction + "\n" + accessKey
				+ "\n" + signatureVersion + "\n" + timestamp;
		String signature = encryptByHMACSHA1(sigStr.getBytes(),
				accessSecret.getBytes());

		Map<String, String> headerParams = new HashMap<String, String>();
		headerParams.put("access-key", accessKey);
		headerParams.put("signature-version", signatureVersion);
		headerParams.put("signature", signature);
		headerParams.put("timestamp", timestamp);

		Map<String, Object> postParams = new HashMap<String, Object>();
		postParams.put("title", audioTitle);
		postParams.put("audio_id", audioId);
		postParams.put("bucket_name", bucketName);
		postParams.put("data_type", dataType);
		postParams.put("audio_file", file);

		if (userParams != null) {
			int i = 0;
			for (String key : userParams.keySet()) {
				String value = userParams.get(key);
				postParams.put("custom_key[" + i + "]", key);
				postParams.put("custom_value[" + i + "]", value);
				i++;
			}
		}

		result = this.postHttp(reqUrl, postParams, headerParams, 8000);

		return result;
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		String audioId = "XXX";
		String audioTitle = "xxx";
		String dataPath = "./a.mp3";
		String dataType = "audio"; // audio & fingerprint
		String bucketName = "<your bucket name>";
		String accessKey = "<your console access_key>";
		String accessSecret = "<your console access_secret>";

		Map<String, String> userParams = new HashMap<String, String>();
		userParams.put("<user-defined-key1>", "<user-defined-value1>");
		userParams.put("<user-defined-key2>", "<user-defined-value2>");

		UploadAudios ua = new UploadAudios();

		String result = ua.upload(audioId, audioTitle, dataPath, dataType,
				bucketName, accessKey, accessSecret, userParams);
		if (result == null) {
			System.out.println("upload error");
		}

		System.out.println(result);
	}

}
