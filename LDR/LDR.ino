#include <WiFi.h>

#include "../secrets.h"

// WLAN zeug
const char* ssid = SSID; //ssid reinpacken
const char* password = WLAN_PASSWORD ; //wlan passwort reinpacken

// LDR zeug
const int ldrPin = 33; 


const int threshold = 3000; //wie hell muss testen
bool was_activated = false;

void setup() {
  Serial.begin(115200); 

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
      Serial.println("sleeping");
      delay(10 * 1000); // 10 Secs
      Serial.println("Sleep stop");
      return;
    case '1':
      break;
    default:
      Serial.print("Unknown response: ");
      Serial.println(response);
  }
  client.stop();
  Serial.println("Got status, debugval:");
  Serial.println(analogRead(ldrPin));

  for (unsigned long long i = 0; i < 80 * 1000000; i++) { // The loop takes ~5s on the processor of the ESP 32
    // Read LDR
    int ldrValue = analogRead(ldrPin);

    // Print the LDR value to the serial monitor
    //Serial.print("Laser Status: ");
    //Serial.println(ldrValue);

    // Tripwire an?
    if (ldrValue < threshold) {
      // Send a signal via WiFi
      if (!was_activated) {
        Serial.print("Activation: ");
        client.connect(ip, serverPort);
        client.println("1");
        client.stop();
        Serial.println(" sended");
        was_activated = true;
      }
    }
    else if (was_activated) {
      was_activated = false;
      Serial.println("Deactivation");
      Serial.println(ldrValue);
      delay(500);
    }
  }
  Serial.println("End Iteration");
}
