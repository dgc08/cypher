
#include <WiFi.h>

// WLAN zeug
const char* ssid = "VSRO-Paed"; //ssid reinpacken
const char* password = "secureVSRO4wl@n#17" ; //wlan passwort reinpacken

// LDR zeug
const int ldrPin = 33; 


const int threshold = 500; //wie hell muss testen

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
  sendSignal();
}

void loop() {
  // Read LDR
  int ldrValue = analogRead(ldrPin);

  // Print the LDR value to the serial monitor
  Serial.print("Laser Status: ");
  Serial.println(ldrValue);

  // Tripwire an?
  if (ldrValue < threshold) {
    // Send a signal via WiFi
    sendSignal();
  }

  delay(1000); //kein spam pls
}

void sendSignal() {
  //TCP oder so
  WiFiClient client;
  const int serverPort = 80; // kp welcher port
  if (client.connect("10.1.252.159", serverPort)) { //ip
    // Send a simple message
    client.println("Got you!");
    client.stop();
  } else {
    Serial.println("Bruh kein wlan");
  }
}
