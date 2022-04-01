#include "WifiCam.hpp"
#include <WiFi.h>

// static const char* WIFI_SSID = "GodOfThunder";
// static const char* WIFI_PASS = "loveu3000";

static const char* WIFI_SSID = "Daddy2k1";
static const char* WIFI_PASS = "khongbiet";

esp32cam::Resolution initialResolution;

WebServer server(80);

void setup_wifi() { 

    IPAddress local_IP(192,168,137,75);
    IPAddress gateway(192, 168, 1, 1); 
    IPAddress subnet(255, 255, 255, 0); 
    IPAddress dns1(1, 1, 1, 1);
    IPAddress dns2(8, 8, 8, 8);

    if (!WiFi.config(local_IP, gateway, subnet, dns1, dns2)) {
        Serial.print("Wifi configuration for static IP failed!");
    }

    WiFi.begin(WIFI_SSID, WIFI_PASS);
    Serial.println("");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi " + String(WIFI_SSID) + " connected.");
    // Serial.println("static: " +String(Wifi.static()));
    Serial.println(WiFi.localIP());
}

void
setup()
{
  Serial.begin(115200);
  Serial.println();

  {
    using namespace esp32cam;

    initialResolution = Resolution::find(1024, 768);

    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(initialResolution);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    if (!ok) {
      Serial.println("camera initialize failure");
      delay(5000);
      ESP.restart();
    }
    Serial.println("camera initialize success");
  }

  // stabilize camera before starting WiFi to reduce "Brownout detector was triggered"
  delay(2000);

  // WiFi.persistent(false);
  // WiFi.mode(WIFI_STA);
  // WiFi.begin(WIFI_SSID, WIFI_PASS);
  // if (WiFi.waitForConnectResult() != WL_CONNECTED) {
  //   Serial.println("WiFi failure");
  //   delay(5000);
  //   ESP.restart();
  // }

  // Serial.println("WiFi connected");
  // Serial.print("http://");
  // Serial.println(WiFi.localIP());
  setup_wifi();
  addRequestHandlers();
  server.begin();
}

void
loop()
{
  server.handleClient();
}