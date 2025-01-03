#include "esp_camera.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "driver/rtc_io.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <base64.h>

// #define CAMERA_MODEL_AI_THINKER // Has PSRAM
#define PWDN_GPIO_NUM  32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM  0
#define SIOD_GPIO_NUM  26
#define SIOC_GPIO_NUM  27

#define Y9_GPIO_NUM    35
#define Y8_GPIO_NUM    34
#define Y7_GPIO_NUM    39
#define Y6_GPIO_NUM    36
#define Y5_GPIO_NUM    21
#define Y4_GPIO_NUM    19
#define Y3_GPIO_NUM    18
#define Y2_GPIO_NUM    5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM  23
#define PCLK_GPIO_NUM  22


const char *ssid = "chien";
const char *password = "hehehehe";

const char* serverName = "http://192.168.137.241:8000/api/streaming/22b5a903-f08d-484e-8767-ea3dcc440eb7/";

esp_err_t configCamera();
void connectWiFi();
void sendImage(camera_fb_t* fb);

void setup() {
  // Disable brownout detector
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  Serial.println("Configuring for camera...");
  esp_err_t err = configCamera();
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
  }
  else Serial.println("Camera ready!");

  Serial.println("Connecting to WiFi...");
  connectWiFi();
  Serial.println("WiFi connected");
}

void loop() {
  camera_fb_t * fb = NULL;
  fb = esp_camera_fb_get();
  if(!fb) {
    Serial.println("Camera capture failed");
    delay(1000);
    return;
  }
  sendImage(fb);
  esp_camera_fb_return(fb);
}

esp_err_t configCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.grab_mode = CAMERA_GRAB_LATEST;
  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 10;

  if (psramFound()) {
    config.fb_count = 2;
    config.fb_location = CAMERA_FB_IN_PSRAM;
  } else {
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_DRAM;
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  return err;
}

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void sendImage(camera_fb_t* fb) {
  if(WiFi.status() == WL_CONNECTED) {
    char* image_buffer = (char*) fb->buf;
    String img_b64 = base64::encode(String(image_buffer, fb->len));
    String payload = "{\"img_b64\": \"" + img_b64 + "\"}";
    HTTPClient http;
    http.begin(String(serverName));
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(payload);
    Serial.print("Response code: ");
    Serial.println(httpResponseCode);
    http.end();
    delay(20);
  } 
  else return;
}
