#include <WiFi.h>
#include <SPI.h>
#include <MFRC522.h>
#include <HTTPClient.h>

const int RED_LED = 2;
const int GREEN_LED = 4;

#define RST_PIN 22
#define SS_PIN 5
MFRC522 rfid(SS_PIN, RST_PIN);

const char* ssid = "YOUR_SSID";          
const char* password = "YOUR_PASSWORD";         

void setup() {
  Serial.begin(115200);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  SPI.begin();
  rfid.PCD_Init();
  connectToWiFi();
}

void connectToWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  
  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED && attempt < 5) {
    delay(1000);
    Serial.print(".");  // Indicate connection attempts
    attempt++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to Wi-Fi");
    Serial.print("IP Address: "); 
    Serial.println(WiFi.localIP());
    blinkLED(GREEN_LED);  // Blink GREEN LED once on success
  } else {
    Serial.println("Failed to connect to Wi-Fi");
    blinkLED(RED_LED);    // Blink RED LED once on failure
  }
}

void loop() {
  // Continuously check for RFID tags
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    String scannedRFID = "";

    // Read the RFID serial number
    for (byte i = 0; i < rfid.uid.size; i++) {
      scannedRFID += String(rfid.uid.uidByte[i], HEX);
    }

    Serial.print("Scanned RFID: ");
    Serial.println(scannedRFID);

    // Send the scanned RFID to the server
    sendRFIDToServer(scannedRFID); 

    rfid.PICC_HaltA();  // Halt the RFID card
    delay(1000);        // Wait before reading the next card
  }
}

void sendRFIDToServer(const String& rfidID) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("YOUR-HOST-ADDRESS/api/attendance/"); // Specify the URL

    http.addHeader("Content-Type", "application/json");

    // Create JSON payload
    String jsonPayload = "{\"rfid_id\": \"" + rfidID + "\"}";

    // Send the POST request
    int httpResponseCode = http.POST(jsonPayload);

    // Check for the response
    if (httpResponseCode == 200) {
      Serial.println("POST successful!");
      blinkLED(GREEN_LED);  // Blink GREEN LED for success
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
      blinkLED(RED_LED);  // Blink RED LED for error
    }

    http.end();  // Free resources
  } else {
    Serial.println("Wi-Fi not connected");
  }
}

void blinkLED(int ledPin) {
  digitalWrite(ledPin, HIGH);
  delay(500);
  digitalWrite(ledPin, LOW);
}
