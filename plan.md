<!-- Haha bin krank heute und mir langweilig deswegen mach ich irgendwas hier kp -->
<!-- Buy the sen bundle -->
<!-- ADATS besser -->

# Connection Raspberry - ESP32
- Raspberry: Server
- ESP32 1: Client

- CLIENT: "0": Request status of Component
  - SERVER: "0": ESP32 should be sleeping
  - SERVER: "1": ESP32 should check the LDR
  
  <br>
  If the component is off, the ESP32 should periodically sleep using esp_deep_sleep for 10 seconds and check the status again
  -> Both ESPs check the status at the rasbpi's socket
  <br><br>
  
  Example code for deep sleep (by chatgpt):  
  ```
  #include <esp_sleep.h>

    void setup() {
      // Initialize serial communication for debugging
      Serial.begin(9600);
      
      // Print a message to indicate starting
      Serial.println("ESP32 is going to sleep for 10 seconds...");
    
      // Put ESP32 into deep sleep for 10 seconds
      esp_sleep_enable_timer_wakeup(10 * 1000000); // 10 seconds in microseconds
      esp_deep_sleep_start();
    }
    
    void loop() {
      // This code won't be executed since the ESP32 is in deep sleep mode
    }
  ```
- Client: "1": Tripwire activated
  
  Server has nothing to answer
