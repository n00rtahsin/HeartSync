/* * HIGH-SENSITIVITY HEART RATE MONITOR
 * Optimized for low-amplitude signals (950-970 range)
 * Output: Serial Monitor @ 115200 Baud
 */

const int sensorPin = A3;
const int ledPin = 13;

float baseline = 955;      // Matches your steady-state data
float filteredSignal = 955;
float sensitivity = 3.5;    // Detects a 4-point jump as a beat

unsigned long lastBeatTime = 0;
int bpmArray[8];
int bpmIndex = 0;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  Serial.println("--- SENSOR CALIBRATED ---");
  Serial.println("Place finger VERY LIGHTLY");
}

void loop() {
  int raw = analogRead(sensorPin);

  // 1. Slow Baseline Follower (follows the 955 drift)
  baseline = (0.99 * baseline) + (0.01 * raw);

  // 2. Fast Filter (smooths the jitter)
  filteredSignal = (0.2 * raw) + (0.8 * filteredSignal);

  // 3. Calculate the "Pulse Peak"
  // If the light drops (Value increases), blood is flowing
  float pulseValue = filteredSignal - baseline;

  // 4. Beat Detection (Tuned for 79-80 BPM)
  if (pulseValue > sensitivity && (millis() - lastBeatTime > 650)) {
    unsigned long duration = millis() - lastBeatTime;
    int bpm = 60000 / duration;

    if (bpm > 45 && bpm < 120) {
      bpmArray[bpmIndex] = bpm;
      bpmIndex = (bpmIndex + 1) % 8;

      int sum = 0;
      for(int i=0; i<8; i++) sum += bpmArray[i];
      int avgBpm = sum / 8;

      if(avgBpm > 0) {
        Serial.print("Heart Rate: ");
        Serial.print(avgBpm);
        Serial.println(" BPM");
      }

      digitalWrite(ledPin, HIGH);
      lastBeatTime = millis();
    }
  }

  if (millis() - lastBeatTime > 200) digitalWrite(ledPin, LOW);

  delay(20);
}