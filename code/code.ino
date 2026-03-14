#include <WiFi.h>
#include <WiFiUdp.h>

// WiFi Credentials
const char* ssid = "Fox-17";
const char* password = "Kyra2bin9";

// Static IP (Choose an IP outside your router's usual DHCP range to avoid conflicts)
IPAddress local_IP(192, 168, 1, 100); 
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

WiFiUDP udp;
unsigned int localUdpPort = 4210;
char incomingPacket[255];

void setup() {
  Serial.begin(115200);

  // Set Static IP
  if (!WiFi.config(local_IP, gateway, subnet)) {
    Serial.println("STA Failed to configure Static IP");
  }

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(localUdpPort);
}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0; // Null-terminate the string
    }
    
    // For debugging: see the data in Serial Monitor
    Serial.print("Received: ");
    Serial.println(incomingPacket);

    // Motor control logic will go here
  }
}
