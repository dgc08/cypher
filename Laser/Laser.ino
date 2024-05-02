#include <WiFi.h>
#include <esp_sleep.h>

// WLAN zeug
const char* ssid = "VSRO-Paed"; //ssid reinpacken
const char* password = "secureVSRO4wl@n#17" ; //wlan passwort reinpacken

// LDR zeug
const int ldrPin = 33; 


const int threshold = 1400; //wie hell muss testen
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
  sendSignal();
}

void loop() {
  //TCP oder so
  WiFiClient client;
  const int serverPort = 6910; // kp welcher port
  if (!(client.connect("10.1.252.159", serverPort))) { //ip
    Serial.println("Verkackt mit Raspi zu reden");
    return;
  }
  client.println("0");
  while (client.available() == 0) {
    delay(100);
  }

  char response = client.read();

  switch (response) {
    case '0':
      esp_sleep_enable_timer_wakeup(10 * 1000000); // 10 seconds in microseconds
      esp_deep_sleep_start();
      return;
    case '1':
      break;
    default:
      Serial.print("Unknown response: ");
      Serial.println(response);
  }

  // Read LDR
  int ldrValue = analogRead(ldrPin);

  // Print the LDR value to the serial monitor
  //Serial.print("Laser Status: ");
  //Serial.println(ldrValue);

  // Tripwire an?
  if (ldrValue < threshold) {
    // Send a signal via WiFi
    if (!was_activated) {
      sendSignal(client);
      was_activated = true;
    }
  }
  else {
    was_activated = false
  }

  client.stop();
  delay(1000); //kein spam pls
}

void sendSignal(WiFiClient &client) {
  // Send a simple message
  client.println("1");
}
