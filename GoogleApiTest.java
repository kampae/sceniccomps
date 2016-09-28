 import java.io.FileOutputStream;
 import java.io.IOException;
 import java.io.InputStream;
 import java.io.OutputStream;
 import java.net.URL;

public class GoogleApiTest {

public static void main(String[] args) throws Exception {
    String apiKey = "AIzaSyBJN20CtR9R9AdWsInx-sAF_CoLRkI66so";
    String imageUrl = "https://maps.googleapis.com/maps/api/streetview?size=600x300&location=1+North+College+Street,+Northfield,+MN+55057&heading=151.78&pitch=-0.76&key=" + apiKey;
    String destinationFile = "javapic.jpg";

    saveImage(imageUrl, destinationFile);
}

public static void saveImage(String imageUrl, String destinationFile) throws IOException {
    URL url = new URL(imageUrl);
    InputStream is = url.openStream();
    OutputStream os = new FileOutputStream(destinationFile);

    byte[] b = new byte[2048];
    int length;

    while ((length = is.read(b)) != -1) {
        os.write(b, 0, length);
    }

    is.close();
    os.close();
}

}