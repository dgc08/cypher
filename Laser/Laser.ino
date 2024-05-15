#include <WiFi.h>

// WLAN zeug
const char* ssid = SSID; //ssid reinpacken
const char* password = WLAN_PASSWORD ; //wlan passwort reinpacken

const int laserPin = 33; 

void setup() {
  Serial.begin(115200); 
  pinMode(laserPin, OUTPUT);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("-");//funny
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  //TCP oder so
  WiFiClient client;
  const int serverPort = 6910; // kp welcher port
  const char* ip = "10.1.253.67";
  if (!(client.connect(ip, serverPort))) { //ip
    Serial.println("Verkackt mit Raspi zu reden");
    return;
  }
  Serial.println("New Iteration");
  client.println("0");
  while (client.available() == 0) {
    delay(100);
  }

  char response = client.read();

  Serial.println(response);

  switch (response) {
    case '0':
      Serial.println("laser off");
      digitalWrite(laserPin, LOW);
      break;
    case '1':
      Serial.println("laser on");
      digitalWrite(laserPin, HIGH);
      break;
    default:
      Serial.print("Unknown response: ");
      Serial.println(response);
  }
  delay(10 * 1000); // 10 Secs
}
